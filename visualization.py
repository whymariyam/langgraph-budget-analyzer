import os
from pathlib import Path
import matplotlib.pyplot as plt


def generate_budget_chart(total_budget: float, spent: float, remaining: float, output_path: str):
    categories = ['Yearly Budget', 'Total Expenses', 'Remaining Balance']
    values = [total_budget, spent, remaining]
    colors = ['#2ecc71', '#e74c3c', '#3498db'] if remaining >= 0 else ['#2ecc71', '#e74c3c', '#95a5a6']

    plt.figure(figsize=(8, 5))
    bars = plt.bar(categories, values, color=colors, width=0.5)
    plt.title("Yearly Budget vs Operational Expenses", fontsize=12, fontweight='bold')
    plt.ylabel("USD ($)", fontsize=10)

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + (total_budget * 0.01),
            f"${height:,.2f}",
            ha='center',
            va='bottom',
            fontweight='bold'
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()