# 🚀 Quick Start Guide

Get AskMyDocs frontend running in 5 minutes!

## Prerequisites

- Python 3.9+
- AskMyDocs backend running (http://localhost:8000)
- Git (optional)

## Option 1: Automated Setup (Recommended)

### macOS/Linux

```bash
# Clone or download the project
cd frontend

# Run setup script
chmod +x setup.sh
./setup.sh

# Start the application
streamlit run streamlit_app.py
```

### Windows

```bash
# Clone or download the project
cd frontend

# Run setup script
setup.bat

# Start the application
streamlit run streamlit_app.py
```

## Option 2: Manual Setup

### Step 1: Create Virtual Environment

```bash
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env  # macOS/Linux
copy .env.example .env  # Windows

# Edit .env if needed (default: http://localhost:8000)
```

### Step 4: Run Application

```bash
streamlit run streamlit_app.py
```

## ✅ Verification

1. **Check Backend is Running:**
   ```bash
   curl http://localhost:8000/health
   # Should return: {"status":"online"}
   ```

2. **Open Frontend:**
   - Navigate to: http://localhost:8501
   - Look for green "✅ Online" indicator in header

3. **Test Upload:**
   - Click "Upload PDF" in sidebar
   - Select any PDF file
   - Click "Upload"
   - Wait for indexing

4. **Test Chat:**
   - Type a question in the chat input
   - Press Enter
   - Verify response appears with confidence score

## 🔧 Troubleshooting

### Backend Offline Error

```
❌ Backend is offline
```

**Fix:**
```bash
# 1. Check if backend is running
curl http://localhost:8000/health

# 2. Update .env with correct URL
BACKEND_URL=http://your-backend-url:8000

# 3. Restart Streamlit
streamlit run streamlit_app.py
```

### Upload Button Disabled

**Cause:** No documents uploaded yet

**Fix:**
- Upload a PDF using the sidebar uploader
- Wait for indexing to complete

### No Response When Asking Questions

**Cause:** Backend processing

**Fix:**
- Wait longer (first query takes time)
- Check backend logs
- Verify backend has documents indexed

### Port Already in Use

```bash
# If port 8501 is in use:
streamlit run streamlit_app.py --server.port 8502
```

## 📚 Common Tasks

### Upload a Document

1. Click "Upload PDF" in sidebar
2. Choose a PDF file (max 50MB)
3. Click "Upload"
4. Wait for green success message

### Ask a Question

1. Type your question in chat input
2. Press Enter
3. View response with confidence score
4. Click expandable sections to see sources

### Delete a Document

1. Find document in sidebar list
2. Expand the document card
3. Click "Delete" button
4. Confirm deletion

### Clear Chat History

1. Press F5 to refresh page, OR
2. Use your browser's reload button

## 🔗 Environment Variables

```env
# Backend URL (default: http://localhost:8000)
BACKEND_URL=http://localhost:8000

# Optional: Streamlit configuration
STREAMLIT_CLIENT_TOOLBAR_MODE=minimal
```

## 📝 Next Steps

1. **Read Full Documentation:** See `README.md`
2. **Development Guide:** See `DEVELOPMENT.md`
3. **Customize Settings:** Edit `.env` and `.streamlit/config.toml`
4. **Deploy:** See deployment section in README

## 🎯 Key Features to Try

✨ **Hybrid Search** - Questions use vector + BM25 search
🤖 **Gemini AI** - Smart responses using Google's latest model
📊 **Confidence Scores** - See how confident the AI is
📖 **Source Citations** - Track which document pages were used
💾 **Session Memory** - Conversation history persists

## ⚡ Performance Tips

- **Smaller PDFs** - Upload < 50MB for faster processing
- **Specific Questions** - Ask detailed questions
- **Clear Answers** - AI works better with specific queries
- **Refresh Documents** - Use refresh button if issues occur

## 📞 Support

| Issue | Solution |
|-------|----------|
| Backend not found | Verify FastAPI is running on port 8000 |
| Upload fails | Check file size (max 50MB) and format (PDF only) |
| Slow responses | Try shorter questions, check backend load |
| Port in use | Run on different port: `--server.port 8502` |

## 🎓 Learning Resources

- **Streamlit Docs:** https://docs.streamlit.io/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Gemini API:** https://ai.google.dev/
- **ChromaDB:** https://docs.trychroma.com/

---

**Questions?** Check the full documentation in README.md or DEVELOPMENT.md
