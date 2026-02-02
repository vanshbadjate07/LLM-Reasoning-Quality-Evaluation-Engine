"""
ReasonEval - Streamlit UI
Interactive web interface for LLM Reasoning Quality Evaluation
"""

import streamlit as st
from modules.llm_client import call_llm
from modules.reasoning_parser import parse_llm_response, split_reasoning_steps
from modules.evaluator import evaluate_reasoning
from modules.scorer import calculate_scores, generate_verdict, get_overall_score
from modules.logger import log_evaluation
import json

# Page configuration
st.set_page_config(
    page_title="ReasonEval - LLM Reasoning Evaluator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Clean, Professional, High Contrast
st.markdown("""
<style>
    /* Global Styles */
    .main {
        background-color: #ffffff;
        color: #1f2937;
    }
    
    /* Header Styles */
    .main-header {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #111827;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    /* Score Cards */
    .metric-card {
        background-color: #f3f4f6;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1f2937;
    }
    .metric-label {
        font-size: 0.875rem;
        color: #6b7280;
        margin-top: 0.25rem;
    }
    
    /* Verdict Badges */
    .verdict-badge {
        padding: 1rem 2rem;
        border-radius: 8px;
        font-size: 1.5rem;
        font-weight: 700;
        text-align: center;
        margin: 1.5rem 0;
        color: white;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .verdict-good {
        background-color: #059669; /* Green-600 */
    }
    .verdict-flawed {
        background-color: #dc2626; /* Red-600 */
    }
    
    /* Reasoning Steps */
    .step-container {
        border-left: 4px solid #3b82f6; /* Blue-500 */
        background-color: #f9fafb;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0 8px 8px 0;
    }
    .step-number {
        font-weight: 700;
        color: #3b82f6;
        margin-bottom: 0.25rem;
    }
    .step-content {
        color: #374151;
        line-height: 1.5;
    }
    
    /* Feedback Box */
    .issue-box {
        background-color: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 6px;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        color: #991b1b;
        display: flex;
        align-items: center;
    }
    .success-box {
        background-color: #ecfdf5;
        border: 1px solid #a7f3d0;
        border-radius: 6px;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        color: #065f46;
    }
</style>
""", unsafe_allow_html=True)

# Title Section
st.markdown("<h1 style='text-align: center;'>🧠 ReasonEval</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280; margin-bottom: 2rem;'>Advanced LLM Reasoning Quality Evaluation System</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Evaluation Criteria")
    st.markdown("""
    Our scoring methodology evaluates 4 key dimensions:
    
    **1. Logical Consistency (35%)**
    - Coherent flow between steps
    - No self-contradictions
    - Conclusion follows premises
    
    **2. Completeness (25%)**
    - Sufficient breakdown of steps
    - No missing logical links
    - Detailed explanations
    
    **3. Instruction Following (20%)**
    - Adherence to formatting
    - Clear step structuring
    
    **4. Hallucination Risk (20%)**
    - Unsupported claims detection
    - Vague/ambiguous language
    """)
    
    st.divider()
    st.header("Settings")
    show_raw = st.toggle("Show Raw LLM Output", value=False)
    
# Main Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Input Question")
    question = st.text_area(
        "Enter a question to evaluate:",
        placeholder="Example: If a train travels 60km in 45 mins, what is its speed in km/h?",
        height=120,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True) # Spacer
    evaluate_btn = st.button("🚀 Run Evaluation", type="primary", use_container_width=True)
    st.caption("Using model: **llama3.2:1b** (Fast)")

if evaluate_btn and question:
    with st.spinner("🤔 Generating reasoning and evaluating..."):
        # 1. Call LLM
        llm_result = call_llm(question)
        
        if not llm_result['success']:
            st.error(f"System Error: {llm_result['error']}")
            st.stop()
            
        raw_response = llm_result['raw_response']
        
        # 2. Parse & Process
        parsed = parse_llm_response(raw_response)
        steps = split_reasoning_steps(parsed['reasoning'])
        
        # 3. Evaluate
        eval_results = evaluate_reasoning(steps, parsed['answer'], question, parsed['reasoning'])
        scores = calculate_scores(eval_results)
        verdict = generate_verdict(scores)
        overall = get_overall_score(scores)
        issues = eval_results.get('detected_issues', [])
        
        # 4. Log
        log_data = {
            "question": question,
            "final_answer": parsed['answer'],
            "reasoning_explanation": parsed['reasoning'],
            "logical_consistency_score": scores['logical_consistency_score'],
            "completeness_score": scores['completeness_score'],
            "instruction_following_score": scores['instruction_following_score'],
            "hallucination_risk_score": scores['hallucination_risk_score'],
            "final_verdict": verdict,
            "detected_issues": issues
        }
        log_evaluation(log_data)

    # --- RESULTS DISPLAY ---
    st.divider()
    
    # Top Section: Verdict & Overall
    res_col1, res_col2 = st.columns([2, 1])
    
    with res_col1:
        color_class = "verdict-good" if verdict == "Good Reasoning" else "verdict-flawed"
        icon = "✅" if verdict == "Good Reasoning" else "⚠️"
        st.markdown(f"""
        <div class="verdict-badge {color_class}">
            {icon} {verdict}
        </div>
        """, unsafe_allow_html=True)
        
    with res_col2:
        st.markdown(f"""
        <div class="metric-card" style="margin-top: 1.5rem; border-color: #3b82f6; background-color: #eff6ff;">
            <div class="metric-value" style="color: #1d4ed8;">{overall:.1f}%</div>
            <div class="metric-label">Quality Score</div>
        </div>
        """, unsafe_allow_html=True)

    # Category Scores
    st.subheader("📊 Category Breakdown")
    c1, c2, c3, c4 = st.columns(4)
    
    def score_card(label, value, help_text):
        return f"""
        <div class="metric-card">
            <div class="metric-value">{value:.0f}</div>
            <div class="metric-label">{label}</div>
        </div>
        """
    
    with c1:
        st.markdown(score_card("Logic", scores['logical_consistency_score'], "Coherence & Flow"), unsafe_allow_html=True)
    with c2:
        st.markdown(score_card("Completeness", scores['completeness_score'], "Depth & Steps"), unsafe_allow_html=True)
    with c3:
        st.markdown(score_card("Instruction", scores['instruction_following_score'], "Formatting"), unsafe_allow_html=True)
    with c4:
        st.markdown(score_card("Reliability", scores['hallucination_risk_score'], "Risk Assessment"), unsafe_allow_html=True)

    # Detailed Analysis
    st.divider()
    ana_col1, ana_col2 = st.columns([3, 2])
    
    with ana_col1:
        st.subheader("🔍 Step-by-Step Analysis")
        if not steps:
            st.warning("No clear reasoning steps detected.")
        
        for i, step in enumerate(steps, 1):
            st.markdown(f"""
            <div class="step-container">
                <div class="step-number">Step {i}</div>
                <div class="step-content">{step}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.subheader("💡 Final Answer")
        st.info(parsed['answer'] if parsed['answer'] else "No distinct final answer found in response.")

    with ana_col2:
        st.subheader("🕵️ Evaluation Findings")
        
        if not issues:
            st.markdown("""
            <div class="success-box">
                ✔️ No critical issues detected. The reasoning appears sound and follows logical principles.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.write("Areas for improvement:")
            for issue in issues:
                st.markdown(f"""
                <div class="issue-box">
                    ⚠️ {issue}
                </div>
                """, unsafe_allow_html=True)
        
        if show_raw:
            st.markdown("### Raw Output")
            st.text_area("Full LLM Response", raw_response, height=300)

elif evaluate_btn and not question:
    st.warning("Please enter a question above to start.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 0.8rem;'>ReasonEval System v2.0 • Powered by Ollama</p>", unsafe_allow_html=True)
