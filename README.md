# 🧠 ReasonEval: Advanced Reasoning Quality Evaluation Engine

> **Assess, Score, and Visualize LLM Reasoning Capabilities with Precision.**

ReasonEval is a production-ready framework designed to evaluate the **quality, depth, and logic** of Large Language Model (LLM) outputs. Unlike simple correctness checks, ReasonEval digs deeper—analyzing the *structure* of thought using **First Principles Thinking** metrics.

---

## 🚀 Key Features

- **🔍 Human-Level Evaluation**: Uses a specialized rule-based engine to score reasoning on 4 dimensions:
  - **Logical Consistency**: Coherence, flow, and contradiction checks.
  - **Completeness**: Step depth and calculation verification.
  - **Instruction Following**: Adherence to strict formatting (First Principles).
  - **Hallucination Risk**: Detection of vague language and unsupported claims.
  
- **📊 Professional Dashboard**: Built with **Streamlit**, offering high-contrast, professional visualization of scores and issues.
- **⚡️ Local & Private**: Powered by **Ollama**, ensuring all data stays on your machine. Zero API costs.
- **🧠 First Principles Prompting**: Forces models to break problems down to fundamental truths before solving.
- **🛡 Self-Verification Logic**: Includes automated self-correction steps to improve accuracy on smaller models (like 1B).

---

## 🛠 Tech Stack

- **Frontend**: Streamlit (Python)
- **Backend**: Flask (API) & Custom Reasoning Engine
- **LLM Engine**: Ollama (Llama 3.2 / 3.1)
- **Language**: Python 3.10+

---

## 📋 Prerequisites

1.  **Python 3.10+** installed.
2.  **Ollama** installed and running. [Download Ollama](https://ollama.ai)

---

## ⚡️ Quick Start

We have streamlined deployment to a single script.

### 1. Clone & Setup
```bash
git clone <repository-url>
cd reasoneval
pip install -r requirements.txt
```

### 2. Launch System
Simply run the helper script. It will auto-start Ollama and the UI.
```bash
./run.sh
```
*The app will open automatically at http://localhost:8501*

---

## 🔧 Configuration

The system is optimized for **Mac M1/M2/M3** by default.

| Setting | Default | Description |
| :--- | :--- | :--- |
| **Model** | `llama3.2:1b` | Lightweight, fast. Good for logic structure. |
| **Alternate** | `llama3.1:8b` | Smarter, usually more accurate, but slower. |

To switch models, edit `config.py`:
```python
OLLAMA_MODEL = "llama3.1:8b" # Uncomment for higher intelligence
```

---

## 🧠 How It Works

1.  **Input**: User asks a complex logic/math question.
2.  **Generation**: The system prompts the local LLM using a **First Principles** template, forcing it to look for axioms and logical steps.
3.  **Parsing**: The `ReasoningParser` extracts the core thought process, ignoring filler.
4.  **Grading**: The `Evaluator` runs the text through 20+ heuristic rules (causal connector usage, assumption checks, etc.).
5.  **Reporting**: The UI displays a **Quality Score (0-100%)** and highlights specific weaknesses (e.g., "Weak causal reasoning").

---

## 📂 Project Structure

```
reasoneval/
├── modules/            # Core Logic
│   ├── evaluator.py    # Scoring Rules
│   ├── llm_client.py   # Ollama Interface
│   └── scorer.py       # Math & Verdicts
├── streamlit_app.py    # Main UI Dashboard
├── app.py              # REST API Service
├── config.py           # System Settings
├── run.sh              # One-Click Launcher
└── requirements.txt    # Dependencies
```

---

*Built for the Future of AI Evaluation.*
