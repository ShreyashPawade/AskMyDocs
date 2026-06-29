"""
Sidebar component for AskMyDocs.
Handles PDF upload, document list, and document management.
"""

import streamlit as st
from config import DISPLAY_STRINGS
from components.upload import render_upload
from components.documents import render_documents


def render_sidebar() -> None:
    """Render the sidebar with upload and document management."""
    
    with st.container():
        # Upload Section
        st.markdown("### 📤 Upload PDF")
        render_upload()
        
        st.divider()
        
        # Documents Section
        st.markdown("### 📚 Documents")
        render_documents()
