"""
AskMyDocs - Frontend Streamlit Application
RAG-powered document Q&A interface with Gemini, ChromaDB, and BM25
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import PAGE_CONFIG, THEME_COLORS
from components.header import render_header
from components.sidebar import render_sidebar
from components.chat import render_chat
from components.upload import render_upload
from components.documents import render_documents
from utils.session import initialize_session


def main():
    """Main application entry point."""
    # Configure page
    st.set_page_config(**PAGE_CONFIG)
    
    # Initialize session state
    initialize_session()
    
    # Load custom CSS
    load_custom_css()
    
    # Render header
    render_header()
    
    # Create two-column layout
    with st.container():
        col1, col2 = st.columns([1, 3.5], gap="medium")
        
        with col1:
            render_sidebar()
        
        with col2:
            render_chat()


def load_custom_css():
    """Load custom CSS styling."""
    css_file = Path(__file__).parent / "style.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # Fallback minimal styling
        st.markdown("""
        <style>
            .stMainBlockContainer {
                padding: 0;
            }
            .stContainer {
                padding: 0;
            }
        </style>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
