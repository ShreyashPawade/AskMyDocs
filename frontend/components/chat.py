"""
Chat component for AskMyDocs.
Main chat interface with message display and input handling.
"""

import streamlit as st
from typing import Optional, List, Dict, Any
from config import DISPLAY_STRINGS, THEME_COLORS
from api import APIClient
from components.confidence import render_confidence_badge
from components.sources import render_sources
from utils.session import (
    get_session_id,
    add_message,
    get_messages,
    set_chat_loading,
    get_chat_loading,
    has_documents
)
from utils.helpers import format_markdown_response, log_info


def render_chat() -> None:
    """Render the main chat interface."""
    
    # Check if backend is online
    if not APIClient.check_health():
        st.error(
            "❌ Backend is offline. Please ensure the FastAPI server is running "
            "at the configured URL."
        )
        return
    
    # Check if documents are uploaded
    if not has_documents():
        st.info(
            "📄 No documents uploaded yet.\n\n"
            "Please upload a PDF document using the sidebar to get started. "
            "Once indexed, you can ask questions about its contents."
        )
        return
    
    # Render chat messages
    render_chat_messages()
    
    # Render chat input
    render_chat_input()


def render_chat_messages() -> None:
    """Render all chat messages."""
    
    messages = get_messages()
    
    if not messages:
        # Empty state
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-state-icon">💬</div>
                <div class="empty-state-text">
                    Start a conversation<br/>
                    <small style="color: var(--text-tertiary);">
                        Ask anything about your documents
                    </small>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return
    
    # Create message container
    message_container = st.container()
    
    with message_container:
        for i, message in enumerate(messages):
            render_single_message(message, i)


def render_single_message(message: Dict[str, Any], message_index: int) -> None:
    """
    Render a single message.
    
    Args:
        message: Message dict with role and content
        message_index: Index for unique keys
    """
    role = message.get("role", "assistant")
    content = message.get("content", "")
    
    # Determine bubble style
    bubble_class = "user" if role == "user" else "assistant"
    
    # Render message bubble
    message_html = f"""
    <div class="message {bubble_class}">
        <div class="message-bubble {bubble_class}">
    """
    
    if role == "assistant":
        # Parse assistant message for confidence and sources
        lines = content.split('\n')
        main_content = []
        confidence = None
        sources = None
        
        for line in lines:
            if line.startswith("CONFIDENCE:"):
                try:
                    confidence = float(line.replace("CONFIDENCE:", "").strip())
                except:
                    pass
            elif line.startswith("SOURCES:"):
                # Parse sources JSON
                try:
                    import json
                    sources_str = line.replace("SOURCES:", "").strip()
                    sources = json.loads(sources_str)
                except:
                    pass
            else:
                main_content.append(line)
        
        message_content = '\n'.join(main_content).strip()
        
        # Render main content with markdown
        st.markdown(
            message_html,
            unsafe_allow_html=True
        )
        st.markdown(message_content)
        
        # Render confidence if present
        if confidence is not None:
            render_confidence_badge(confidence)
        
        # Render sources if present
        if sources:
            render_sources(sources)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    else:
        # User message - simple rendering
        message_html += format_markdown_response(content)
        message_html += "</div></div>"
        st.markdown(message_html, unsafe_allow_html=True)


def render_chat_input() -> None:
    """Render the chat input area."""
    
    # Chat input
    user_input = st.chat_input(
        placeholder=DISPLAY_STRINGS['ask_anything'],
        key="chat_input"
    )
    
    if user_input:
        # Check if already loading
        if get_chat_loading():
            st.warning("⏳ Previous message still processing...")
            return
        
        # Add user message
        add_message("user", user_input)
        
        # Set loading state
        set_chat_loading(True)
        
        # Get session ID
        session_id = get_session_id()
        
        # Send to backend
        with st.spinner(DISPLAY_STRINGS['loading']):
            response = send_chat_message(user_input, session_id)
        
        # Set loading state
        set_chat_loading(False)
        
        # Process response
        if response:
            format_and_store_response(response)
        
        # Rerun to show new messages
        st.rerun()


def send_chat_message(question: str, session_id: str) -> Optional[Dict[str, Any]]:
    """
    Send a chat message to the backend.
    
    Args:
        question: User question
        session_id: Session ID
    
    Returns:
        Response dict or None if error
    """
    log_info(f"Sending message: {question[:50]}...")
    
    result = APIClient.send_chat_message(question, session_id)
    
    if result:
        log_info("Message sent successfully")
    else:
        log_info("Message send failed")
    
    return result


def format_and_store_response(response: Dict[str, Any]) -> None:
    """
    Format and store the assistant response.
    
    Args:
        response: Response dict from backend
    """
    answer = response.get("answer", "No response")
    confidence = response.get("confidence")
    sources = response.get("sources", [])
    
    # Format response content
    content = answer
    
    if confidence is not None:
        content += f"\n\nCONFIDENCE:{confidence}"
    
    if sources:
        import json
        content += f"\n\nSOURCES:{json.dumps(sources)}"
    
    # Store in session
    add_message("assistant", content)
    log_info("Response stored in chat history")
