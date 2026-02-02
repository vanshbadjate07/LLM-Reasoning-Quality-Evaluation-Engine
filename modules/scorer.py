"""
Scorer Module
Calculates scores and generates verdict
"""

from config import SCORING_WEIGHTS, GOOD_REASONING_THRESHOLD


def calculate_scores(evaluation_results: dict) -> dict:
    """
    Calculate aggregate scores from evaluation results
    
    Args:
        evaluation_results: Results from evaluator.evaluate_reasoning()
        
    Returns:
        dict with four scores (0-100 each):
            - logical_consistency_score
            - completeness_score
            - instruction_following_score
            - hallucination_risk_score
    """
    
    # Logical Consistency Score
    lc_rules = evaluation_results.get("logical_consistency", {})
    lc_scores = [rule["score"] for rule in lc_rules.values()]
    logical_consistency_score = sum(lc_scores) / len(lc_scores) if lc_scores else 0
    
    # Completeness Score
    comp_rules = evaluation_results.get("completeness", {})
    comp_scores = [rule["score"] for rule in comp_rules.values()]
    completeness_score = sum(comp_scores) / len(comp_scores) if comp_scores else 0
    
    # Instruction Following Score
    if_rules = evaluation_results.get("instruction_following", {})
    if_scores = [rule["score"] for rule in if_rules.values()]
    instruction_following_score = sum(if_scores) / len(if_scores) if if_scores else 0
    
    # Hallucination Risk Score (higher score = more risk)
    hr_rules = evaluation_results.get("hallucination_risk", {})
    hr_scores = [rule["score"] for rule in hr_rules.values()]
    hallucination_risk_score = sum(hr_scores) / len(hr_scores) if hr_scores else 100
    
    return {
        "logical_consistency_score": round(logical_consistency_score, 2),
        "completeness_score": round(completeness_score, 2),
        "instruction_following_score": round(instruction_following_score, 2),
        "hallucination_risk_score": round(hallucination_risk_score, 2)
    }


def generate_verdict(scores: dict) -> str:
    """
    Generate final verdict based on scores
    
    Args:
        scores: Dict with four score values
        
    Returns:
        "Good Reasoning" or "Flawed Reasoning"
    """
    # Calculate weighted average
    # Note: For hallucination_risk, we invert it (100 - score) because higher risk = worse
    weighted_score = (
        scores["logical_consistency_score"] * SCORING_WEIGHTS["logical_consistency"] +
        scores["completeness_score"] * SCORING_WEIGHTS["completeness"] +
        scores["instruction_following_score"] * SCORING_WEIGHTS["instruction_following"] +
        (100 - scores["hallucination_risk_score"]) * SCORING_WEIGHTS["hallucination_risk"]
    )
    
    # Determine verdict
    if weighted_score >= GOOD_REASONING_THRESHOLD:
        return "Good Reasoning"
    else:
        return "Flawed Reasoning"


def get_overall_score(scores: dict) -> float:
    """
    Calculate overall weighted score
    
    Args:
        scores: Dict with four score values
        
    Returns:
        Overall score (0-100)
    """
    weighted_score = (
        scores["logical_consistency_score"] * SCORING_WEIGHTS["logical_consistency"] +
        scores["completeness_score"] * SCORING_WEIGHTS["completeness"] +
        scores["instruction_following_score"] * SCORING_WEIGHTS["instruction_following"] +
        (100 - scores["hallucination_risk_score"]) * SCORING_WEIGHTS["hallucination_risk"]
    )
    
    return round(weighted_score, 2)
