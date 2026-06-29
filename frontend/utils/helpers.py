"""
Helper utilities for the AskMyDocs frontend.
Contains common functions for logging, formatting, and conversions.
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def log_error(message: str, exception: Optional[Exception] = None) -> None:
    """
    Log an error message.
    
    Args:
        message: Error message to log
        exception: Optional exception object
    """
    if exception:
        logger.error(f"{message} - {str(exception)}")
    else:
        logger.error(message)


def log_info(message: str) -> None:
    """
    Log an info message.
    
    Args:
        message: Info message to log
    """
    logger.info(message)


def format_file_size(size_bytes: int) -> str:
    """
    Format bytes to human-readable file size.
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted string (e.g., "2.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def get_confidence_level(confidence: float) -> str:
    """
    Get confidence level label from score.
    
    Args:
        confidence: Confidence score (0-5)
    
    Returns:
        Level string: "High", "Medium", or "Low"
    """
    if confidence >= 4.0:
        return "High"
    elif confidence >= 2.0:
        return "Medium"
    else:
        return "Low"


def get_confidence_color(confidence: float) -> str:
    """
    Get color for confidence badge.
    
    Args:
        confidence: Confidence score (0-5)
    
    Returns:
        Color name: "green", "yellow", or "red"
    """
    if confidence >= 4.0:
        return "🟢"
    elif confidence >= 2.0:
        return "🟡"
    else:
        return "🔴"


def format_timestamp(timestamp: Optional[float] = None) -> str:
    """
    Format timestamp to readable string.
    
    Args:
        timestamp: Unix timestamp (uses current time if None)
    
    Returns:
        Formatted string (e.g., "2:45 PM")
    """
    if timestamp is None:
        dt = datetime.now()
    else:
        dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%I:%M %p")


def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: Text to clean
    
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to maximum length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def highlight_text(text: str, query: str) -> str:
    """
    Highlight query terms in text.
    
    Args:
        text: Text to highlight
        query: Query terms
    
    Returns:
        Text with highlighted terms
    """
    for term in query.split():
        if term.lower() in text.lower():
            text = text.replace(
                term,
                f"**{term}**",
                1
            )
    return text


def validate_session_id(session_id: Optional[str]) -> bool:
    """
    Validate session ID format.
    
    Args:
        session_id: Session ID to validate
    
    Returns:
        True if valid, False otherwise
    """
    if session_id is None or not isinstance(session_id, str):
        return False
    if len(session_id) < 10:
        return False
    return True


def format_chat_message(role: str, content: str) -> Dict[str, str]:
    """
    Format a chat message.
    
    Args:
        role: Message role ("user" or "assistant")
        content: Message content
    
    Returns:
        Formatted message dict
    """
    return {
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }


def extract_json_from_response(response_text: str) -> Optional[Dict[str, Any]]:
    """
    Extract JSON from response text.
    
    Args:
        response_text: Response text potentially containing JSON
    
    Returns:
        Parsed JSON dict, or None if invalid
    """
    try:
        import json
        # Try to find JSON in the text
        if "{" in response_text and "}" in response_text:
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            json_str = response_text[start:end]
            return json.loads(json_str)
    except Exception as e:
        log_error(f"Failed to extract JSON: {str(e)}")
    
    return None


def get_file_extension(filename: str) -> str:
    """
    Get file extension from filename.
    
    Args:
        filename: Filename string
    
    Returns:
        Extension (e.g., ".pdf")
    """
    if "." in filename:
        return "." + filename.split(".")[-1].lower()
    return ""


def is_valid_pdf(filename: str) -> bool:
    """
    Check if filename is a valid PDF.
    
    Args:
        filename: Filename to check
    
    Returns:
        True if PDF, False otherwise
    """
    return get_file_extension(filename).lower() == ".pdf"


def format_markdown_response(response: str) -> str:
    """
    Format response for markdown rendering.
    
    Args:
        response: Raw response text
    
    Returns:
        Markdown-formatted response
    """
    # Ensure proper spacing around headers
    lines = response.split('\n')
    formatted_lines = []
    
    for i, line in enumerate(lines):
        if line.startswith('#'):
            if i > 0:
                formatted_lines.append('')
            formatted_lines.append(line)
            formatted_lines.append('')
        else:
            formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)


def get_emoji_for_status(status: str) -> str:
    """
    Get emoji for status string.
    
    Args:
        status: Status string
    
    Returns:
        Appropriate emoji
    """
    emoji_map = {
        "success": "✅",
        "error": "❌",
        "warning": "⚠️",
        "info": "ℹ️",
        "loading": "⏳",
        "online": "🟢",
        "offline": "🔴",
    }
    return emoji_map.get(status.lower(), "")
