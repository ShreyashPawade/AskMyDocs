# AskMyDocs - Streamlit Frontend

A professional, production-ready Streamlit frontend for the AskMyDocs RAG (Retrieval-Augmented Generation) application. This application provides a ChatGPT-like interface for querying documents using hybrid search with Gemini, ChromaDB, BM25, and cross-encoder reranking.

## Features

✨ **Core Features**
- 💬 ChatGPT-like interface with dark professional theme
- 📄 PDF document upload and management
- 🔍 Hybrid search (Vector + BM25 + RRF)
- 🤖 Gemini 2.5 Flash LLM integration
- 📚 ChromaDB vector search
- ⭐ Confidence scores for responses
- 📖 Citation sources with page numbers
- 💾 Session conversation memory
- 🎨 Responsive dark theme UI
- ⚡ Auto-scroll and streaming support

## Technology Stack

- **Framework:** Streamlit
- **API Client:** Requests
- **Language:** Python 3.9+
- **Styling:** Custom CSS
- **Architecture:** Modular component-based design

## Project Structure

```
frontend/
├── streamlit_app.py          # Main application entry point
├── api.py                    # Backend API client
├── config.py                 # Configuration and constants
├── style.css                 # Custom CSS styling
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── README.md                 # This file
│
├── components/               # UI Components
│   ├── __init__.py
│   ├── header.py            # App header with status
│   ├── sidebar.py           # Sidebar container
│   ├── chat.py              # Chat interface
│   ├── upload.py            # PDF upload
│   ├── documents.py         # Document management
│   ├── confidence.py        # Confidence badge
│   └── sources.py           # Citation sources
│
└── utils/                    # Utility modules
    ├── __init__.py
    ├── session.py           # Session state management
    └── helpers.py           # Helper functions
```

## Prerequisites

- Python 3.9 or higher
- pip or conda
- Running AskMyDocs FastAPI backend (http://localhost:8000)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd frontend
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n askmydocs python=3.9
conda activate askmydocs
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env if backend URL is different
# BACKEND_URL=http://localhost:8000
```

## Running the Application

### Start the Frontend

```bash
streamlit run streamlit_app.py
```

The application will be available at `http://localhost:8501`

### With Custom Backend URL

```bash
BACKEND_URL=http://your-backend-url:8000 streamlit run streamlit_app.py
```

### Production Deployment

```bash
streamlit run streamlit_app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true
```

## Configuration

### Backend URL

Set the backend URL in `.env`:

```env
BACKEND_URL=http://localhost:8000
```

Or via environment variable:

```bash
export BACKEND_URL=http://your-backend:8000
```

### Streamlit Configuration

Edit `.streamlit/config.toml` for Streamlit-specific settings:

```toml
[theme]
primaryColor = "#6366F1"
backgroundColor = "#0F1419"
secondaryBackgroundColor = "#1A1F2E"
textColor = "#E8EEF7"
font = "sans serif"

[server]
maxUploadSize = 50
```

## API Endpoints Used

The frontend communicates with the following backend endpoints:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Check backend status |
| POST | `/chat` | Send message, get response |
| POST | `/chat_stream` | Stream response tokens |
| POST | `/upload` | Upload PDF document |
| GET | `/documents` | Get list of documents |
| GET | `/documents/{filename}` | Get document metadata |
| DELETE | `/documents/{filename}` | Delete document |

## Usage Guide

### 1. **Upload Documents**

1. Navigate to the **Upload PDF** section in the sidebar
2. Click "Browse files" and select a PDF
3. Click "Upload" button
4. Wait for indexing to complete
5. Document appears in the document list

### 2. **Ask Questions**

1. Type your question in the chat input
2. Press Enter or click send
3. AI processes and returns answer with confidence score
4. View source citations below the answer

### 3. **Manage Documents**

- **View Details:** Expand document card → Click "View Details"
- **Delete:** Expand document card → Click "Delete"
- **Refresh:** Click the refresh button to sync with backend

### 4. **Monitor Backend Status**

- Green indicator = Backend online
- Red indicator = Backend offline
- Check your backend URL in `.env` if offline

## Features Guide

### Chat Interface

- **User Messages:** Right-aligned indigo bubbles
- **Assistant Messages:** Left-aligned dark bubbles with markdown support
- **Streaming:** Responses update in real-time as tokens arrive
- **History:** All messages persist in session memory

### Confidence Scores

- **High (Green):** ≥ 4.0 - Very confident answer
- **Medium (Yellow):** ≥ 2.0 - Reasonably confident
- **Low (Red):** < 2.0 - Low confidence, verify answer

### Source Citations

- Shows PDF filename
- Displays page number
- References chunk ID for traceability
- Clickable for future enhancement

### Document Management

- Upload status with metadata (pages, chunks)
- Automatic indexing and chunking
- Delete with confirmation
- View detailed metadata
- Real-time document count

## Error Handling

The application handles various error scenarios:

### Network Errors
```
❌ Network Error: Cannot reach backend
```
**Solution:** Ensure FastAPI backend is running and `BACKEND_URL` is correct

### Backend Offline
```
❌ Backend is offline. Please ensure the FastAPI server is running...
```
**Solution:** Start the backend server and verify connection

### Upload Failures
```
❌ Upload Failed: [error details]
```
**Solution:** Check file size, format, and backend permissions

### No Documents
```
📄 No documents uploaded yet.
```
**Solution:** Upload a PDF to start asking questions

## Performance Tips

1. **Smaller PDFs:** Upload PDFs < 50MB for faster processing
2. **Specific Questions:** Ask detailed questions for better results
3. **Refresh on Issues:** Use refresh button if documents don't appear
4. **Clear History:** Use "Reset Session" to clear old messages

## Troubleshooting

### Application Won't Start

```bash
# Check Python version
python --version

# Verify dependencies
pip install -r requirements.txt --upgrade

# Run with verbose output
streamlit run streamlit_app.py --logger.level=debug
```

### Backend Connection Issues

```bash
# Test backend connectivity
curl http://localhost:8000/health

# Check firewall/network
netstat -an | grep 8000  # On Linux/Mac
netstat -ano | grep 8000  # On Windows
```

### Slow Performance

1. Check backend server load
2. Reduce PDF file sizes
3. Clear browser cache
4. Restart Streamlit app

### Messages Not Persisting

- Clear browser cache
- Check session state in Streamlit
- Verify backend is saving session data

## Development

### Code Structure

**Components:** Modular Streamlit components following single-responsibility principle

**API Client:** Centralized API communication with error handling

**Session Management:** Persistent session state across reruns

**Helpers:** Reusable utility functions for common operations

### Adding New Features

1. Create component in `components/`
2. Add configuration to `config.py`
3. Implement with proper error handling
4. Update `style.css` for styling
5. Add tests if applicable

### Running Tests

```bash
# Future: Add pytest configuration
pytest tests/
```

## Deployment

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV BACKEND_URL=http://backend:8000
EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://backend:8000
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
```

### Heroku

```bash
# Create Procfile
echo "web: streamlit run streamlit_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
git push heroku main
```

### AWS

```bash
# Using Streamlit Cloud
# Push to GitHub and connect repository at https://share.streamlit.io
```

## Performance Monitoring

The application logs important events:

```bash
# View logs
streamlit logs

# Enable debug mode
streamlit run streamlit_app.py --logger.level=debug
```

## Security

⚠️ **Important Notes:**

1. Never commit `.env` file with secrets
2. Use HTTPS in production
3. Validate all user inputs
4. Keep dependencies updated
5. Use environment variables for sensitive config

## Contributing

1. Follow PEP8 style guide
2. Add docstrings to functions
3. Test with different PDFs
4. Update documentation
5. Submit pull requests

## License

This project is part of the AskMyDocs application.

## Support

For issues or questions:

1. Check the troubleshooting section
2. Review backend API documentation
3. Check Streamlit documentation
4. Open an issue on the repository

## Roadmap

- [ ] Streaming responses with token-by-token display
- [ ] Conversation export (PDF/JSON)
- [ ] Advanced search filters
- [ ] Document similarity search
- [ ] Custom LLM model selection
- [ ] Rate limiting and quotas
- [ ] Multi-user support
- [ ] Dark/Light theme toggle
- [ ] Internationalization (i18n)
- [ ] Mobile app version

## Changelog

### v1.0.0 (Initial Release)

- Core chat interface
- PDF upload and management
- Document querying
- Confidence scores
- Source citations
- Session memory
- Dark professional theme
- Comprehensive error handling

---

**Built with ❤️ for document intelligence**

For more information about AskMyDocs, visit the main repository.
