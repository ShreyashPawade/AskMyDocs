"""
Session management module for AskMyDocs frontend.
Handles session state, message history, and user preferences.
"""

import streamlit as st
import uuid
from typing import List, Dict, Any, Optional
from config import SESSION_DEFAULTS
from utils.helpers import log_info, validate_session_id


def initialize_session() -> None:
    """Initialize Streamlit session state with defaults."""
    
    # Initialize session ID
    if "session_id" not in st.session_state or st.session_state.session_id is None:
        st.session_state.session_id = str(uuid.uuid4())
        log_info(f"New session created: {st.session_state.session_id}")
    
    # Initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize documents list
    if "documents" not in st.session_state:
        st.session_state.documents = []
    
    # Initialize backend status
    if "backend_online" not in st.session_state:
        st.session_state.backend_online = True
    
    # Initialize chat loading state
    if "current_chat_loading" not in st.session_state:
        st.session_state.current_chat_loading = False
    
    # Initialize sidebar state
    if "show_upload" not in st.session_state:
        st.session_state.show_upload = False
    
    # Initialize document detail view
    if "viewing_document_detail" not in st.session_state:
        st.session_state.viewing_document_detail = None


def get_session_id() -> str:
    """
    Get the current session ID.
    
    Returns:
        Session ID string
    """
    if "session_id" not in st.session_state or not validate_session_id(st.session_state.session_id):
        st.session_state.session_id = str(uuid.uuid4())
    
    return st.session_state.session_id


def add_message(role: str, content: str) -> None:
    """
    Add a message to the chat history.
    
    Args:
        role: Message role ("user" or "assistant")
        content: Message content
    """
    message = {
        "role": role,
        "content": content
    }
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    st.session_state.messages.append(message)
    log_info(f"Message added: {role} - {len(content)} chars")


def get_messages() -> List[Dict[str, str]]:
    """
    Get all messages from chat history.
    
    Returns:
        List of message dicts with "role" and "content"
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    return st.session_state.messages


def clear_messages() -> None:
    """Clear all messages from chat history."""
    st.session_state.messages = []
    log_info("Chat history cleared")


def get_last_user_message() -> Optional[str]:
    """
    Get the last user message.
    
    Returns:
        Last user message content, or None if no messages
    """
    messages = get_messages()
    for message in reversed(messages):
        if message["role"] == "user":
            return message["content"]
    return None


def set_backend_status(online: bool) -> None:
    """
    Set backend online/offline status.
    
    Args:
        online: True if online, False if offline
    """
    st.session_state.backend_online = online


def get_backend_status() -> bool:
    """
    Get backend online/offline status.
    
    Returns:
        True if online, False if offline
    """
    if "backend_online" not in st.session_state:
        st.session_state.backend_online = True
    
    return st.session_state.backend_online


def set_chat_loading(loading: bool) -> None:
    """
    Set chat loading state.
    
    Args:
        loading: True if loading, False otherwise
    """
    st.session_state.current_chat_loading = loading


def get_chat_loading() -> bool:
    """
    Get chat loading state.
    
    Returns:
        True if currently loading, False otherwise
    """
    if "current_chat_loading" not in st.session_state:
        st.session_state.current_chat_loading = False
    
    return st.session_state.current_chat_loading


def set_documents(documents: List[Dict[str, Any]]) -> None:
    """
    Update documents list.
    
    Args:
        documents: List of document dicts
    """
    st.session_state.documents = documents
    log_info(f"Documents list updated: {len(documents)} documents")


def get_documents() -> List[Dict[str, Any]]:
    """
    Get cached documents list.
    
    Returns:
        List of document dicts
    """
    if "documents" not in st.session_state:
        st.session_state.documents = []
    
    return st.session_state.documents


def add_document(document: Dict[str, Any]) -> None:
    """
    Add a document to the documents list.
    
    Args:
        document: Document dict with filename, pages, chunks
    """
    if "documents" not in st.session_state:
        st.session_state.documents = []
    
    # Avoid duplicates
    existing_filenames = [doc.get("filename") for doc in st.session_state.documents]
    if document.get("filename") not in existing_filenames:
        st.session_state.documents.append(document)
        log_info(f"Document added: {document.get('filename')}")


def remove_document(filename: str) -> None:
    """
    Remove a document from the documents list.
    
    Args:
        filename: Document filename to remove
    """
    if "documents" in st.session_state:
        st.session_state.documents = [
            doc for doc in st.session_state.documents
            if doc.get("filename") != filename
        ]
        log_info(f"Document removed: {filename}")


def clear_documents() -> None:
    """Clear all documents from list."""
    st.session_state.documents = []
    log_info("Documents list cleared")


def get_document_by_filename(filename: str) -> Optional[Dict[str, Any]]:
    """
    Get document details by filename.
    
    Args:
        filename: Document filename
    
    Returns:
        Document dict or None if not found
    """
    documents = get_documents()
    for doc in documents:
        if doc.get("filename") == filename:
            return doc
    return None


def get_message_count() -> int:
    """
    Get total number of messages in history.
    
    Returns:
        Message count
    """
    return len(get_messages())


def has_messages() -> bool:
    """
    Check if there are any messages.
    
    Returns:
        True if messages exist, False otherwise
    """
    return len(get_messages()) > 0


def has_documents() -> bool:
    """
    Check if any documents are uploaded.
    
    Returns:
        True if documents exist, False otherwise
    """
    return len(get_documents()) > 0


def get_conversation_summary() -> str:
    """
    Get a summary of the conversation.
    
    Returns:
        Summary string with message counts
    """
    messages = get_messages()
    user_count = sum(1 for m in messages if m["role"] == "user")
    assistant_count = sum(1 for m in messages if m["role"] == "assistant")
    
    return f"{user_count} questions, {assistant_count} answers"


def export_conversation() -> str:
    """
    Export conversation as formatted text.
    
    Returns:
        Formatted conversation string
    """
    messages = get_messages()
    lines = ["# AskMyDocs Conversation Export\n"]
    
    for message in messages:
        role = message["role"].upper()
        content = message["content"]
        lines.append(f"\n## {role}\n")
        lines.append(content)
    
    return "\n".join(lines)


def reset_session() -> None:
    """Reset all session state to defaults."""
    st.session_state.messages = []
    st.session_state.documents = []
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.backend_online = True
    st.session_state.current_chat_loading = False
    log_info("Session reset")
