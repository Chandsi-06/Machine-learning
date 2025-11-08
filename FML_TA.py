"""
Expense Tracker CLI
Author: ChatGPT (GPT-5 Thinking mini)
Description:
A simple command-line expense tracker for hackathon submission.
It supports:
 - add: add an expense (amount, category, note)
 - list: list all expenses
 - report: show total and by-category sums
 - export: export to CSV
Data is stored in a local JSON file named 'expenses.json' in the same folder.
Usage examples:
  python solution.py add 12.50 Food "lunch at cafe"
  python solution.py list
  python solution.py report
  python solution.py export expenses.csv
"""

import sys
import json
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
import csv

DATA_FILE = Path(__file__).with_name("expenses.json")

def load_expenses():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_expenses(expenses):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2, ensure_ascii=False)

def add_expense(amount, category, note=""):
    try:
        amt = float(Decimal(amount))
    except (InvalidOperation, ValueError):
        print("Invalid amount format. Use a number like 12.50")
        return
    entry = {
        "id": int(datetime.utcnow().timestamp()*1000),
        "amount": amt,
        "category": category,
        "note": note,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    expenses = load_expenses()
    expenses.append(entry)
    save_expenses(expenses)
    print("Expense added:")
    print(entry)

def list_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return
    for e in sorted(expenses, key=lambda x: x["timestamp"], reverse=True):
        ts = e["timestamp"]
        print(f'{e["id"]} | {ts} | {e["category"]:12} | ₹{e["amount"]:.2f} | {e["note"]}')

def report():
    expenses = load_expenses()
    total = sum(e["amount"] for e in expenses)
    by_cat = {}
    for e in expenses:
        by_cat[e["category"]] = by_cat.get(e["category"], 0) + e["amount"]
    print(f"Total expenses: ₹{total:.2f}")
    print("By category:")
    for cat, s in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"  {cat:12} : ₹{s:.2f}")

def export_csv(filename):
    expenses = load_expenses()
    if not expenses:
        print("No expenses to export.")
        return
    keys = ["id", "timestamp", "category", "amount", "note"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for e in expenses:
            writer.writerow({k:e.get(k,"") for k in keys})
    print(f"Exported {len(expenses)} records to {filename}")

def help_text():
    print(__doc__)

def main(argv):
    if len(argv) < 2:
        help_text()
        return
    cmd = argv[1].lower()
    if cmd == "add":
        if len(argv) < 4:
            print("Usage: python solution.py add <amount> <category> [note]")
            return
        amount = argv[2]
        category = argv[3]
        note = " ".join(argv[4:]) if len(argv) > 4 else ""
        add_expense(amount, category, note)
    elif cmd == "list":
        list_expenses()
    elif cmd == "report":
        report()
    elif cmd == "export":
        if len(argv) < 3:
            print("Usage: python solution.py export <filename.csv>")
            return
        export_csv(argv[2])
    else:
        help_text()

if __name__ == "__main__":
    main(sys.argv)
