# AskMyDocs Frontend - Development Guide

## Overview

This document provides guidance for developers working on the AskMyDocs frontend.

## Architecture

### Component Structure

The application follows a modular component architecture:

```
streamlit_app.py (Main entry point)
    ├── render_header()       - App header with status
    ├── render_sidebar()      - Sidebar container
    │   ├── render_upload()   - PDF upload component
    │   └── render_documents()- Document list
    └── render_chat()         - Chat interface
        ├── render_chat_messages()
        ├── render_single_message()
        └── render_chat_input()
```

### Data Flow

```
User Input (Chat/Upload)
    ↓
API Client (api.py)
    ↓
Backend API
    ↓
Response Processing
    ↓
Session State Update (utils/session.py)
    ↓
Component Re-render
```

## Development Workflow

### 1. Setting Up Development Environment

```bash
# Clone repository
git clone <repo-url>
cd frontend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies with dev tools
pip install -r requirements.txt
pip install pytest pytest-cov pylint black

# Setup pre-commit hooks
# (Future: Add .pre-commit-config.yaml)
```

### 2. Code Style

**Follow PEP8 Standard:**

```bash
# Format code with Black
black streamlit_app.py components/ utils/

# Check style with Pylint
pylint components/

# Sort imports
isort --profile black streamlit_app.py components/ utils/
```

**Naming Conventions:**

- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Private methods: `_prefix_method_name`
- Components: `render_component_name`

**Documentation:**

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Short description of function.
    
    Longer description if needed, explaining behavior,
    edge cases, and important notes.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When specific condition occurs
    """
    pass
```

### 3. Adding New Features

**Step 1: Create Component**

```python
# components/new_feature.py
"""New feature component for AskMyDocs."""

def render_new_feature() -> None:
    """Render the new feature component."""
    pass
```

**Step 2: Update Config**

```python
# config.py - Add configuration if needed
NEW_FEATURE_CONFIG = {
    "option1": value1,
    "option2": value2,
}
```

**Step 3: Integrate**

```python
# streamlit_app.py or relevant component
from components.new_feature import render_new_feature

# Use in main layout
render_new_feature()
```

**Step 4: Style**

```css
/* style.css - Add styling */
.new-feature-container {
  background-color: var(--bg-tertiary);
  border-radius: var(--border-radius);
  padding: 16px;
}
```

### 4. Session State Management

**Always use session helper functions:**

```python
from utils.session import (
    add_message,
    get_messages,
    set_chat_loading,
    get_backend_status,
)

# Add message
add_message("user", "Hello")

# Get messages
messages = get_messages()

# Check loading state
if get_chat_loading():
    st.spinner("Loading...")
```

**Don't directly modify st.session_state:**

```python
# ❌ Wrong
st.session_state.messages.append(msg)

# ✅ Correct
add_message("user", content)
```

### 5. API Communication

**Use centralized APIClient:**

```python
from api import APIClient

# Chat
response = APIClient.send_chat_message(question, session_id)

# Upload
result = APIClient.upload_document(file_bytes, filename)

# Always handle None responses
if response:
    process_response(response)
else:
    st.error("Request failed")
```

**Error Handling Pattern:**

```python
try:
    result = APIClient.some_method()
    if result:
        # Process result
        pass
    else:
        # Handle API error
        st.error("Error message")
except Exception as e:
    log_error(f"Error: {str(e)}")
    st.error("Unexpected error occurred")
```

### 6. Testing

**Test Components:**

```python
# tests/test_components.py
import streamlit as st
from components.chat import render_chat_messages

def test_chat_messages():
    """Test chat message rendering."""
    st.session_state.messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"}
    ]
    
    # Component should not raise error
    render_chat_messages()
```

**Test Helpers:**

```python
# tests/test_helpers.py
from utils.helpers import get_confidence_level

def test_confidence_levels():
    """Test confidence level calculation."""
    assert get_confidence_level(4.5) == "High"
    assert get_confidence_level(3.0) == "Medium"
    assert get_confidence_level(1.0) == "Low"
```

**Run Tests:**

```bash
pytest tests/ -v
pytest tests/ --cov=. --cov-report=html
```

## Debugging

### Enable Debug Logging

```bash
streamlit run streamlit_app.py --logger.level=debug
```

### View Logs

```bash
# On Linux/Mac
streamlit logs

# Check specific log file
tail -f ~/.streamlit/logs/2024-*.log
```

### Debug Session State

```python
# Add to any component to inspect state
with st.expander("🔧 Debug Info"):
    st.json({
        "session_id": st.session_state.session_id,
        "messages_count": len(st.session_state.messages),
        "documents_count": len(st.session_state.documents),
        "backend_online": st.session_state.backend_online,
    })
```

### Debug API Calls

```python
# api.py - Add logging
import logging

logger = logging.getLogger(__name__)

@staticmethod
def send_chat_message(question: str, session_id: str):
    logger.debug(f"Sending: {question}")
    logger.debug(f"Session: {session_id}")
    
    response = requests.post(...)
    logger.debug(f"Response: {response.status_code}")
    
    return response
```

## Performance Optimization

### 1. Reduce Re-renders

```python
# ✅ Use keys to prevent re-rendering
for doc in documents:
    st.write(doc, key=f"doc_{doc['filename']}")

# ❌ Avoid unnecessary state changes
st.session_state.temp_var = value  # Causes rerun
```

### 2. Cache Expensive Operations

```python
from functools import lru_cache

@lru_cache(maxsize=32)
def get_confidence_level(confidence: float) -> str:
    # Cached result
    return "High" if confidence >= 4.0 else "Medium"
```

### 3. Optimize Messages Display

```python
# ✅ Only render visible messages
visible_messages = st.session_state.messages[-20:]  # Last 20
for msg in visible_messages:
    render_single_message(msg)

# ❌ Don't render all if many
for msg in all_messages:  # Slow with 1000+ messages
    render_single_message(msg)
```

### 4. Use Columns Layout

```python
# ✅ Efficient layout
col1, col2, col3 = st.columns(3)
with col1: st.write("A")
with col2: st.write("B")
with col3: st.write("C")

# ❌ Less efficient
st.write("A")
st.write("B")
st.write("C")
```

## Common Patterns

### Pattern 1: Form Submission

```python
with st.form("my_form"):
    name = st.text_input("Name")
    submit = st.form_submit_button("Submit")
    
    if submit:
        # Process form
        process_input(name)
        st.success("Done!")
```

### Pattern 2: Loading States

```python
if processing:
    with st.spinner("Processing..."):
        result = do_work()
        st.success("Complete!")
else:
    st.button("Start")
```

### Pattern 3: Expandable Sections

```python
with st.expander("Advanced Options"):
    option1 = st.checkbox("Option 1")
    option2 = st.slider("Option 2", 0, 100)
    
    if option1:
        # Show dependent content
        st.write("Option 1 is enabled")
```

### Pattern 4: Error Handling

```python
try:
    result = api_call()
    if result:
        st.success("Success!")
    else:
        st.warning("No results found")
except ValueError as e:
    st.error(f"Invalid input: {e}")
except Exception as e:
    log_error(f"Unexpected error: {e}")
    st.error("Something went wrong. Please try again.")
```

## Deployment

### Local Development

```bash
streamlit run streamlit_app.py
```

### Testing Deployment

```bash
# Simulate production environment
streamlit run streamlit_app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true \
  --logger.level warning
```

### Docker Deployment

```bash
# Build image
docker build -t askmydocs-frontend .

# Run container
docker run -p 8501:8501 \
  -e BACKEND_URL=http://backend:8000 \
  askmydocs-frontend
```

## Troubleshooting

### Issue: Changes Don't Appear

**Solution:** Clear Streamlit cache

```bash
# Clear all cache
rm -rf ~/.streamlit/
streamlit run streamlit_app.py --logger.level=debug
```

### Issue: Session State Not Persisting

**Solution:** Use proper session initialization

```python
# Always initialize session early
from utils.session import initialize_session

initialize_session()  # Must be called first
```

### Issue: API Calls Failing

**Solution:** Check backend connectivity

```python
# Test backend
import requests
try:
    r = requests.get("http://localhost:8000/health")
    print(r.json())
except:
    print("Backend not reachable")
```

## Code Review Checklist

Before submitting PR:

- [ ] Code follows PEP8 style guide
- [ ] All functions have docstrings
- [ ] Error handling is comprehensive
- [ ] Type hints are used
- [ ] No hardcoded values (use config.py)
- [ ] Features are properly documented
- [ ] Tests are included
- [ ] No sensitive data in code
- [ ] Performance is acceptable
- [ ] UI is responsive

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python PEP8 Guide](https://www.python.org/dev/peps/pep-0008/)
- [Requests Library](https://requests.readthedocs.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## Getting Help

1. Check existing issues/PRs
2. Review documentation
3. Check logs with debug mode
4. Test with minimal example
5. Open issue with details
