"""
Header component for AskMyDocs.
Displays application title and backend status indicator.
"""

import streamlit as st
from config import THEME_COLORS, DISPLAY_STRINGS
from api import APIClient
from utils.session import set_backend_status, get_backend_status


def render_header() -> None:
    """Render the application header."""
    
    # Check backend status
    backend_online = APIClient.check_health()
    set_backend_status(backend_online)
    
    # HTML header with custom styling
    st.markdown(
        f"""
        <div class="header-container">
            <div class="header-content">
                <div class="header-left">
                    <h1 class="header-title">{DISPLAY_STRINGS['app_title']}</h1>
                    <p class="header-subtitle">{DISPLAY_STRINGS['app_subtitle']}</p>
                </div>
                <div class="header-status">
                    <div class="status-indicator {'status-online' if backend_online else 'status-offline'}"></div>
                    <span class="status-text">
                        {'✅ Online' if backend_online else '❌ Offline'}
                    </span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
