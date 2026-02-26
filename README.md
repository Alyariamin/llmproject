# 📚 RAG-Based Document QA System  
Django + LangChain + Celery + TF-IDF

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system using Django and LangChain.

Users submit questions, and the system retrieves relevant published documents using TF-IDF similarity search before generating an AI-powered answer grounded in those documents.

The architecture separates indexing, retrieval, and generation to ensure performance and clean responsibility boundaries.

---

## 🏗 Architecture

### Main Request Flow

Client  
↓  
Django REST API  
↓  
LangChain RetrievalQA  
↓  
Custom TFIDFRetriever  
↓  
Redis (cached TF-IDF index)  
↓  
LLM (OpenRouter / OpenAI-compatible endpoint)

### Index Rebuild Flow (Asynchronous)

Document Saved/Deleted  
↓  
Django Signal  
↓  
Celery Task  
↓  
Rebuild TF-IDF Index  
↓  
Store Index in Redis  

---

## 🧠 Core Components

### 1. Documents

Each document contains:

- title  
- content  
- status (Draft / Published / Archived)  

Only published documents are indexed and searchable.

---

### 2. TF-IDF Indexing

The system uses TfidfVectorizer from scikit-learn to:

- Combine document title and content  
- Convert documents into numerical vectors  
- Compute cosine similarity for search  

The cached index contains:

```python
{
    "vectorizer": fitted TfidfVectorizer,
    "doc_vectors": numpy array,
    "doc_ids": list of document IDs
}
```

The index is stored in Redis under:

tfidf_vectors

---

### 3. Celery Integration

Index rebuilding is handled asynchronously.

Whenever a document is created, updated, or deleted:

1. A Django signal triggers.  
2. A Celery task runs in the background.  
3. The TF-IDF index is rebuilt.  
4. The new index replaces the old cache.  

This prevents heavy computation during API requests.

---

### 4. Custom TFIDFRetriever

The retriever:

- Loads the cached TF-IDF index from Redis  
- Vectorizes the user query  
- Computes cosine similarity  
- Filters results using a similarity threshold  
- Returns relevant documents to LangChain  

The retriever never rebuilds the index.

---

### 5. LangChain Usage

LangChain orchestrates retrieval and generation using:

```python
RetrievalQA.from_chain_type(...)
```

LangChain:

- Calls the custom retriever  
- Injects retrieved document context into the prompt  
- Sends the prompt to the configured LLM  
- Returns the generated answer with source documents  

LangChain handles orchestration, not indexing.

---

## 📂 Project Structure

yourapp/

├── views.py              # API endpoint  
├── retriever.py          # Custom TF-IDF retriever  
├── tasks.py              # Celery tasks  
├── signals.py            # Reindex triggers  
├── services/  
│     └── index_service.py  # Index building logic  
├── models.py             # Document & Survey models  

---

## 🔄 End-to-End Flow

1. User sends a question to the API.  
2. LangChain calls TFIDFRetriever.  
3. Retriever loads cached TF-IDF index.  
4. Similar documents are selected.  
5. Documents are passed to the LLM.  
6. The LLM generates an answer.  
7. Question, answer, and related documents are stored in the database.  

---

## 🧩 Technologies Used

- Django  
- Django REST Framework  
- LangChain  
- Celery  
- Redis  
- scikit-learn  
- NumPy  
- OpenRouter / OpenAI-compatible LLM API  


## 🐳 Run with Docker

Build and start all services:

```bash
docker compose up --build
```

The app will be available at:

```
http://localhost:8000
```

---


## 👤 Create Superuser for Admin Panel

To access Django admin:

```bash
docker compose exec web python manage.py createsuperuser
```
---


- Admin panel URL: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- Search URL: [http://localhost:8000/search/](http://localhost:8000/search/)

---
## 🔍 Search API

You can send POST requests to the search endpoint:

```
http://localhost:8000/search/
```

### Request Format (JSON)

```json
{
  "question": "my question"
}
```

### Example using `curl`

```bash
curl -X POST http://localhost:8000/search/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Django?"}'
```

The response will contain the answer returned by the OpenRouter API (via your backend logic).

---

## 🛑 Stop the Project

```bash
docker compose down
```

