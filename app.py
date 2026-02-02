"""
ReasonEval - LLM Reasoning Quality Evaluation System
Flask Application Entry Point
"""

from flask import Flask, request, jsonify
from modules.llm_client import call_llm
from modules.reasoning_parser import parse_llm_response, split_reasoning_steps
from modules.evaluator import evaluate_reasoning
from modules.scorer import calculate_scores, generate_verdict, get_overall_score
from modules.logger import log_evaluation
from utils.helpers import validate_json_payload, format_issues
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG

app = Flask(__name__)


@app.route('/evaluate', methods=['POST'])
def evaluate():
    """
    Main evaluation endpoint
    
    Expected JSON payload:
        {
            "question": "Your question here"
        }
    
    Returns:
        JSON response with evaluation results
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        # Validate payload
        is_valid, error_msg = validate_json_payload(data, ['question'])
        if not is_valid:
            return jsonify({
                "success": False,
                "error": error_msg
            }), 400
        
        question = data['question'].strip()
        
        # Step 1: Call LLM
        llm_result = call_llm(question)
        
        if not llm_result['success']:
            return jsonify({
                "success": False,
                "error": f"LLM call failed: {llm_result['error']}"
            }), 500
        
        raw_response = llm_result['raw_response']
        
        # Step 2: Parse LLM response
        parsed = parse_llm_response(raw_response)
        answer = parsed['answer']
        reasoning = parsed['reasoning']
        
        # Step 3: Split reasoning into steps
        steps = split_reasoning_steps(reasoning)
        
        # Step 4: Evaluate reasoning
        evaluation_results = evaluate_reasoning(steps, answer, question, reasoning)
        
        # Step 5: Calculate scores
        scores = calculate_scores(evaluation_results)
        
        # Step 6: Generate verdict
        verdict = generate_verdict(scores)
        overall_score = get_overall_score(scores)
        
        # Step 7: Get detected issues
        detected_issues = evaluation_results.get('detected_issues', [])
        
        # Step 8: Log evaluation
        log_data = {
            "question": question,
            "final_answer": answer,
            "reasoning_explanation": reasoning,
            "logical_consistency_score": scores['logical_consistency_score'],
            "completeness_score": scores['completeness_score'],
            "instruction_following_score": scores['instruction_following_score'],
            "hallucination_risk_score": scores['hallucination_risk_score'],
            "final_verdict": verdict,
            "detected_issues": detected_issues
        }
        log_evaluation(log_data)
        
        # Step 9: Prepare response
        response = {
            "success": True,
            "question": question,
            "raw_llm_response": raw_response,  # Include original LLM response
            "final_answer": answer,
            "reasoning_steps": steps,
            "reasoning_explanation": reasoning,
            "scores": {
                "logical_consistency": scores['logical_consistency_score'],
                "completeness": scores['completeness_score'],
                "instruction_following": scores['instruction_following_score'],
                "hallucination_risk": scores['hallucination_risk_score'],
                "overall_score": overall_score
            },
            "verdict": verdict,
            "detected_issues": detected_issues,
            "step_count": len(steps)
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "ReasonEval"
    }), 200


@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API information"""
    return jsonify({
        "service": "ReasonEval - LLM Reasoning Quality Evaluation System",
        "version": "1.0.0",
        "endpoints": {
            "/evaluate": {
                "method": "POST",
                "description": "Evaluate reasoning quality of LLM response",
                "payload": {
                    "question": "Your question here"
                }
            },
            "/health": {
                "method": "GET",
                "description": "Health check endpoint"
            }
        }
    }), 200


if __name__ == '__main__':
    print("=" * 60)
    print("ReasonEval - LLM Reasoning Quality Evaluation System")
    print("=" * 60)
    print(f"Starting Flask server on {FLASK_HOST}:{FLASK_PORT}")
    print(f"API Endpoint: http://{FLASK_HOST}:{FLASK_PORT}/evaluate")
    print("=" * 60)
    
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
