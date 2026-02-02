# 🚀 Quick Start - ReasonEval with Streamlit UI

## ✅ System is Ready!

Your ReasonEval system is **fully functional** and running!

## 🌐 Access the Web Interface

**Open your browser and go to:**
```
http://localhost:8501
```

Or click this link if your browser is open: http://localhost:8501

## 📝 How to Use

1. **Enter your question** in the text area
   - Example: "If a train travels 60 km in 45 minutes, what is its speed in km/h?"

2. **Click "🚀 Evaluate Reasoning"**

3. **Wait for results** (first time will download the model - takes a few minutes)

4. **View the evaluation:**
   - ✅ Final Answer
   - 📊 Scores (Logical Consistency, Completeness, etc.)
   - 🔍 Reasoning Steps
   - ⚠️ Detected Issues
   - 🎯 Overall Verdict

## ⚙️ What's Running

You have **3 processes** running:

1. **Ollama Server** - Provides the LLM (llama3.2:1b)
2. **Streamlit UI** - Web interface on port 8501
3. **Model Download** - Downloading llama3.2:1b (~1GB, faster than 8B)

## 💡 Tips

- **First question takes longer** - model needs to download first time
- **Use step-by-step questions** - get better reasoning evaluation
- **Check the sidebar** - toggle options for raw response and detailed scores
- **All evaluations are logged** - check `logs/evaluations.csv`

## 🎨 UI Features

- Beautiful gradient design
- Real-time evaluation
- Interactive score visualization
- Step-by-step reasoning display
- Issue highlighting
- Raw LLM response viewer

## 📊 Example Questions to Try

```
1. What is 25 × 4?

2. If a book costs $12 and I have $50, how many books can I buy?

3. If all cats are mammals and all mammals are animals, are all cats animals?

4. A train travels 120 km in 2 hours. What is its average speed?
```

## 🎉 You're All Set!

Just open **http://localhost:8501** in your browser and start evaluating!

---

**Note:** Keep the terminal windows running. Don't close them or the system will stop.
