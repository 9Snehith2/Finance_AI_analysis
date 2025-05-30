# 🧠 Multi-Agent Financial Analyst Assistant

This is a multi-agent financial analysis assistant that performs the following tasks:
- Scrapes financial news from a given URL
- Summarizes the article using LLaMA 2 via Ollama
- Retrieves relevant financial context using FAISS
- Makes a final investment-related decision

---

## 🔧 Architecture Overview

The system is composed of the following agents, each running as an independent FastAPI microservice:

| Agent              | Port  | Description                                       |
|-------------------|-------|---------------------------------------------------|
| Scraping Agent     | 8001  | Extracts text from the given URL                 |
| Summarizer Agent   | 8002  | Summarizes article using LLaMA 2 (via Ollama)    |
| Retriever Agent    | 8003  | Searches contextual documents using FAISS        |
| Decision Agent     | 8004  | Makes final decision based on summary and context|
| Orchestrator Agent | 8000  | Orchestrates all agents end-to-end               |
| Streamlit UI       | 8501  | Frontend for user input and output               |

---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/your-username/Finance_AI_analysis.git
cd Finance_AI_analysis
