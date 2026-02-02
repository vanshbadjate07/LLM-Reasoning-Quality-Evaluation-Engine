"""
Logger Module
Handles CSV logging of evaluations using Pandas
"""

import pandas as pd
import os
from datetime import datetime
from config import LOG_FILE_PATH


def ensure_log_directory():
    """Create logs directory if it doesn't exist"""
    log_dir = os.path.dirname(LOG_FILE_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)


def log_evaluation(data: dict) -> None:
    """
    Log evaluation to CSV file
    
    Args:
        data: Dictionary containing:
            - question
            - final_answer
            - reasoning_explanation
            - logical_consistency_score
            - completeness_score
            - instruction_following_score
            - hallucination_risk_score
            - final_verdict
            - detected_issues (list)
    """
    ensure_log_directory()
    
    # Prepare row data
    row_data = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Question": data.get("question", ""),
        "Final Answer": data.get("final_answer", ""),
        "Reasoning Explanation": data.get("reasoning_explanation", ""),
        "Logical Consistency Score": data.get("logical_consistency_score", 0),
        "Completeness Score": data.get("completeness_score", 0),
        "Instruction Following Score": data.get("instruction_following_score", 0),
        "Hallucination Risk Score": data.get("hallucination_risk_score", 0),
        "Final Verdict": data.get("final_verdict", ""),
        "Detected Issues": "; ".join(data.get("detected_issues", []))
    }
    
    # Create DataFrame
    df = pd.DataFrame([row_data])
    
    # Append to CSV (create if doesn't exist)
    if os.path.exists(LOG_FILE_PATH):
        # Append without header
        df.to_csv(LOG_FILE_PATH, mode='a', header=False, index=False)
    else:
        # Create new file with header
        df.to_csv(LOG_FILE_PATH, mode='w', header=True, index=False)


def get_evaluation_history(limit: int = None) -> pd.DataFrame:
    """
    Retrieve evaluation history from CSV
    
    Args:
        limit: Optional limit on number of records to return
        
    Returns:
        DataFrame with evaluation history
    """
    if not os.path.exists(LOG_FILE_PATH):
        return pd.DataFrame()
    
    df = pd.read_csv(LOG_FILE_PATH)
    
    if limit:
        return df.tail(limit)
    
    return df
