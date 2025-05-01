# 🤖 RecruitEdge AI  

*Focuses on giving recruiters an edge with AI*

An Intelligent CV Screening and Job Description Matching System for Smarter Pre-Hiring Decisions  
Built using **Python**, **Azure AI Services**, and **Semantic Kernel**


## 🧠 Overview

**RecruitEdge AI** is a multi-agent, AI-powered assistant designed to empower recruiters by automating the most time-consuming parts of early-stage hiring — from generating inclusive job descriptions to parsing resumes, matching candidates, and summarizing public profiles like GitHub.

By combining **LLMs**, **semantic search**, and smart filtering techniques, RecruitEdge AI reduces bias and human error while ensuring the best-fit candidates are identified efficiently. 

---

## 🚨 Problem Statement

Recruiters often miss strong candidates due to limitations of traditional ATS systems, which rely on keyword-based filters and rigid resume structures. Writing inclusive, optimized job descriptions is another manual bottleneck, along with reviewing candidates' online activity across platforms.

**RecruitEdge AI** addresses these gaps through:

- Generating bias-free and role-optimized job descriptions  
- Filtering resumes with intelligent algorithms focused on skill, experience, and relevance  
- Matching resumes and job descriptions using semantic embeddings  
- Auto-summarizing LinkedIn, GitHub, and portfolio links for recruiter convenience  

---

## ⚙️ Technology Stack

- **Language**: Python  
- **Agents & Kernel**: [Microsoft Semantic Kernel](https://aka.ms/SemanticKernel)  
- **AI Services**: Azure OpenAI (LLMs), Azure Functions (optional), GitHub API, Web Scraping  
- **Resume Parsing**: PDF extractors + Regex/NLP logic  
- **Similarity Matching**: Embedding models (e.g., OpenAI text-embedding), Cosine Similarity  
- **Output Presentation**: JSON / Text summaries (for UI/Chatbot use)  

---

## 🧩 Multi-Agent Architecture (Semantic Kernel)

### 💠 Kernel

- Semantic Kernel orchestrates the communication between agents.  
- Functions are defined modularly for different tasks.  
- Plugins include: JobDescriptionGenerator, JDMatcher, WebProfiler.  

### 🔁 Agent Flow

```
+---------------------------+
|        Agent X1M         |
|  JD Generation Assistant |
+---------------------------+
             ↓
+---------------------------+
|        Agent X2M         |
|Resume Parser & JD Matcher|
+---------------------------+
             ↓
+---------------------------+
|        Agent X5IP        |
|   Web Profiler (GitHub)  |
+---------------------------+
```

Each agent can be triggered independently or as part of an automated pipeline.

---

## 🔒 Ethics & Fairness

HireFlow ManagerBot emphasizes **fair hiring**:  
- No hard filters based solely on keywords  
- Considers transferable skills, not just exact matches  
- Highlights underrepresented experience and potential  

---

## 🚀 Future Enhancements

- UI dashboard for recruiters  
- Real-time chatbot assistant (via Azure Bot Service)  
- Slack/Teams integration for notifications  
- Candidate feedback generation  

## 🧪 How to Run

1. Set up Azure OpenAI + API keys  
2. Clone this repo  
3. Install dependencies: 
```bash
pip install -r requirements.txt
```
4. Run kernel orchestrator script:
```bash
python main.py
```
5. Upload resumes and watch the magic ✨
---

```bash
# MS_Hackathon

This is our offical repo for the Microsoft Ai Agent Hackathon Project.


## Requirements

- Github Account
- Python 3.12+
- Azure Subscription
- Azure AI Foundry Account
```
```bash
## Initial Setup

1. Create a virtual environment in the specified directory by running the following command in your terminal:

python -m venv venv
```
2. Activate the virtual environment by running the following command in your terminal:
```bash
venv/scripts/activate
```
3. Create a `.env` file from the `.env.example` file by running the following command in your terminal:
```bash
cp .env.example .env
```
4. Install the Required Packages
Make sure the virtual environment is activated and then run the followning command in your terminal:
```bash
pip install -r requirements.txt
```
## Sign in to Azure using Keyless Authentication

Download **Azure CLI** 

Next, open a terminal and run `az login` or `az login --use-device-code` to sign into your Azure account.

Once you have logged in, select your subscription in the terminal.

## Running the Project
```bash
python main.py
```



