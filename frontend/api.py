"""
API client module for communicating with the AskMyDocs backend.
Handles all REST API calls with proper error handling and timeouts.
"""

import requests
from typing import Dict, Any, List, Optional, Generator
import streamlit as st
from config import API_ENDPOINTS, DISPLAY_STRINGS
from utils.helpers import log_error

# Request timeout (seconds)
REQUEST_TIMEOUT = 180
STREAM_TIMEOUT = 60


class APIClient:
    """Client for interacting with AskMyDocs backend."""
    
    @staticmethod
    def check_health() -> bool:
        """
        Check if backend is online.
        
        Returns:
            bool: True if backend is online, False otherwise
        """
        try:
            response = requests.get(
                API_ENDPOINTS["health"],
                timeout=REQUEST_TIMEOUT
            )
            return response.status_code == 200
        except Exception as e:
            log_error(f"Health check failed: {str(e)}")
            return False
    
    @staticmethod
    def send_chat_message(
        question: str,
        session_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Send a chat message to the backend.
        
        Args:
            question: The user's question
            session_id: Session ID for conversation memory
        
        Returns:
            Response dict with answer, confidence, and sources, or None on error
        """
        try:
            payload = {
                "question": question,
                "session_id": session_id
            }
            
            response = requests.post(
                API_ENDPOINTS["chat"],
                json=payload,
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                log_error(f"Chat API error: {response.status_code} - {response.text}")
                st.error(f"{DISPLAY_STRINGS['error_backend']}: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            log_error("Chat request timeout")
            st.error("⏱️ Request timed out. Please try again.")
            return None
        except requests.exceptions.ConnectionError:
            log_error("Connection error to backend")
            st.error(f"❌ {DISPLAY_STRINGS['error_network']}: Cannot reach backend")
            return None
        except Exception as e:
            log_error(f"Chat API exception: {str(e)}")
            st.error(f"❌ Error: {str(e)}")
            return None
    
    @staticmethod
    def stream_chat_message(
        question: str,
        session_id: str
    ) -> Optional[Generator[str, None, None]]:
        """
        Stream chat response token-by-token from backend.
        
        Args:
            question: The user's question
            session_id: Session ID for conversation memory
        
        Yields:
            Token strings as they arrive
        
        Returns:
            None if request fails, otherwise yields tokens
        """
        try:
            payload = {
                "question": question,
                "session_id": session_id
            }
            
            response = requests.post(
                API_ENDPOINTS["chat_stream"],
                json=payload,
                timeout=STREAM_TIMEOUT,
                stream=True
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        yield line.decode('utf-8')
            else:
                log_error(f"Stream API error: {response.status_code}")
                st.error(f"{DISPLAY_STRINGS['error_backend']}: {response.status_code}")
                
        except requests.exceptions.Timeout:
            log_error("Stream request timeout")
            st.error("⏱️ Request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            log_error("Connection error during streaming")
            st.error(f"❌ {DISPLAY_STRINGS['error_network']}: Connection lost")
        except Exception as e:
            log_error(f"Stream API exception: {str(e)}")
            st.error(f"❌ Error: {str(e)}")
    
    @staticmethod
    def upload_document(file_bytes: bytes, filename: str) -> Optional[Dict[str, Any]]:
        """
        Upload a PDF document to the backend.
        
        Args:
            file_bytes: PDF file content as bytes
            filename: Original filename
        
        Returns:
            Response dict with upload status and metadata, or None on error
        """
        try:
            files = {"file": (filename, file_bytes, "application/pdf")}
            
            response = requests.post(
                API_ENDPOINTS["upload"],
                files=files,
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                log_error(f"Upload API error: {response.status_code} - {response.text}")
                st.error(f"{DISPLAY_STRINGS['error_upload']}: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            log_error("Upload request timeout")
            st.error("⏱️ Upload timed out. File may be too large.")
            return None
        except requests.exceptions.ConnectionError:
            log_error("Connection error during upload")
            st.error(f"❌ {DISPLAY_STRINGS['error_network']}: Cannot reach backend")
            return None
        except Exception as e:
            log_error(f"Upload API exception: {str(e)}")
            st.error(f"❌ {DISPLAY_STRINGS['error_upload']}: {str(e)}")
            return None
    
    @staticmethod
    def get_documents() -> Optional[Dict[str, Any]]:
        """
        Fetch list of uploaded documents.
        
        Returns:
            Response dict with documents list, or None on error
        """
        try:
            response = requests.get(
                API_ENDPOINTS["documents"],
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                log_error(f"Get documents error: {response.status_code}")
                return None
                
        except requests.exceptions.ConnectionError:
            log_error("Connection error fetching documents")
            return None
        except Exception as e:
            log_error(f"Get documents exception: {str(e)}")
            return None
    
    @staticmethod
    def get_document_detail(filename: str) -> Optional[Dict[str, Any]]:
        """
        Fetch detailed metadata for a specific document.
        
        Args:
            filename: Document filename
        
        Returns:
            Document metadata dict, or None on error
        """
        try:
            url = f"{API_ENDPOINTS['document_detail']}/{filename}"
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                return response.json()
            else:
                log_error(f"Get document detail error: {response.status_code}")
                return None
                
        except Exception as e:
            log_error(f"Get document detail exception: {str(e)}")
            return None
    
    @staticmethod
    def delete_document(filename: str) -> bool:
        """
        Delete a document from the backend.
        
        Args:
            filename: Document filename to delete
        
        Returns:
            True if successful, False otherwise
        """
        try:
            url = f"{API_ENDPOINTS['document_delete']}/{filename}"
            response = requests.delete(url, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                return True
            else:
                log_error(f"Delete document error: {response.status_code} - {response.text}")
                st.error(f"{DISPLAY_STRINGS['error_delete']}: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            log_error("Connection error during delete")
            st.error(f"❌ {DISPLAY_STRINGS['error_network']}: Cannot reach backend")
            return False
        except Exception as e:
            log_error(f"Delete document exception: {str(e)}")
            st.error(f"❌ {DISPLAY_STRINGS['error_delete']}: {str(e)}")
            return False
