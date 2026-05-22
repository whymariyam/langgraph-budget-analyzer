# LangGraph Invoice/Budget Analyzer

I made this automated budget analyzer to help me track my expenses. To use this, you add all your monthly/yearly expense invoices in the pdf_invoices folder. It prompts you to add your monthly/yearly budget in the terminal and then it tells you how much of your monthly budget you've exhausted (also with a cool chart) and which your top paid vendors are this month.

It uses LangGraph agents to extract financial metrics from markdown invoices into PostgreSQL with concurrent LLM processing and performance tracking.

# Prerequisites

Before starting, ensure you have the following installed:

Python 3.10+
PostgreSQL 14+ (running locally or via a cloud provider)
pip and venv
An OpenRouter account and API key

# Installation

Clone the repository, Create and Activate a Virtual Environment (Ubuntu)
```bash
git clone https://github.com/whymariyam/langgraph-budget-analyzer.git
cd langgraph-budget-analyzer
bashpython -m venv venv
source venv/bin/activate
```

Install dependencies
```bash
pip install -r requirements.txt
```

