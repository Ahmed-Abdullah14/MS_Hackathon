# 🤖 RecruitEdge AI  

*Focuses on giving recruiters an edge with AI*

An Intelligent CV Screening and Job Description Matching System for Smarter Pre-Hiring Decisions  
Built using **Python**, **Azure AI Services**, and **Semantic Kernel**


## 🧠 Overview

**RecruitEdge AI** is a multi-agent, AI-powered assistant designed to empower recruiters by automating the most time-consuming parts of early-stage hiring — from generating inclusive job descriptions to matching candidates to those job descriptions.

By leveraging the power of **LLMs** and **AI Agents**, RecruitEdge AI reduces bias and human error while ensuring the best-fit candidates are identified efficiently. 

---

## 🚨 Problem Statement

Hiring managers often face the time-consuming task of manually reviewing dozens—or even hundreds—of resumes for a single role. Traditional ATS systems rely heavily on keyword matching, often eliminating strong candidates due to rigid formatting or missing terms.

RecruitEdge AI solves this by using AI agents powered by Large Language Models (LLMs) to intelligently match candidate resumes to job descriptions. This ensures that the hiring manager sees the most relevant candidates first, without having to manually screen every CV, while also reducing the risk of overlooking great talent.

**RecruitEdge AI** addresses these gaps through:

- Generating bias-free and role-optimized job descriptions  
- Intelligently matching resumes and job descriptions using LLM-powered agents for accurate and efficient candidate shortlisting.  

---

## ⚙️ Technology Stack

- **Language**: Python  
- **AI Services**: [Microsoft Semantic Kernel](https://aka.ms/SemanticKernel), Azure OpenAI (LLMs), Chainlit
- **Resume Parsing**: PDF extracting using pdfplumber 
- **Output Presentation**: JSON / Text summaries (for UI/Chatbot use)  

---

## 🧩 Multi-Agent Architecture (Semantic Kernel)

### 💠 Kernel

- Semantic Kernel orchestrates the communication between agents.  
- Functions are defined modularly for different tasks.  
- Plugins include: JobDescriptionGenerator and JDMatcher.  

### 🔁 Agent Flow

```
+---------------------------+
|                           |
|      Manager Agent        |
+---------------------------+
             ↓
+---------------------------+
|                           |
|         JD Agent          |
+---------------------------+
             ↓
+---------------------------+
|                           |
|     JD Matcher Agent      |
+---------------------------+
```

The Manager Agent communicates with the user and manages the other two agents based on the user input.

---

## 🚀 Future Enhancements
  
- Semantic search with vector embeddings for smarter candidate filtering 
- Advanced web profiler for deeper GitHub and LinkedIn insights
- UI dashboard for recruiters
- Auto-generated emails for interviews and hiring steps

## Requirements

- Github Account
- Python 3.12+
- Azure Subscription
- Azure AI Foundry Account

## Initial Setup

1. Create a virtual environment in the specified directory by running the following command in your terminal:
```bash
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
5. Upload resumes in the data/resume folders or use the sample already resumes provided.

## Sign in to Azure using Keyless Authentication

Download **Azure CLI** 

Next, open a terminal and run `az login` to sign into your Azure account.

Once you have logged in, select your subscription in the terminal.

## Running the Project


```bash
python main.py
```



