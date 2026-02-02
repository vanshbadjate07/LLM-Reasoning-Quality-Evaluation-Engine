"""
Reasoning Parser Module
Extracts and parses reasoning steps from LLM response
"""

import re


def parse_llm_response(raw_response: str) -> dict:
    """
    Parse the LLM response to extract answer and reasoning
    
    Args:
        raw_response: Raw text from LLM
        
    Returns:
        dict with keys:
            - answer: Final answer extracted
            - reasoning: Reasoning explanation text
    """
    if not raw_response or not raw_response.strip():
        return {
            "answer": "",
            "reasoning": ""
        }
    
    # Strategy 0: Explicit "REASONING:" and "FINAL ANSWER:" blocks (Priority)
    reasoning_match = re.search(r"REASONING:\s*(.*?)\s*(?:FINAL ANSWER:|$)", raw_response, re.DOTALL | re.IGNORECASE)
    answer_match = re.search(r"FINAL ANSWER:\s*(.*)", raw_response, re.DOTALL | re.IGNORECASE)
    
    reasoning = ""
    answer = ""
    
    if reasoning_match:
        reasoning = reasoning_match.group(1).strip()
    if answer_match:
        answer = answer_match.group(1).strip()
        
    if reasoning and answer:
        return {"answer": answer, "reasoning": reasoning}

    # Fallback Strategy: Try to find "Final Answer:" or similar patterns
    answer_patterns = [
        r"(?:final answer|answer):\s*(.+?)(?:\n|$)",
        r"(?:therefore|thus|so),?\s+(?:the answer is|it is)\s+(.+?)(?:\n|$)",
        r"(?:the result is|the solution is)\s+(.+?)(?:\n|$)"
    ]
    
    for pattern in answer_patterns:
        match = re.search(pattern, raw_response, re.IGNORECASE | re.MULTILINE)
        if match:
            answer = match.group(1).strip()
            break
    
    # If no explicit answer found, try to extract last sentence or paragraph
    if not answer:
        lines = [line.strip() for line in raw_response.split('\n') if line.strip()]
        if lines:
            answer = lines[-1]
    
    # Extract reasoning (everything before the final answer, or entire response)
    if not reasoning:
        reasoning = raw_response
        if answer:
            # Try to get everything before the answer
            answer_index = raw_response.lower().rfind(answer.lower())
            if answer_index > 0:
                # Look backwards for "Final Answer:" or similar
                reasoning_end = raw_response[:answer_index].rfind("Final Answer")
                if reasoning_end == -1:
                    reasoning_end = raw_response[:answer_index].rfind("Answer:")
                if reasoning_end == -1:
                    reasoning_end = raw_response[:answer_index].rfind("Therefore")
                
                if reasoning_end > 0:
                    reasoning = raw_response[:reasoning_end].strip()
                else:
                    reasoning = raw_response[:answer_index].strip()


def split_reasoning_steps(reasoning: str) -> list:
    """
    Split reasoning text into individual steps
    
    Args:
        reasoning: Reasoning explanation text
        
    Returns:
        list of reasoning steps (strings)
    """
    if not reasoning or not reasoning.strip():
        return []
    
    steps = []
    
    # Pattern 1: Numbered lists (1., 2., 1), 2) or **1.**, **2.**)
    numbered_pattern = r'(?:^|\n)\s*(?:\*\*)?(\d+)(?:[.)]|\*\*)\s+(.+?)(?=(?:\n\s*(?:\*\*)?\d+(?:[.)]|\*\*)|\Z))'
    numbered_matches = re.findall(numbered_pattern, reasoning, re.MULTILINE | re.DOTALL)
    
    if numbered_matches and len(numbered_matches) >= 2:
        steps = [match[1].strip() for match in numbered_matches]
        return steps
    
    # Pattern 2: Step 1:, Step 2:, **Step 1:**, etc.
    step_pattern = r'(?:^|\n)\s*(?:\*\*)?(?:step\s+\d+|step\s+[a-z])(?:\*\*)?[:\s]+(.+?)(?=(?:\n\s*(?:\*\*)?step\s+|\Z))'
    step_matches = re.findall(step_pattern, reasoning, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    
    if step_matches and len(step_matches) >= 2:
        steps = [match.strip() for match in step_matches]
        return steps
    
    # Pattern 3: Bullet points (-, *, •)
    bullet_pattern = r'(?:^|\n)\s*[-*•]\s+(.+?)(?=(?:\n\s*[-*•]|\Z))'
    bullet_matches = re.findall(bullet_pattern, reasoning, re.MULTILINE | re.DOTALL)
    
    if bullet_matches and len(bullet_matches) >= 2:
        steps = [match.strip() for match in bullet_matches]
        return steps
    
    # Pattern 4: First, Second, Third, etc.
    ordinal_pattern = r'(?:^|\n)\s*(?:first|second|third|fourth|fifth|next|then|finally)[,:\s]+(.+?)(?=(?:\n\s*(?:first|second|third|fourth|fifth|next|then|finally)|\Z))'
    ordinal_matches = re.findall(ordinal_pattern, reasoning, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    
    if ordinal_matches and len(ordinal_matches) >= 2:
        steps = [match.strip() for match in ordinal_matches]
        return steps
    
    # Fallback: Split by sentences or paragraphs
    # Try splitting by double newlines first (paragraphs)
    paragraphs = [p.strip() for p in reasoning.split('\n\n') if p.strip()]
    if len(paragraphs) >= 2:
        return paragraphs
    
    # Last resort: Split by sentences
    sentences = re.split(r'[.!?]+\s+', reasoning)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
    
    if len(sentences) >= 2:
        return sentences
    
    # If all else fails, return the entire reasoning as one step
    return [reasoning.strip()] if reasoning.strip() else []
