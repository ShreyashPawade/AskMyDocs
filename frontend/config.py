"""
Configuration module for AskMyDocs frontend.
Contains API endpoints, theme colors, and application constants.
"""

import os
from typing import Dict, Any

# ============================================================================
# API Configuration
# ============================================================================

# Backend API base URL - can be set via environment variable
BACKEND_URL = os.getenv("BACKEND_URL", "askmydocs-production-0b5f.up.railway.app")

# API Endpoints
API_ENDPOINTS = {
    "health": f"{BACKEND_URL}/health",
    "chat": f"{BACKEND_URL}/chat",
    "chat_stream": f"{BACKEND_URL}/chat_stream",
    "upload": f"{BACKEND_URL}/upload",
    "documents": f"{BACKEND_URL}/documents",
    "document_detail": f"{BACKEND_URL}/documents",  # {filename}
    "document_delete": f"{BACKEND_URL}/documents",  # {filename}
}

# ============================================================================
# Streamlit Page Configuration
# ============================================================================

PAGE_CONFIG = {
    "page_title": "AskMyDocs",
    "page_icon": "📚",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# ============================================================================
# Theme Colors - Dark Professional Theme
# ============================================================================

THEME_COLORS = {
    # Primary
    "bg_primary": "#0F1419",        # Very dark blue-black
    "bg_secondary": "#1A1F2E",      # Dark blue-gray
    "bg_tertiary": "#252B3D",       # Medium dark blue
    
    # Text
    "text_primary": "#E8EEF7",      # Light blue-white
    "text_secondary": "#A0A9BE",    # Medium gray-blue
    "text_tertiary": "#6B7280",     # Darker gray
    
    # Accents
    "accent_primary": "#6366F1",    # Indigo
    "accent_secondary": "#8B5CF6",  # Purple
    "accent_success": "#10B981",    # Green
    "accent_warning": "#F59E0B",    # Amber
    "accent_danger": "#EF4444",     # Red
    
    # Status Indicators
    "status_online": "#10B981",     # Green
    "status_offline": "#EF4444",    # Red
    
    # Borders
    "border_light": "#3F4558",      # Light gray
    "border_dark": "#1F2937",       # Dark gray
    
    # Message Bubbles
    "user_bubble": "#6366F1",       # Indigo for user
    "assistant_bubble": "#1F2937",  # Dark gray for assistant
}

# ============================================================================
# Application Constants
# ============================================================================

# Confidence thresholds
CONFIDENCE_THRESHOLDS = {
    "high": 4.0,      # >= 4.0 = High confidence (green)
    "medium": 2.0,    # >= 2.0 and < 4.0 = Medium (yellow)
    "low": 0.0,       # < 2.0 = Low confidence (red)
}

# UI Constants
UI_CONSTANTS = {
    "chat_max_width": 900,
    "message_max_width": 800,
    "sidebar_width": 350,
    "border_radius": "12px",
    "animation_duration": "0.3s",
}

# Upload constraints
UPLOAD_CONFIG = {
    "max_file_size_mb": 50,
    "allowed_formats": [".pdf"],
}

# Session defaults
SESSION_DEFAULTS = {
    "messages": [],
    "session_id": None,
    "documents": [],
    "backend_online": True,
    "current_chat_loading": False,
}

# ============================================================================
# Display Strings
# ============================================================================

DISPLAY_STRINGS = {
    "app_title": "AskMyDocs",
    "app_subtitle": "Hybrid Search • Gemini • ChromaDB • BM25 • Cross Encoder",
    "backend_online": "Backend Online",
    "backend_offline": "Backend Offline",
    "no_documents": "No documents uploaded yet.",
    "upload_hint": "Upload a PDF to get started.",
    "click_to_delete": "Click to delete",
    "click_to_view": "Click to view details",
    "ask_anything": "Ask anything about your documents...",
    "loading": "Thinking...",
    "error_network": "Network Error",
    "error_backend": "Backend Error",
    "error_upload": "Upload Failed",
    "error_delete": "Delete Failed",
    "success_upload": "✅ Document uploaded successfully!",
    "success_delete": "✅ Document deleted successfully!",
}
