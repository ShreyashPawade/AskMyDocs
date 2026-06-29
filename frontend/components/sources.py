"""
Sources component for AskMyDocs.
Displays citation sources and document references.
"""

import streamlit as st
from typing import List, Dict, Any, Optional


def render_sources(sources: Optional[List[Dict[str, Any]]]) -> None:
    """
    Render the sources/citations section.
    
    Args:
        sources: List of source dicts with chunk_id, source, page
    """
    if not sources or len(sources) == 0:
        return
    
    # Sources header
    st.markdown(
        """
        <div class="sources-container">
            <div class="sources-header">📚 Sources</div>
        """,
        unsafe_allow_html=True
    )
    
    # Render each source
    for source in sources:
        render_source_item(source)
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_source_item(source: Dict[str, Any]) -> None:
    """
    Render a single source item.
    
    Args:
        source: Source dict with chunk_id, source, page
    """
    filename = source.get("source", "Unknown")
    page = source.get("page", "?")
    chunk_id = source.get("chunk_id", "?")
    
    st.markdown(
        f"""
        <div class="source-item">
            <span class="source-icon">📄</span>
            <div class="source-info">
                <div class="source-filename">{filename}</div>
                <div class="source-page">Page {page} • Chunk {chunk_id}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
