"""
Configuration settings for ReasonEval system
"""

# Ollama Configuration
OLLAMA_MODEL = "llama3.2:1b"  # Smaller model for faster download (~1GB vs 4.9GB)
OLLAMA_API_BASE = "http://localhost:11434"
OLLAMA_TIMEOUT = 120  # seconds

# Flask Configuration
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5001
FLASK_DEBUG = True

# Logging Configuration
LOG_FILE_PATH = "logs/evaluations.csv"

# Scoring Configuration
SCORING_WEIGHTS = {
    "logical_consistency": 0.35,
    "completeness": 0.25,
    "instruction_following": 0.20,
    "hallucination_risk": 0.20  # This will be inverted (lower is better)
}

# Verdict threshold (0-100)
GOOD_REASONING_THRESHOLD = 70

# LLM Prompt Template
LLM_PROMPT_TEMPLATE = """You are an expert reasoner. Solve the following question using First Principles Thinking.

Question: {question}

Guidance:
1. Break the problem down to its fundamental truths.
2. Reason upwards from there, step-by-step.
3. Explicitly state your assumptions and logical connections.
4. Avoid using analogies; focus on the core logic.
5. Verify your final answer by checking if it makes sense contextually.

Format your response exactly as follows:
REASONING:
1. First, [Foundational Truth / Definition].
2. Next, [Deduction from Step 1].
3. Then, [Further logical step].
...
Final Step, [Conclusion].

FINAL ANSWER:
[Your final concise answer]

Example:
Question: Is a tomato a fruit or vegetable?
REASONING:
1. First, we define a fruit biologically as the part of a plant that develops from a flower and contains seeds.
2. Next, we observe that a tomato grows from the flower of the tomato plant.
3. Then, we check the inside of a tomato and find seeds.
4. Therefore, biologically, a tomato fits the definition of a fruit.
5. However, culinarily, we define vegetables by their savory taste and use in main dishes.
6. Since a tomato is savory and used in salads/sauces, it is culinarily treated as a vegetable.

FINAL ANSWER:
Biologically a fruit, culinarily a vegetable."""
