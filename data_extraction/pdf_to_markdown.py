import os
import re
from pathlib import Path
import fitz

def clean_extracted_text(text: str) -> str:
    text = re.sub(r'\r\n', '\n', text)
    lines = [line.strip() for line in text.split('\n')]
    return '\n'.join([line for line in lines if line])

def parse_pdf_to_markdown(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    md_content = [f"# Invoice: {pdf_path.stem}\n"]

    for page_num, page in enumerate(doc, start=1):
        text_blocks = page.get_text("blocks")
        text_blocks.sort(key=lambda b: (b[1], b[0]))

        for block in text_blocks:
            block_text = block[4].strip()
            if not block_text:
                continue
            if any(kwd in block_text.lower() for kwd in ["total", "invoice no", "amount", "due", "balance"]):
                md_content.append(f"\n**{block_text}**\n")
            else:
                md_content.append(f"\n{block_text}\n")

    return clean_extracted_text("\n".join(md_content))

def execute_extraction(input_folder: str, output_folder: str):
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    for pdf_file in input_path.glob("*.pdf"):
        try:
            markdown_text = parse_pdf_to_markdown(pdf_file)
            md_file_path = output_path / f"{pdf_file.stem}.md"
            md_file_path.write_text(markdown_text, encoding="utf-8")
        except Exception:
            pass

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    execute_extraction(
        input_folder=str(base_dir / "pdf_invoices"),
        output_folder=str(base_dir / "markdown_invoices")
    )
