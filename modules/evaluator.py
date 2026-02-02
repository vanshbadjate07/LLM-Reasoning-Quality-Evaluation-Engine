"""
Rule-Based Evaluator Module
Implements reasoning quality evaluation rules
"""

import re
from utils.helpers import sanitize_text


# ============================================================================
# LOGICAL CONSISTENCY RULES
# ============================================================================

def check_step_count(steps: list) -> dict:
    """Check if multiple reasoning steps exist"""
    count = len(steps)
    
    if count == 0:
        return {
            "score": 0,
            "issue": "No reasoning steps found"
        }
    elif count == 1:
        return {
            "score": 30,
            "issue": "Only one reasoning step provided"
        }
    elif count == 2:
        return {
            "score": 60,
            "issue": "Only two reasoning steps (minimal)"
        }
    else:
        return {
            "score": 100,
            "issue": None
        }


def check_logical_flow(steps: list) -> dict:
    """Check for logical flow and coherence between steps"""
    if len(steps) < 2:
        return {"score": 50, "issue": "Insufficient steps to evaluate flow"}
    
    issues = []
    score = 100
    
    # Check for transition words/phrases
    transition_words = [
        'therefore', 'thus', 'so', 'hence', 'consequently',
        'then', 'next', 'after', 'because', 'since',
        'as a result', 'this means', 'which gives'
    ]
    
    transitions_found = 0
    for step in steps:
        step_lower = step.lower()
        if any(word in step_lower for word in transition_words):
            transitions_found += 1
    
    # Penalize if very few transitions
    if transitions_found < len(steps) * 0.3:
        score -= 20
        issues.append("Weak logical connections between steps")
    
    # Check for abrupt topic changes (very basic heuristic)
    # Look for steps that are very short or disconnected
    very_short_steps = sum(1 for step in steps if len(step.split()) < 5)
    if very_short_steps > len(steps) * 0.4:
        score -= 15
        issues.append("Some steps are too brief or disconnected")
    
    return {
        "score": max(0, score),
        "issue": "; ".join(issues) if issues else None
    }


def check_contradictions(steps: list) -> dict:
    """Check for contradictory statements"""
    if len(steps) < 2:
        return {"score": 100, "issue": None}
    
    # Simple contradiction detection using negation patterns
    contradiction_indicators = [
        (r'\bnot\b', r'\bis\b'),
        (r'\bno\b', r'\byes\b'),
        (r'\bcannot\b', r'\bcan\b'),
        (r'\bfalse\b', r'\btrue\b'),
        (r'\bincorrect\b', r'\bcorrect\b'),
    ]
    
    score = 100
    issues = []
    
    # Check for explicit contradictions
    for i, step in enumerate(steps):
        step_lower = step.lower()
        if 'however' in step_lower or 'but actually' in step_lower or 'correction' in step_lower:
            score -= 20
            issues.append(f"Possible self-correction or contradiction in step {i+1}")
    
    return {
        "score": max(0, score),
        "issue": "; ".join(issues) if issues else None
    }


def check_answer_support(steps: list, answer: str) -> dict:
    """Check if the final answer is supported by the reasoning"""
    if not answer or not steps:
        return {"score": 0, "issue": "Missing answer or reasoning"}
    
    # Extract key terms from answer
    answer_words = set(re.findall(r'\b\w+\b', answer.lower()))
    answer_words = {w for w in answer_words if len(w) > 3}  # Filter short words
    
    if not answer_words:
        return {"score": 50, "issue": "Cannot extract key terms from answer"}
    
    # Check if answer terms appear in reasoning
    reasoning_text = " ".join(steps).lower()
    matching_terms = sum(1 for word in answer_words if word in reasoning_text)
    
    if matching_terms == 0:
        return {
            "score": 20,
            "issue": "Answer not clearly derived from reasoning"
        }
    elif matching_terms < len(answer_words) * 0.3:
        return {
            "score": 50,
            "issue": "Weak connection between reasoning and answer"
        }
    else:
        return {"score": 100, "issue": None}


# ============================================================================
# COMPLETENESS RULES
# ============================================================================

def check_missing_steps(steps: list, question: str) -> dict:
    """Detect obvious gaps in reasoning chain"""
    if not steps:
        return {"score": 0, "issue": "No reasoning provided"}
    
    score = 100
    issues = []
    
    # Check if question involves calculation
    if any(op in question for op in ['+', '-', '*', '/', 'calculate', 'compute', 'sum', 'product']):
        # Look for numerical operations in steps
        has_calculation = any(
            any(op in step for op in ['+', '-', '*', '/', '=', 'equals'])
            for step in steps
        )
        if not has_calculation:
            score -= 30
            issues.append("Question requires calculation but no explicit computation shown")
    
    # Check for very short reasoning overall
    total_length = sum(len(step) for step in steps)
    if total_length < 100:
        score -= 20
        issues.append("Reasoning is too brief")
    
    return {
        "score": max(0, score),
        "issue": "; ".join(issues) if issues else None
    }


def check_step_depth(steps: list) -> dict:
    """Evaluate if steps are too shallow or vague"""
    if not steps:
        return {"score": 0, "issue": "No steps to evaluate"}
    
    score = 100
    issues = []
    
    # Check average step length
    avg_length = sum(len(step.split()) for step in steps) / len(steps)
    
    if avg_length < 5:
        score -= 30
        issues.append("Steps are too shallow (very short)")
    elif avg_length < 8:
        score -= 15
        issues.append("Steps could be more detailed")
    
    # Check for vague words
    vague_words = ['maybe', 'perhaps', 'possibly', 'might', 'could be', 'seems']
    vague_count = sum(
        1 for step in steps
        if any(word in step.lower() for word in vague_words)
    )
    
    if vague_count > len(steps) * 0.4:
        score -= 20
        issues.append("Too many vague or uncertain statements")
    
    return {
        "score": max(0, score),
        "issue": "; ".join(issues) if issues else None
    }


def check_reasoning_substance(steps: list) -> dict:
    """Check for indicators of deep, first-principles thinking"""
    if not steps:
        return {"score": 0, "issue": "No steps to evaluate"}
        
    score = 100
    issues = []
    
    # Text to check
    full_text = " ".join(steps).lower()
    
    # Check for fundamental indicators (First Principles)
    principles_indicators = [
        'fundamental', 'break down', 'truth', 'assumption', 'axiom',
        'specifically', 'precisely', 'definition', 'core'
    ]
    
    found_principles = sum(1 for ind in principles_indicators if ind in full_text)
    
    if found_principles == 0:
        score -= 20
        issues.append("Lack of first-principles language (e.g., 'fundamental', 'assumption')")
    
    # Check for causal reasoning
    causal_indicators = [
        'because', 'since', 'implies', 'causes', 'leads to', 'result of', 'due to'
    ]
    found_causal = sum(1 for ind in causal_indicators if ind in full_text)
    
    if found_causal < len(steps) * 0.5:
        score -= 15
        issues.append("Weak causal reasoning (few 'because', 'since', etc.)")
        
    return {
        "score": max(0, score),
        "issue": "; ".join(issues) if issues else None
    }


# ============================================================================
# INSTRUCTION FOLLOWING RULES
# ============================================================================

def check_step_format(reasoning: str) -> dict:
    """Verify step-by-step structure"""
    if not reasoning:
        return {"score": 0, "issue": "No reasoning provided"}
    
    score = 100
    issues = []
    
    # Check for numbered format
    has_numbers = bool(re.search(r'(?:^|\n)\s*\d+[.)]', reasoning, re.MULTILINE))
    
    # Check for "Step" labels
    has_step_labels = bool(re.search(r'(?:^|\n)\s*step\s+\d+', reasoning, re.IGNORECASE | re.MULTILINE))
    
    # Check for bullet points
    has_bullets = bool(re.search(r'(?:^|\n)\s*[-*•]', reasoning, re.MULTILINE))
    
    # Check for ordinal words
    has_ordinals = bool(re.search(
        r'(?:^|\n)\s*(?:first|second|third|next|then|finally)',
        reasoning,
        re.IGNORECASE | re.MULTILINE
    ))
    
    if not (has_numbers or has_step_labels or has_bullets or has_ordinals):
        score -= 40
        issues.append("No clear step-by-step structure")
    
    return {
        "score": max(0, score),
        "issue": "; ".join(issues) if issues else None
    }


def check_explicit_numbering(reasoning: str) -> dict:
    """Check for numbered or labeled steps"""
    if not reasoning:
        return {"score": 0, "issue": "No reasoning provided"}
    
    # Count numbered items
    numbered_items = len(re.findall(r'(?:^|\n)\s*\d+[.)]', reasoning, re.MULTILINE))
    
    # Count step labels
    step_labels = len(re.findall(r'(?:^|\n)\s*step\s+\d+', reasoning, re.IGNORECASE | re.MULTILINE))
    
    total_explicit = numbered_items + step_labels
    
    if total_explicit >= 3:
        return {"score": 100, "issue": None}
    elif total_explicit >= 2:
        return {"score": 70, "issue": "Limited explicit numbering"}
    elif total_explicit >= 1:
        return {"score": 40, "issue": "Minimal explicit numbering"}
    else:
        return {"score": 20, "issue": "No explicit step numbering"}


# ============================================================================
# HALLUCINATION RISK RULES
# ============================================================================

def check_unsupported_claims(steps: list) -> dict:
    """Flag claims without justification"""
    if not steps:
        return {"score": 100, "issue": None}  # No claims = no unsupported claims
    
    score = 100
    issues = []
    
    # Look for assertive statements without justification
    assertive_patterns = [
        r'\bit is\b.*\b(?:obvious|clear|evident)\b',
        r'\bwe know that\b',
        r'\bit must be\b',
        r'\bclearly\b',
    ]
    
    unsupported_count = 0
    for step in steps:
        step_lower = step.lower()
        for pattern in assertive_patterns:
            if re.search(pattern, step_lower):
                # Check if there's a "because" or "since" nearby
                if 'because' not in step_lower and 'since' not in step_lower and 'as' not in step_lower:
                    unsupported_count += 1
                    break
    
    if unsupported_count > 0:
        penalty = min(40, unsupported_count * 15)
        score -= penalty
        issues.append(f"Found {unsupported_count} potentially unsupported claim(s)")
    
    return {
        "score": max(0, score),
        "issue": "; ".join(issues) if issues else None
    }


def check_vague_statements(steps: list) -> dict:
    """Detect overly vague or ambiguous language"""
    if not steps:
        return {"score": 100, "issue": None}
    
    score = 100
    issues = []
    
    vague_indicators = [
        'probably', 'maybe', 'perhaps', 'might', 'could',
        'seems', 'appears', 'likely', 'possibly', 'somewhat',
        'kind of', 'sort of', 'approximately', 'roughly'
    ]
    
    vague_count = 0
    for step in steps:
        step_lower = step.lower()
        if any(indicator in step_lower for indicator in vague_indicators):
            vague_count += 1
    
    if vague_count > len(steps) * 0.5:
        score -= 40
        issues.append("Excessive vague or uncertain language")
    elif vague_count > len(steps) * 0.3:
        score -= 20
        issues.append("Moderate use of vague language")
    
    return {
        "score": max(0, score),
        "issue": "; ".join(issues) if issues else None
    }


# ============================================================================
# MAIN EVALUATION FUNCTION
# ============================================================================

def evaluate_reasoning(steps: list, answer: str, question: str, raw_reasoning: str) -> dict:
    """
    Run all evaluation rules and collect results
    
    Args:
        steps: List of reasoning steps
        answer: Final answer
        question: Original question
        raw_reasoning: Raw reasoning text
        
    Returns:
        dict with rule results and detected issues
    """
    results = {
        "logical_consistency": {
            "step_count": check_step_count(steps),
            "logical_flow": check_logical_flow(steps),
            "contradictions": check_contradictions(steps),
            "answer_support": check_answer_support(steps, answer)
        },
        "completeness": {
            "missing_steps": check_missing_steps(steps, question),
            "step_depth": check_step_depth(steps),
            "substance": check_reasoning_substance(steps)
        },
        "instruction_following": {
            "step_format": check_step_format(raw_reasoning),
            "explicit_numbering": check_explicit_numbering(raw_reasoning)
        },
        "hallucination_risk": {
            "unsupported_claims": check_unsupported_claims(steps),
            "vague_statements": check_vague_statements(steps)
        }
    }
    
    # Collect all detected issues
    all_issues = []
    for category, rules in results.items():
        for rule_name, rule_result in rules.items():
            if rule_result.get("issue"):
                all_issues.append(f"[{category}] {rule_result['issue']}")
    
    results["detected_issues"] = all_issues
    
    return results
