# langgraph-budget-analyzer

I made this automated budget analyzer to help me track my expenses. To use this, you add all your monthly expense invoices in the pdf_invoices folder. It prompts you to add your monthly budget in the terminal and then it tells you how much of your monthly budget you've exhausted (also with a cool chart) and which your top paid vendors are this month.

It uses LangGraph agents to extract financial metrics from markdown invoices into PostgreSQL with concurrent LLM processing and performance tracking.

