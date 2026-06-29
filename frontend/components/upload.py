"""
Upload component for AskMyDocs.
Handles PDF file uploads and backend integration.
"""

import streamlit as st
from config import DISPLAY_STRINGS, UPLOAD_CONFIG
from api import APIClient
from utils.session import add_document, get_documents as get_session_documents
from utils.helpers import log_info, log_error


def render_upload() -> None:
    """Render the file upload component."""
    
    # File uploader
    uploaded_file = st.file_uploader(
        label="Choose a PDF file",
        type=["pdf"],
        key="pdf_uploader",
        help="Upload a PDF document to index and search"
    )
    
    if uploaded_file is not None:
        # Show file info
        file_size_mb = uploaded_file.size / (1024 * 1024)
        
        if file_size_mb > UPLOAD_CONFIG["max_file_size_mb"]:
            st.error(
                f"File too large! Maximum size is {UPLOAD_CONFIG['max_file_size_mb']}MB. "
                f"Your file is {file_size_mb:.1f}MB."
            )
            return
        
        # Upload button and progress
        if st.button("Upload", key="upload_button", use_container_width=True):
            with st.spinner("📤 Uploading and indexing document..."):
                file_bytes = uploaded_file.getvalue()
                result = APIClient.upload_document(file_bytes, uploaded_file.name)
                
                if result and result.get("status") == "success":
                    # Add to session state
                    document_info = {
                        "filename": result.get("filename"),
                        "pages": result.get("pages"),
                        "chunks": result.get("chunks")
                    }
                    add_document(document_info)
                    
                    # Show success message
                    st.success(
                        f"✅ Document uploaded!\n\n"
                        f"**Filename:** {result.get('filename')}\n"
                        f"**Pages:** {result.get('pages')}\n"
                        f"**Chunks:** {result.get('chunks')}"
                    )
                    
                    log_info(f"Document uploaded: {uploaded_file.name}")
                else:
                    st.error(f"Upload failed. Please try again.")
                    log_error(f"Upload failed for {uploaded_file.name}")
