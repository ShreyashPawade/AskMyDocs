"""
Confidence badge component for AskMyDocs.
Displays confidence score with color-coded visual indicator.
"""

import streamlit as st
from config import CONFIDENCE_THRESHOLDS
from utils.helpers import get_confidence_level, get_confidence_color


def render_confidence_badge(confidence: float) -> None:
    """
    Render a confidence badge.
    
    Args:
        confidence: Confidence score (0-5)
    """
    level = get_confidence_level(confidence)
    color_emoji = get_confidence_color(confidence)
    
    # Determine CSS class
    if confidence >= CONFIDENCE_THRESHOLDS["high"]:
        css_class = "confidence-high"
    elif confidence >= CONFIDENCE_THRESHOLDS["medium"]:
        css_class = "confidence-medium"
    else:
        css_class = "confidence-low"
    
    # Render badge
    st.markdown(
        f"""
        <div class="confidence-badge {css_class}">
            <span class="confidence-dot"></span>
            <span>{color_emoji} {level} Confidence ({confidence:.2f})</span>
        </div>
        """,
        unsafe_allow_html=True
    )
