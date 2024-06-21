# Content-scour

## Scour the web. Vasculhe a web.



### RAG - Retrieval Augmented Generation

**This application processes and indexes user documents for efficient
retrieval and question answering.**

Here\'s what it does:

-   Processes user uploaded documents: It can handle various file formats like PDF, CSV, and text files.

-   Extracts content from documents using Langchain:

    -   For PDFs, it splits each page into separate chunks for processing.

    -   For CSV files, it converts each row into text.

    -   For other text files, it reads the entire content.

-   Splits large documents into smaller chunks to improve search performance.

-   Embeds document content using a powerful AI model providade by AI21 to create a compressed representation for efficient searching.

-   Indexes the document embeddings in a database for fast retrieval.

-   Provides a way to search for information within user documents by taking a plain text query as input.

-   Uses a large language model (LLM) providade by Groq to answer the user\'s question based on the retrieved documents and a customizable prompt.

### ChatBot

Answers user-input questions based on standard pre-trained model provided by AwanLLM. [*https://www.awanllm.com*](https://www.awanllm.com/).

LLM: Meta-Llama-3-8B-Instruct

### RAG - Geração aumentada de recuperação 

**Essa aplicação processa e indexa documentos do usuários para
recuperação e resposta eficiente.**

Funcionalidades:

-   Processa documentos enviados por usuários: Suporta diversos formatos como PDF, CSV e arquivos de texto.

-   Extrai conteúdo de documentos:

    -   Para PDFs, divide cada página em partes menores para processamento.

    -   Para arquivos CSV, converte cada linha em texto.

    -   Para outros arquivos de texto, lê todo o conteúdo.

-   Divide documentos grandes em partes menores para melhorar o desempenho da pesquisa.

-   Cria embeddings do conteúdo do documento usando um modelo de IA poderoso para gerar uma representação compactada para pesquisa eficiente.

-   Indexa os embeddings de documentos em um banco de dados para rápida recuperação.

-   Fornece uma maneira de pesquisar informações dentro dos documentos do usuário recebendo uma consulta em texto simples como entrada.

-   Utiliza um grande modelo de linguagem (LLM) para responder à pergunta do usuário com base nos documentos recuperados e em um prompt personalizável.

### ChatBot

Responde perguntas do usuário com base no treinamento fornecido pelos
responsável usando o serviço fornecido pela AwanLLM. [*https://www.awanllm.com*](https://www.awanllm.com/).

LLM: Meta-Llama-3-8B-Instruct

## For devs

Frontend:
-   Vue.js 3
-   Vite 5
-   Vuetify
-   Axios
-   Pinia

Backend:
-   Django 5
-   Langchain

Database:
-   PostgreSQL
-   PGVector

Server:
-   NGINX
-   Certbot

Shipped with Docker.
