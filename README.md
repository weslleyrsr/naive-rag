# naive-rag
Simple RAG based app

![rag architecture](./assets/rag.png)

## Todo
 - Store chunk hash in metadata to compare if the content changed.
 - Review chunk size
 - Exclude not relevant chunks from prompt (min similarity)

# Setup

### Dependencies
```bash
  pip install -r requirements.txt
```

### Data ingestion
```bash
  python populate_database.py
```

### Query data
```bash
  python query_data.py "beside the bank's money, the bank holds what?"
```

### Env
```dotenv
OPENAI_API_KEY=<your-api-key>
```

# References
 - [Python RAG Tutorial (with Local LLMs): AI For Your PDFs](https://youtu.be/2TJxpyO3ei4?list=PLZJBfja3V3Ru9jR6vxD6TRrz1bRI4zK6j)
 - [PyPDFDirectoryLoader](https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.pdf.PyPDFDirectoryLoader.html#langchain_community.document_loaders.pdf.PyPDFDirectoryLoader)
 - [Text splitters](https://python.langchain.com/api_reference/text_splitters/index.html)
 - [Chromadb](https://python.langchain.com/api_reference/community/vectorstores/langchain_community.vectorstores.chroma.Chroma.html)
 - [ChatOpenAI](https://python.langchain.com/api_reference/openai/chat_models/langchain_openai.chat_models.base.ChatOpenAI.html)