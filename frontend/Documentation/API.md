# API Integration Guide

## Overview

The AskMyDocs frontend communicates with a FastAPI backend through REST APIs. This document explains each endpoint and provides usage examples.

## Base URL

```
http://localhost:8000
```

Configure via environment variable:
```env
BACKEND_URL=http://your-backend-url:8000
```

## Authentication

Currently, the API uses no authentication. For production, implement:
- API keys
- JWT tokens
- OAuth2

## Endpoints

### 1. Health Check

Check if backend is online.

**Request:**
```http
GET /health
```

**Response (200 OK):**
```json
{
    "status": "online"
}
```

**Example (Python):**
```python
import requests

response = requests.get("http://localhost:8000/health")
print(response.json())
# Output: {'status': 'online'}
```

**Frontend Usage:**
```python
from api import APIClient

online = APIClient.check_health()
if online:
    st.info("Backend is online")
else:
    st.error("Backend is offline")
```

---

### 2. Chat Message

Send a question and get a response.

**Request:**
```http
POST /chat
Content-Type: application/json

{
    "question": "What is machine learning?",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Parameters:**
- `question` (string, required): User's question
- `session_id` (string, required): Unique session identifier

**Response (200 OK):**
```json
{
    "answer": "Machine learning is a subset of artificial intelligence...",
    "confidence": 4.5,
    "sources": [
        {
            "chunk_id": 12,
            "source": "introduction_to_ml.pdf",
            "page": 3
        },
        {
            "chunk_id": 45,
            "source": "introduction_to_ml.pdf",
            "page": 7
        }
    ]
}
```

**Response Fields:**
- `answer` (string): AI-generated answer to the question
- `confidence` (float): Confidence score (0-5)
- `sources` (array): List of document sources used

**Example (Python):**
```python
import requests
import uuid

payload = {
    "question": "What is machine learning?",
    "session_id": str(uuid.uuid4())
}

response = requests.post(
    "http://localhost:8000/chat",
    json=payload,
    timeout=30
)

if response.status_code == 200:
    data = response.json()
    print(f"Answer: {data['answer']}")
    print(f"Confidence: {data['confidence']}")
    print(f"Sources: {len(data['sources'])} documents")
```

**Frontend Usage:**
```python
from api import APIClient
from utils.session import get_session_id

session_id = get_session_id()
response = APIClient.send_chat_message("Your question", session_id)

if response:
    answer = response["answer"]
    confidence = response["confidence"]
    sources = response["sources"]
```

---

### 3. Stream Chat Message

Stream response token-by-token (for real-time display).

**Request:**
```http
POST /chat_stream
Content-Type: application/json

{
    "question": "Explain quantum computing",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response (200 OK - Streaming):**
```
Quantum computing is a...
field of computing that uses...
quantum bits (qubits) instead of...
classical bits...
```

**Example (Python):**
```python
import requests

payload = {
    "question": "Explain quantum computing",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
}

response = requests.post(
    "http://localhost:8000/chat_stream",
    json=payload,
    stream=True,
    timeout=60
)

for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

**Frontend Usage:**
```python
from api import APIClient

for token in APIClient.stream_chat_message("Your question", session_id):
    st.write(token, end="")
```

---

### 4. Upload Document

Upload a PDF file for indexing.

**Request:**
```http
POST /upload
Content-Type: multipart/form-data

file: <PDF file content>
```

**Parameters:**
- `file` (file, required): PDF file to upload

**Response (200 OK):**
```json
{
    "status": "success",
    "filename": "my_document.pdf",
    "pages": 42,
    "chunks": 168,
    "message": "PDF indexed successfully."
}
```

**Example (Python):**
```python
with open("document.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:8000/upload",
        files=files
    )

if response.status_code == 200:
    data = response.json()
    print(f"Uploaded: {data['filename']}")
    print(f"Pages: {data['pages']}")
    print(f"Chunks: {data['chunks']}")
```

**Frontend Usage:**
```python
from api import APIClient

file_bytes = uploaded_file.getvalue()
result = APIClient.upload_document(file_bytes, filename)

if result and result.get("status") == "success":
    st.success(f"Uploaded: {result['filename']}")
else:
    st.error("Upload failed")
```

---

### 5. List Documents

Get list of uploaded documents.

**Request:**
```http
GET /documents
```

**Response (200 OK):**
```json
{
    "documents": [
        {
            "filename": "introduction.pdf",
            "pages": 20,
            "chunks": 80
        },
        {
            "filename": "advanced_topics.pdf",
            "pages": 35,
            "chunks": 140
        }
    ]
}
```

**Example (Python):**
```python
response = requests.get("http://localhost:8000/documents")

if response.status_code == 200:
    data = response.json()
    for doc in data["documents"]:
        print(f"{doc['filename']}: {doc['pages']} pages, {doc['chunks']} chunks")
```

**Frontend Usage:**
```python
from api import APIClient

documents = APIClient.get_documents()
if documents:
    for doc in documents["documents"]:
        st.write(f"📄 {doc['filename']} ({doc['pages']} pages)")
```

---

### 6. Get Document Details

Get detailed metadata for a specific document.

**Request:**
```http
GET /documents/{filename}
```

**Parameters:**
- `filename` (string, required): Document filename

**Response (200 OK):**
```json
{
    "filename": "introduction.pdf",
    "pages": 20,
    "chunks": 80,
    "upload_date": "2024-01-15T10:30:00Z",
    "file_size_mb": 5.2,
    "status": "indexed"
}
```

**Example (Python):**
```python
response = requests.get(
    "http://localhost:8000/documents/introduction.pdf"
)

if response.status_code == 200:
    doc = response.json()
    print(f"Filename: {doc['filename']}")
    print(f"Pages: {doc['pages']}")
    print(f"Chunks: {doc['chunks']}")
```

**Frontend Usage:**
```python
from api import APIClient

details = APIClient.get_document_detail("my_document.pdf")
if details:
    st.json(details)
```

---

### 7. Delete Document

Delete a document and remove it from indexing.

**Request:**
```http
DELETE /documents/{filename}
```

**Parameters:**
- `filename` (string, required): Document filename

**Response (200 OK):**
```json
{
    "status": "success",
    "deleted_chunks": 80
}
```

**Example (Python):**
```python
response = requests.delete(
    "http://localhost:8000/documents/old_document.pdf"
)

if response.status_code == 200:
    data = response.json()
    print(f"Deleted {data['deleted_chunks']} chunks")
```

**Frontend Usage:**
```python
from api import APIClient

success = APIClient.delete_document("my_document.pdf")
if success:
    st.success("Document deleted")
else:
    st.error("Deletion failed")
```

---

## Error Handling

### Common Status Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 200 | Success | Process normally |
| 400 | Bad Request | Check request format |
| 404 | Not Found | Verify filename/ID exists |
| 413 | File Too Large | Reduce file size |
| 500 | Server Error | Check backend logs |
| 503 | Service Unavailable | Backend is down |

### Error Response Format

```json
{
    "detail": "Error message describing what went wrong"
}
```

### Handling Errors in Frontend

```python
import requests
import streamlit as st

try:
    response = requests.post(
        "http://localhost:8000/chat",
        json=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        # Process success response
        data = response.json()
    elif response.status_code == 400:
        st.error("Invalid request format")
    elif response.status_code == 404:
        st.error("Resource not found")
    elif response.status_code == 500:
        st.error("Server error - please try again")
    else:
        st.error(f"Error {response.status_code}")
        
except requests.exceptions.Timeout:
    st.error("Request timed out - server is slow")
except requests.exceptions.ConnectionError:
    st.error("Cannot connect to backend")
except Exception as e:
    st.error(f"Unexpected error: {str(e)}")
```

## Session Management

### Session ID

Each user gets a unique session ID to maintain conversation history:

```python
import uuid

# Generate unique session ID
session_id = str(uuid.uuid4())

# Use in all API calls
payload = {
    "question": "...",
    "session_id": session_id
}
```

### Session Persistence

Sessions are maintained by the backend. Frontend stores session ID in:

```python
import streamlit as st

# Store in session state
st.session_state.session_id = session_id

# Retrieve for API calls
session_id = st.session_state.session_id
```

## Rate Limiting (Future)

Currently no rate limiting. In production, implement:

```python
# Expected rate limits
- Chat: 10 requests/minute per session
- Upload: 1 request/minute per session
- List documents: 30 requests/minute
```

Handle 429 (Too Many Requests):

```python
if response.status_code == 429:
    retry_after = int(response.headers.get('Retry-After', 60))
    st.warning(f"Rate limited. Retry after {retry_after}s")
```

## Timeouts

**Recommended Timeouts:**

```python
# Chat endpoints
CHAT_TIMEOUT = 30  # seconds

# Streaming endpoints
STREAM_TIMEOUT = 60  # seconds

# Upload endpoints
UPLOAD_TIMEOUT = 30  # seconds (may need increase for large files)
```

## Batch Operations

The API doesn't support batch operations yet. Process sequentially:

```python
documents = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]

for doc in documents:
    result = upload_document(doc)
    if not result:
        st.error(f"Failed to upload {doc}")
        break
```

## API Monitoring

### Health Check Interval

```python
import streamlit as st
import time

# Check backend health every 30 seconds
if "last_health_check" not in st.session_state:
    st.session_state.last_health_check = time.time()

if time.time() - st.session_state.last_health_check > 30:
    online = APIClient.check_health()
    st.session_state.backend_online = online
    st.session_state.last_health_check = time.time()
```

### Logging API Calls

```python
import logging

logger = logging.getLogger(__name__)

def log_api_call(endpoint, method, status_code, duration):
    logger.info(
        f"API: {method} {endpoint} - "
        f"Status: {status_code} - "
        f"Duration: {duration}ms"
    )
```

## CORS Configuration

If frontend and backend are on different domains, enable CORS:

**Backend (FastAPI):**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## API Versioning

Current API version: **v1**

Future versions will use path versioning:
```
/v1/chat
/v2/chat
```

For now, no version prefix is used.

## Testing the API

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# List documents
curl http://localhost:8000/documents

# Send chat message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is AI?",
    "session_id": "test-session-id"
  }'

# Upload document
curl -X POST http://localhost:8000/upload \
  -F "file=@document.pdf"
```

### Using Python Requests

```python
import requests

# Create session
session = requests.Session()
session.headers.update({
    'User-Agent': 'AskMyDocs-Frontend/1.0'
})

# Make requests
response = session.get("http://localhost:8000/documents")
print(response.json())
```

### Using Postman

1. Import API collection (future)
2. Set base URL: `{{backend_url}}`
3. Create variables for authentication (future)
4. Test each endpoint

## Troubleshooting API Issues

### 400 Bad Request

**Cause:** Invalid JSON format

**Fix:** Verify request body format

```python
import json

payload = {
    "question": "...",
    "session_id": "..."
}

# Validate JSON
json.dumps(payload)  # Should not raise

# Send
requests.post(url, json=payload)
```

### 500 Internal Server Error

**Cause:** Backend error

**Check:**
1. Backend is running
2. Database connection is active
3. Backend logs for errors
4. Request payload is valid

### Timeout Errors

**Cause:** Backend is slow or unresponsive

**Fix:**
- Increase timeout
- Check backend load
- Verify network connection
- Check for large file processing

---

## API Response Times

**Typical Response Times:**

| Endpoint | Time |
|----------|------|
| Health check | < 100ms |
| List documents | < 200ms |
| Chat (small answer) | 2-5 seconds |
| Chat (large answer) | 5-15 seconds |
| Upload (10MB) | 10-30 seconds |
| Delete | < 500ms |

## Future API Enhancements

Planned for future versions:

- [ ] Authentication (JWT/API keys)
- [ ] Rate limiting per user
- [ ] Batch operations
- [ ] Advanced search filters
- [ ] Webhook support
- [ ] GraphQL endpoint
- [ ] Caching layer
- [ ] Analytics endpoint

---

**For questions about the API, check the backend documentation or open an issue.**
