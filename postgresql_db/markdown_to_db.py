import os
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

base_dir = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=base_dir / ".env")

#I've saved these values in the .env file in my base directory (you can give them ur desired name and pass)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS processed_invoices (
            id SERIAL PRIMARY KEY,
            file_name TEXT UNIQUE NOT NULL,
            markdown_content TEXT NOT NULL,
            vendor TEXT,
            amount NUMERIC(12, 2),
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


def save_markdown_to_db(output_folder: str):
    output_path = Path(output_folder)
    conn = get_db_connection()
    cur = conn.cursor()

    for md_file in output_path.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            cur.execute("""
                INSERT INTO processed_invoices (file_name, markdown_content)
                VALUES (%s, %s)
                ON CONFLICT (file_name)
                DO UPDATE SET markdown_content = EXCLUDED.markdown_content;
            """, (md_file.name, content))
        except Exception:
            conn.rollback()
        else:
            conn.commit()

    cur.close()
    conn.close()

if __name__ == "__main__":
    init_db()
    save_markdown_to_db(str(base_dir / "markdown_invoices"))
