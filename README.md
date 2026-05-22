# LangGraph Invoice/Budget Analyzer

I made this automated budget analyzer to help me track my expenses. To use this, you add all your yearly expense invoices in the pdf_invoices folder. It prompts you to add your yearly budget in the terminal and then it tells you how much of your monthly budget you've exhausted (also with a cool chart) and which your top paid vendors are this month.

It uses a **LangGraph** agent to extract financial metrics from markdown invoices into PostgreSQL with **concurrent LLM processing** and performance tracking.

## Visual

![Alt text description](budget_chart.png)

## Final Output

![Alt text description](terminal_output.png)

## Prerequisites

Before starting, ensure you have the following installed:

• Python 3.10+
• PostgreSQL 14+ (running locally or via a cloud provider)
• pip and venv
• An OpenRouter account and API key

## Installation

Clone the repository, Create and Activate a Virtual Environment (Ubuntu)
```bash
git clone https://github.com/whymariyam/langgraph-budget-analyzer.git
cd langgraph-budget-analyzer
python3 -m venv venv
source venv/bin/activate
```

Install dependencies
```bash
pip install -r requirements.txt
```
## Creating Secret Variables

Populate your .env file
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=budget_analyzer #you may choose a different one
DB_USER=your_postgres_user #you may choose a different one
DB_PASSWORD=your_postgres_password #you may choose a different one
OPENROUTER_API_KEY=your_openrouter_api_key
# Optional: Define your preferred routing model
LLM_MODEL=meta-llama/llama-3-70b-instruct:free #you may choose a different one
```

## PDF Addition

Create a pdf_invoices folder in your project's base directory and drop your target invoices inside
```bash
mkdir pdf_invoices
#move your files into the directory
```

Run the scripts in this order
```bash
python3 pdf_to_markdown.py
python3 markdown_to_db.py
python3 LangGraph_agent.py
python3 visualization.py
python3 main.py
#make sure you're in the respective directory

```



