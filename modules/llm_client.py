"""
Ollama LLM Client Module
Handles communication with local Ollama instance
"""

import requests
import subprocess
import json
import time
from config import OLLAMA_MODEL, OLLAMA_API_BASE, OLLAMA_TIMEOUT, LLM_PROMPT_TEMPLATE


def check_ollama_running():
    """Check if Ollama service is running"""
    try:
        response = requests.get(f"{OLLAMA_API_BASE}/api/tags", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def check_model_available():
    """Check if the required model is available locally"""
    try:
        response = requests.get(f"{OLLAMA_API_BASE}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            for model in models:
                if model.get("name", "").startswith(OLLAMA_MODEL.split(":")[0]):
                    return True
        return False
    except requests.exceptions.RequestException:
        return False


def download_model():
    """Download the LLM model using Ollama CLI"""
    print(f"Downloading model {OLLAMA_MODEL}... This may take a few minutes.")
    try:
        # Use subprocess to run ollama pull command
        result = subprocess.run(
            ["ollama", "pull", OLLAMA_MODEL],
            capture_output=True,
            text=True,
            timeout=600  # 10 minutes timeout for download
        )
        
        if result.returncode == 0:
            print(f"Model {OLLAMA_MODEL} downloaded successfully!")
            return True
        else:
            print(f"Error downloading model: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("Model download timed out. Please try again.")
        return False
    except FileNotFoundError:
        print("Ollama CLI not found. Please install Ollama first.")
        return False
    except Exception as e:
        print(f"Error downloading model: {str(e)}")
        return False


def ensure_model_ready():
    """Ensure Ollama is running and model is available"""
    if not check_ollama_running():
        raise Exception(
            "Ollama is not running. Please start Ollama service first.\n"
            "Visit: https://ollama.ai for installation instructions."
        )
    
    if not check_model_available():
        print(f"Model {OLLAMA_MODEL} not found locally.")
        if not download_model():
            raise Exception(f"Failed to download model {OLLAMA_MODEL}")
    
    return True


def call_llm(question: str) -> dict:
    """
    Call Ollama LLM with the given question
    
    Args:
        question: The question to ask the LLM
        
    Returns:
        dict with keys:
            - raw_response: Original LLM output
            - success: Boolean indicating if call was successful
            - error: Error message if failed
    """
    # Ensure model is ready
    try:
        ensure_model_ready()
    except Exception as e:
        return {
            "raw_response": "",
            "success": False,
            "error": str(e)
        }
    
    # Format the prompt
    prompt = LLM_PROMPT_TEMPLATE.format(question=question)
    
    # Prepare the request payload
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
        }
    }
    
    try:
        # Make the API call
        response = requests.post(
            f"{OLLAMA_API_BASE}/api/generate",
            json=payload,
            timeout=OLLAMA_TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            raw_response = result.get("response", "")
            
            return {
                "raw_response": raw_response,
                "success": True,
                "error": None
            }
        else:
            return {
                "raw_response": "",
                "success": False,
                "error": f"Ollama API returned status code {response.status_code}"
            }
            
    except requests.exceptions.Timeout:
        return {
            "raw_response": "",
            "success": False,
            "error": "Request to Ollama timed out"
        }
    except requests.exceptions.RequestException as e:
        return {
            "raw_response": "",
            "success": False,
            "error": f"Request error: {str(e)}"
        }
    except Exception as e:
        return {
            "raw_response": "",
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }
