import os
import sys
from pathlib import Path
import psycopg2
from dotenv import load_dotenv
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from LangGraph_agent import agent_app
from visualization import generate_budget_chart

base_dir = Path(__file__).resolve().parent
load_dotenv(dotenv_path=base_dir / ".env")


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )


def fetch_unprocessed_invoices(conn) -> list:
    cur = conn.cursor()
    cur.execute("""
        SELECT id, file_name, markdown_content 
        FROM processed_invoices 
        WHERE vendor IS NULL OR amount IS NULL;
    """)
    rows = cur.fetchall()
    cur.close()
    return rows


def update_invoice_data(invoice_id: int, vendor: str, amount: float):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE processed_invoices 
            SET vendor = %s, amount = %s 
            WHERE id = %s;
        """, (vendor, amount, invoice_id))
        conn.commit()
    except Exception:
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def get_budget_summary(conn) -> tuple:
    cur = conn.cursor()
    cur.execute("""
        SELECT COALESCE(SUM(amount), 0.0) 
        FROM processed_invoices;
    """)
    total_spent = float(cur.fetchone()[0])

    cur.execute("""
        SELECT file_name, vendor, amount 
        FROM processed_invoices 
        WHERE amount IS NOT NULL AND amount > 0 
        ORDER BY amount DESC;
    """)
    top_invoices = cur.fetchall()
    cur.close()
    return total_spent, top_invoices


def process_single_invoice(invoice):
    invoice_id, file_name, content = invoice
    try:
        state_input = {
            "invoice_id": invoice_id,
            "file_name": file_name,
            "markdown_content": content,
            "vendor": "",
            "amount": 0.0
        }
        output = agent_app.invoke(state_input)
        update_invoice_data(invoice_id, output["vendor"], output["amount"])
    except Exception:
        pass


def main():
    try:
        yearly_budget_input = input("Enter your yearly budget (USD): ").strip()
        yearly_budget = float(yearly_budget_input)
    except ValueError:
        print("Invalid budget input. Please enter a numerical value.", file=sys.stderr)
        return

    try:
        conn = get_db_connection()
    except Exception as e:
        print(f"Database connection failed: {e}", file=sys.stderr)
        return

    unprocessed = fetch_unprocessed_invoices(conn)
    if unprocessed:
        print(f"Processing {len(unprocessed)} invoices concurrently with LLM agent...")

        max_workers = 10

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_single_invoice, inv) for inv in unprocessed]
            for _ in tqdm(as_completed(futures), total=len(futures), desc="Analyzing Invoices", unit="inv"):
                pass

    total_spent, top_invoices = get_budget_summary(conn)
    remaining_balance = yearly_budget - total_spent

    print("\n" + "=" * 40)
    print(" BUDGET ANALYSIS REPORT")
    print("=" * 40)
    print(f"Yearly Budget:       ${yearly_budget:,.2f}")
    print(f"Total Expenses:      ${total_spent:,.2f}")
    print(f"Remaining Balance:   ${remaining_balance:,.2f}")
    print("-" * 40)

    if remaining_balance >= 0:
        print("Status: UNDER BUDGET")
    else:
        print("Status: OVER BUDGET")

    print("\nTOP MOST EXPENSIVE INVOICES:")
    print(f"{'File Name':<30} | {'Vendor':<20} | {'Amount':<12}")
    print("-" * 68)
    for file_name, vendor, amount in top_invoices:
        print(f"{file_name[:30]:<30} | {str(vendor)[:20]:<20} | ${float(amount):<11,.2f}")

    try:
        chart_output = str(base_dir / "budget_chart.png")
        generate_budget_chart(yearly_budget, total_spent, remaining_balance, chart_output)
        print(f"\nVisualization chart saved to: {chart_output}")
    except Exception as e:
        print(f"\nCould not generate visualization chart: {e}", file=sys.stderr)

    conn.close()


if __name__ == "__main__":
    main()