"""
Utility Helper Functions
"""

import re
import json


def sanitize_text(text: str) -> str:
    """
    Clean and normalize text
    
    Args:
        text: Input text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def extract_keywords(text: str, min_length: int = 4) -> list:
    """
    Simple keyword extraction
    
    Args:
        text: Input text
        min_length: Minimum word length to consider
        
    Returns:
        List of keywords
    """
    if not text:
        return []
    
    # Extract words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter by length and common stop words
    stop_words = {
        'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or',
        'but', 'in', 'with', 'to', 'for', 'of', 'as', 'by', 'from',
        'this', 'that', 'these', 'those', 'it', 'its', 'are', 'was',
        'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does',
        'did', 'will', 'would', 'should', 'could', 'may', 'might'
    }
    
    keywords = [
        word for word in words
        if len(word) >= min_length and word not in stop_words
    ]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for word in keywords:
        if word not in seen:
            seen.add(word)
            unique_keywords.append(word)
    
    return unique_keywords


def format_issues(issues: list) -> str:
    """
    Format issue list for display or storage
    
    Args:
        issues: List of issue strings
        
    Returns:
        Formatted string
    """
    if not issues:
        return "None"
    
    return "; ".join(issues)


def validate_json_payload(data: dict, required_fields: list) -> tuple:
    """
    Validate JSON payload
    
    Args:
        data: Input dictionary
        required_fields: List of required field names
        
    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    if not isinstance(data, dict):
        return False, "Payload must be a JSON object"
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
        
        if not data[field] or not str(data[field]).strip():
            return False, f"Field '{field}' cannot be empty"
    
    return True, None


def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Input text
        max_length: Maximum length
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."
