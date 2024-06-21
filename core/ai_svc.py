import csv
from io import BytesIO
from django.conf import settings

from django.db import connection
from langchain_core.documents import Document as lc_document
from langchain_core.prompts.prompt import PromptTemplate
from langchain_postgres import PGVector
from langchain_groq import ChatGroq
from langchain_ai21 import AI21Embeddings
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

CONNECTION_STRING = (
    f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?sslmode=allow"
)
COLLECTION_NAME = 'langchain_collection'

ai21_embedding = AI21Embeddings(
    api_key=settings.AI21_API_KEY
)

def process_user_document(document, user):
    file = document.file.file
    collection = f"{user.id}{user.username}_collection"
    if document.file_type == "pdf":
        memory_object = BytesIO()
        file.seek(0)
        memory_object.write(file.read())
        memory_object.seek(0)

        loader = PyPDFLoader(memory_object)
        pages = loader.load_and_split()
    else:
        content = ""
        if document.file_type == "csv":
            data = csv.DictReader(file)
            for line in data:
                content += f"{line}\n"
        else:
            content = file.read().decode('utf-8')
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
        content_doc = lc_document(page_content=content, metadata={"source": document.file.name})

    split_documents = text_splitter.split_documents(pages if document.file_type == "pdf" else [content_doc])
    processed_lc_documents = [
        lc_document(page_content=chunk.page_content, metadata=chunk.metadata) for chunk in split_documents
    ]

    PGVector.from_documents(
        embedding=ai21_embedding,
        documents=processed_lc_documents,
        collection_name=collection,
        connection=CONNECTION_STRING
    )

    document.processed = True
    document.save()


def delete_user_document(document, user):
    collection = f"{user.id}{user.username}_collection"
    vector_ids = _get_vector_id(document.file.name)
    _, db = _get_llm(collection)

    db.delete(vector_ids, collection_only=True)
    document.delete()

def rag_from_query(query, user):
    collection = f"{user.id}{user.username}_collection"
    chat, db = _get_llm(collection)

    retriever = db.as_retriever(search_kwargs={'k': 10})

    prompt = set_custom_prompt()

    qa = RetrievalQA.from_chain_type(llm=chat,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False,
        chain_type_kwargs={"prompt": prompt}
    )

    response = qa.invoke({"query": query})
    
    return response


def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """

    template = """Use the following pieces of information to answer the user's question in brazillian portuguese.\n
    If you don't know the answer, just say that you don't know, don't try to make up an answer.\n\n
    Context: {context}\n
    Question: {question}\n\n
    Only return the helpful answer below, if possible, and nothing else.
    """

    prompt = PromptTemplate(template=template,
                            input_variables=['context', 'question'])
    return prompt


def _get_llm(collection):
    chat = ChatGroq(
        temperature=1,
        groq_api_key=settings.GROQ_API_KEY,
        model_name=settings.GROQ_API_MODEL
    )

    db = PGVector.from_existing_index(ai21_embedding, collection_name=collection, connection=CONNECTION_STRING)
    
    return chat, db


def _get_vector_id(document_name):
    with connection.cursor() as cursor:
        query = """
        SELECT id
        FROM langchain_pg_embedding
        WHERE cmetadata->>'source' = %s
        """
        cursor.execute(query, (document_name,))
        results = cursor.fetchall()

    return [result[0] for result in results] if results else None
