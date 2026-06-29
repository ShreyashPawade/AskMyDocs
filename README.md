# 📚 AskMyDocs

> A production-ready Retrieval-Augmented Generation (RAG) application that enables users to upload PDF documents and interact with them using natural language. Built with **FastAPI**, **Gemini**, **ChromaDB**, **BM25**, **Cross-Encoder Re-ranking**, and a **Streamlit** frontend.

---

## 🚀 Live Demo

**Frontend:** *(Coming Soon)*

**Backend API:** *(Coming Soon)*

---

## ✨ Features

* 📄 Upload and index PDF documents
* 💬 Chat with your documents using natural language
* 🔍 Hybrid Retrieval (BM25 + ChromaDB Vector Search)
* 🎯 Cross-Encoder Re-ranking for improved retrieval quality
* 🧠 History-aware Query Rewriting
* 📚 Source Citation with page numbers
* 📊 Confidence Score for every response
* ⚡ Streaming LLM responses
* 🗂️ Document Management (Upload, View, Delete)
* 💾 Session-based conversation memory
* 🐳 Dockerized deployment
* 🎨 Modern Streamlit interface

---

# 🏗️ System Architecture

```
                User
                  │
                  ▼
          Streamlit Frontend
                  │
                  ▼
            FastAPI Backend
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
 Query Rewriter       Hybrid Retriever
                              │
             ┌────────────────┴───────────────┐
             ▼                                ▼
      BM25 Search                    Chroma Vector Search
             └──────────────┬───────────────┘
                            ▼
                 Reciprocal Rank Fusion
                            ▼
                 Cross Encoder Re-ranking
                            ▼
                  Retrieved Context
                            ▼
                  Gemini 2.5 Flash
                            ▼
          Answer + Sources + Confidence
```

---

# 📂 Project Structure

```
AskMyDocs/
│
├── app.py
├── retriever.py
├── vector_store.py
├── llm.py
├── model.py
├── document_registry.py
│
├── frontend/
│   ├── streamlit_app.py
│   ├── api.py
│   ├── config.py
│   ├── style.css
│   ├── components/
│   └── utils/
│
├── docs/
├── uploads/
├── chroma_db/
│
├── Dockerfile
├── Dockerfile.streamlit
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# 🔍 Retrieval Pipeline

1. User submits a question.
2. Query is rewritten using conversation history.
3. Hybrid retrieval is performed:

   * BM25 lexical search
   * ChromaDB semantic vector search
4. Reciprocal Rank Fusion combines both result sets.
5. Cross-Encoder re-ranks retrieved chunks.
6. Top-ranked context is passed to Gemini.
7. Gemini generates the final answer.
8. Sources and confidence score are returned to the user.

---

# 🛠️ Technology Stack

### Backend

* FastAPI
* Python
* Google Gemini 2.5 Flash
* ChromaDB
* Sentence Transformers
* Rank-BM25
* Cross Encoder
* PyPDF

### Frontend

* Streamlit
* Requests
* Custom CSS

### Deployment

* Docker
* Docker Compose

---

# 📊 API Endpoints

| Method | Endpoint                | Description         |
| ------ | ----------------------- | ------------------- |
| GET    | `/`                     | API Status          |
| GET    | `/health`               | Health Check        |
| POST   | `/chat`                 | Chat with documents |
| POST   | `/chat_stream`          | Streaming responses |
| POST   | `/upload`               | Upload PDF          |
| GET    | `/documents`            | List documents      |
| GET    | `/documents/{filename}` | Document details    |
| DELETE | `/documents/{filename}` | Delete document     |

---

# ⚙️ Installation

## Clone the repository

```bash
git clone https://github.com/ShreyashPawade/AskMyDocs.git

cd AskMyDocs
```

---

## Create a virtual environment

```bash
python -m venv venv
```

Activate it:

### macOS/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configure environment variables

Create a `.env` file:

```text
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

## Start the backend

```bash
uvicorn app:app --reload
```

---

## Start the frontend

```bash
streamlit run frontend/streamlit_app.py
```

---

# 🐳 Docker

Build the containers

```bash
docker compose build
```

Run the application

```bash
docker compose up
```

Backend:

```
http://localhost:8000
```

Frontend:

```
http://localhost:8501
```

---

# 📸 Screenshots

Add screenshots of:

* Home page
* Upload PDF
* Chat interface
* Source citations
* Document management
* Streaming responses

---

# 🚀 Future Improvements

* User Authentication (JWT)
* Persistent Chat History
* PostgreSQL Integration
* OCR Support for Scanned PDFs
* Multi-query Retrieval
* HyDE Retrieval
* RAG Evaluation (Ragas / DeepEval)
* Deployment on Kubernetes
* Monitoring Dashboard
* Role-based Access Control

---

# 👨‍💻 Author

**Shreyash Pawade**

* B.Tech, NIT Warangal
* WorldQuant Research Consultant
* Quantitative Research & AI Enthusiast

GitHub: https://github.com/ShreyashPawade

---

# 📄 License

This project is licensed under the MIT License.
