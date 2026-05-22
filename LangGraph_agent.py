import os
import json
from pathlib import Path
from typing import List, Dict, Any
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END

class AnalysisState(TypedDict):
    invoice_id: int
    file_name: str
    markdown_content: str
    vendor: str
    amount: float

def parse_invoice_node(state: AnalysisState) -> Dict[str, Any]:
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="openrouter/free",
        temperature=0.0,
        model_kwargs={"response_format": {"type": "json_object"}}
    )
    prompt = ChatPromptTemplate.from_template(
        "Extract the vendor name and total invoice amount from this markdown invoice. "
        "Return valid JSON only with keys \"vendor\" (string) and \"amount\" (float). "
        "If the amount cannot be found or is unclear, return 0.0. Text:\n\n{text}"
    )
    try:
        response = (prompt | llm).invoke({"text": state["markdown_content"]}).content
        data = json.loads(response)
        return {
            "vendor": str(data.get("vendor", "Unknown")),
            "amount": float(data.get("amount", 0.0))
        }
    except Exception:
        return {"vendor": "Unknown", "amount": 0.0}

builder = StateGraph(AnalysisState)
builder.add_node("ParseInvoice", parse_invoice_node)
builder.add_edge(START, "ParseInvoice")
builder.add_edge("ParseInvoice", END)

agent_app = builder.compile()