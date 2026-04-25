# 🩺 MediScan AI — Lab Report Analyzer

<p align="center">
  <b>AI-powered health report analysis with instant insights, structured advice, and smart chatbot assistance.</b>
</p>

<p align="center">
  📄 Text • 🖼 Image • 📑 PDF → 📊 Insights • 🧠 AI Advice • 💬 Chatbot
</p>

---

## 🚀 Badges

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge" />
  
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" />
</p>

---

## 🚀 Overview

MediScan AI is an intelligent healthcare application that analyzes lab reports from text, images, and PDFs. It extracts medical parameters, evaluates them, and generates structured explanations along with personalized health recommendations and a context-aware AI chatbot.

---

## ✨ Features

- 📄 **Multi-Input Support** — Text, Image, and PDF uploads
- 🤖 **AI Parameter Extraction** — Automatically detects medical values
- 📊 **Smart Analysis Engine** — Classifies values (High / Low / Normal)
- 🧠 **AI Summary & Advice** — Diet, Lifestyle, Precautions
- 💬 **AI Chatbot** — Context-aware responses based on report
- 🎨 **Modern UI** — Clean Streamlit interface
- 🛡 **Safety Guardrails** — Prevents unsafe outputs

---

## 🛠 Tech Stack

- **Frontend** — Streamlit, HTML/CSS
- **Backend** — Python
- **AI** — Groq API (`openai/gpt-oss-120b`)
- **Processing** — OCR (image & PDF extraction), JSON parsing

---

## 📂 Project Structure

lab-report-analysis/
│
├── .env                        ← API keys (gitignored)
├── .env.example                ← template for new devs
├── .gitignore
├── requirements.txt
├── README.md
├── prompts.py                  ← LLM prompt templates
│
├── chatbot/
│   └── memory.py               ← chat history trim + summarize
│
├── utils/
│   ├── ai_extractor.py         ← LLM-based parameter extraction
│   ├── extractor.py            ← PDF + image text extraction
│   └── parser.py               ← parameter analysis + reference ranges
│
└── frontend/
    ├── streamlit_app.py        ← entry point + router
    ├── db.py                   ← SQLite (users + reports)
    ├── auth_ui.py              ← login / signup UI
    ├── mediscan.db             ← SQLite database (gitignored)
    │
    ├── components/
    │   ├── helpers.py          ← AI helpers, chat, markdown formatter
    │   └── styles.py           ← theme tokens + CSS injection
    │
    └── page_modules/
        ├── landing.py          ← hero + features
        ├── dashboard.py        ← upload, analyse, results, chat
        ├── history.py          ← report history list
        ├── analytics.py        ← stats overview
        ├── reports.py          ← saved report viewer
        └── settings.py         ← account info
```

```

---

## ⚙️ Setup & Installation

### 1. Install Python
Make sure you have **Python 3.10+** installed. Download from [python.org](https://www.python.org/downloads/).

### 2. Install dependencies
Open a terminal in the project folder and run:
```bash
pip install -r requirements.txt
```

### 3. 🔑 Add your API Key (important!)
The project needs a Groq API key to work.

**Step 1** — Get a free API key from [console.groq.com](https://console.groq.com)
- Sign up / log in
- Go to **API Keys** → click **Create API Key**
- Copy the key

**Step 2** — Create a file named `.env` in the **root of the project folder** (same level as `app.py`):

```
lab-report-analysis-tool/   ← project root
├── .env                    ← create this file here
├── app.py
├── frontend/
...
```

**Step 3** — Open the `.env` file and paste this inside:
```
GROQ_API_KEY=your_api_key_here
```
Replace `your_api_key_here` with the key you copied.

> ⚠️ Do **not** share or upload this file. It's already in `.gitignore`.

---

## ▶️ Run the App

```bash
streamlit run frontend/streamlit_app.py
```

Then open your browser at **http://localhost:8501**

---

## 📌 Usage

1. **Analyze Report** — Select input type (Text / Image / PDF), upload or paste your report, click Analyze
2. **View Results** — See parameter breakdown and AI summary
3. **Chat with AI** — Ask health-related questions based on your report

---

## 🛡 Guardrails

- ❌ No diagnosis
- ❌ No medicines
- ❌ No hallucinated data
- ✅ Only uses report data
- ✅ Rejects non-medical inputs

---

## ⚠️ Disclaimer

This tool is for informational purposes only and does not replace professional medical advice.

---

## 👨‍💻 Authors

Akshat Acharya, Praduman Dadhich and Krish Lenjhara

---

## ⭐ Support

If you like this project: ⭐ Star it • 🍴 Fork it • 🚀 Contribute
