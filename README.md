# 🧠 Agentic Credit Modeling System

Welcome to the **Agentic Credit Modeling System**! This is a modular, explainable AI framework to build credit risk models using agents that collaborate dynamically based on human guidance and regulatory compliance.

## 📦 What This Project Does

This project demonstrates the **first step** in the agentic workflow: **data cleaning**. It uses:

* 🤖 **Developer Agent** – reads human guidance and generates executable data-cleaning code using OpenAI LLM
* 🧑‍⚖️ **Governance Agent** – reads regulatory PDFs (e.g., IFRS 9) and summarizes constraints
* 📄 **Human YAML Guidance** – provides step-by-step task instructions

The system will be expanded later to include:

* 📚 **Documentation Agent** – auto-generates documentation for every modeling step
* 🧠 Retrieval-Augmented Generation (RAG) – for deeper regulatory understanding

---

## 🚀 Quick Start Guide

### ✅ 1. Clone the repository

```bash
git clone https://github.com/your-repo/agentic-credit-model.git
cd agentic-credit-model
```

### 🛠️ 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 📦 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 🔐 4. Set your OpenAI API Key

Create a `.env` file:

```env
OPENAI_API_KEY=your-api-key-here
```

Make sure `.env` is listed in your `.gitignore`.

---

## 📁 Project Structure

```
agentic-credit-model/
├── agents/
│   ├── developer_agent.py         # Developer Agent logic
│   └── governance_agent.py        # Governance Agent logic
├── data/
│   └── sample_credit_data.csv     # Sample data file
├── pdfs/
│   └── ifrs9_excerpt.pdf          # Simulated regulatory input
├── guidance/
│   └── step_1_cleaning.yaml       # Human instructions for this step
├── generated_code/
│   └── step_cleaning_*.py         # LLM-generated cleaning code
├── .env                           # Your OpenAI API Key
├── requirements.txt               # All dependencies
└── main.py                        # Main orchestration script
```

---

## 🧠 Agents in Action

### 👨‍💻 Developer Agent

* Reads: `step_1_cleaning.yaml`
* Consults: Governance Agent
* Uses: GPT-4 via LangChain to generate Python code
* Saves code: `generated_code/step_cleaning_<timestamp>.py`
* Executes it on your input dataset

### ⚖️ Governance Agent

* Reads: `pdfs/ifrs9_excerpt.pdf`
* Extracts relevant regulatory guidance (for now, simple PDF read — future: RAG)
* Provides compliance context to Developer Agent

---

## 🧪 How to Run

### 1. Place your credit data CSV in `/data`

Example: `data/sample_credit_data.csv`

### 2. Edit the YAML guidance

Example: `guidance/step_1_cleaning.yaml`

```yaml
step: data_cleaning
objective: Clean missing values in a compliant manner
constraints: Use median imputation for numeric; do not drop rows
```

### 3. Run the system

```bash
python main.py
```

You’ll see:

* Governance constraints printed
* LLM-generated cleaning code (also saved)
* Executed DataFrame after cleaning

---

## 💡 Example Output

```
🤖 Asking LLM to generate cleaning code...
📝 Code saved to: generated_code/step_cleaning_20250524_101501.py
✅ Code executed successfully.
```

---

## 📌 Notes

* Ensure your PDF (`pdfs/ifrs9_excerpt.pdf`) includes some text about data handling under IFRS 9.
* This is a toy example for now — ideal for testing workflows.
* Later steps will include feature engineering, model training, and validation.

---

## 🔄 Future Extensions

* [ ] Convert Governance Agent to use RAG with vectorstores
* [ ] Add Memory & Tool-using agents via LangChain AgentExecutor
* [ ] Integrate Documentation Agent to track all code and decisions
* [ ] Add Streamlit front-end (Talk to Model-style interface)

---

## 🙌 Contributing

Feel free to fork the repo and submit PRs or issues. Suggestions welcome!

---

## 🧾 License

MIT License

---

## 📬 Questions?

Reach out on [GitHub Discussions](https://github.com/your-repo/agentic-credit-model/discussions) or raise an issue.

---

Happy modeling! 💼📊🤖
