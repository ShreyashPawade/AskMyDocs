"""
Documents component for AskMyDocs.
Displays uploaded documents and provides management options.
"""

import streamlit as st
from typing import Optional, Dict, Any
from config import DISPLAY_STRINGS
from api import APIClient
from utils.session import (
    get_documents as get_session_documents,
    set_documents,
    remove_document as remove_from_session
)
from utils.helpers import log_info, log_error


def render_documents() -> None:
    """Render the documents list component."""
    
    # Refresh documents list on load
    refresh_documents()
    
    # Get documents from session
    documents = get_session_documents()
    
    # Show empty state if no documents
    if not documents:
        st.info(
            f"📄 {DISPLAY_STRINGS['no_documents']}\n\n"
            f"{DISPLAY_STRINGS['upload_hint']}"
        )
        return
    
    # Show document count
    st.caption(f"📚 {len(documents)} document{'s' if len(documents) != 1 else ''} indexed")
    
    # Render each document
    for doc in documents:
        render_document_card(doc)
    
    # Refresh button
    if st.button("🔄 Refresh", key="refresh_documents", use_container_width=True):
        refresh_documents()
        st.rerun()


def render_document_card(document: Dict[str, Any]) -> None:
    """
    Render a single document card.
    
    Args:
        document: Document dict with filename, pages, chunks
    """
    filename = document.get("filename", "Unknown")
    pages = document.get("pages", 0)
    chunks = document.get("chunks", 0)
    
    # Create expandable card
    with st.expander(f"📄 {filename}", expanded=False):
        # Document metadata
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Pages", pages)
        
        with col2:
            st.metric("Chunks", chunks)
        
        # Action buttons
        col1, col2, col3 = st.columns(3, gap="small")
        
        with col1:
            if st.button(
                "👁️ View Details",
                key=f"view_{filename}",
                use_container_width=True,
                help=DISPLAY_STRINGS['click_to_view']
            ):
                show_document_details(filename)
        
        with col2:
            if st.button(
                "📋 Copy Info",
                key=f"copy_{filename}",
                use_container_width=True
            ):
                info_text = f"Filename: {filename}\nPages: {pages}\nChunks: {chunks}"
                st.code(info_text, language="text")
        
        with col3:
            if st.button(
                "🗑️ Delete",
                key=f"delete_{filename}",
                use_container_width=True,
                help=DISPLAY_STRINGS['click_to_delete']
            ):
                delete_document(filename)
                st.rerun()


def show_document_details(filename: str) -> None:
    """
    Show detailed metadata for a document.
    
    Args:
        filename: Document filename
    """
    with st.spinner("📋 Loading document details..."):
        details = APIClient.get_document_detail(filename)
        
        if details:
            st.json(details)
        else:
            st.warning(f"Could not load details for {filename}")


def delete_document(filename: str) -> None:
    """
    Delete a document from the backend and update session.
    
    Args:
        filename: Document filename to delete
    """
    with st.spinner(f"🗑️ Deleting {filename}..."):
        success = APIClient.delete_document(filename)
        
        if success:
            # Remove from session
            remove_from_session(filename)
            st.success(f"✅ {filename} deleted successfully!")
            log_info(f"Document deleted: {filename}")
        else:
            st.error(f"❌ Failed to delete {filename}")
            log_error(f"Failed to delete document: {filename}")


def refresh_documents() -> None:
    """Refresh documents list from backend."""
    result = APIClient.get_documents()
    
    if result and "documents" in result:
        set_documents(result["documents"])
        log_info(f"Documents refreshed: {len(result['documents'])} documents")
    else:
        log_error("Failed to refresh documents")
