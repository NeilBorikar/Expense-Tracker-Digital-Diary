"""
───────────────────────────────────────────────
 🧠 DIGITAL DIARY X — The God-Level Expense Tracker
───────────────────────────────────────────────
Features:
✔ Write & View Diary Entries
✔ Add, View, and Filter Expenses
✔ Expense Reports by Category, Date, or Range
✔ Total Expense Summary
✔ Persistent JSON-based Storage
✔ Clean OOP Design with Error Handling
✔ Beautiful CLI with Rich Library

Author: Neil ⚡
───────────────────────────────────────────────
"""

import json
import os
from datetime import datetime, date
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, FloatPrompt, IntPrompt

console = Console()

# ============================================================
#                      DATA MODELS
# ============================================================

class Expense:
    """Represents a single expense entry."""
    def __init__(self, category: str, amount: float, date_str: str = None):
        self.category = category.strip().title()
        self.amount = round(amount, 2)
        self.date = date_str or date.today().isoformat()

    def __repr__(self):
        return f"[{self.date}] {self.category}: ₹{self.amount:.2f}"

    def to_dict(self):
        return {"category": self.category, "amount": self.amount, "date": self.date}


class DigitalDiaryX:
    """God-level Digital Diary + Expense Tracker."""
    DIARY_FILE = "diary_entries.txt"
    EXPENSE_FILE = "expenses.json"

    def __init__(self):
        self.expenses = []
        self.load_expenses()

    # ============================================================
    #                      MAIN MENU
    # ============================================================
    def start(self):
        while True:
            console.print("\n[bold cyan]=== DIGITAL DIARY X ===[/bold cyan]")
            console.print("1️⃣  Write New Diary Entry")
            console.print("2️⃣  View All Diary Entries")
            console.print("3️⃣  Add New Expense")
            console.print("4️⃣  View All Expenses")
            console.print("5️⃣  Expense Reports")
            console.print("6️⃣  Show Total Expenses")
            console.print("7️⃣  Exit")
            choice = Prompt.ask("\nChoose an option", choices=[str(i) for i in range(1, 8)])

            try:
                match choice:
                    case "1": self.write_diary_entry()
                    case "2": self.view_diary_entries()
                    case "3": self.add_expense()
                    case "4": self.view_all_expenses()
                    case "5": self.expense_reports()
                    case "6": self.show_total_expenses()
                    case "7":
                        self.save_expenses()
                        console.print("\n💾 [green]All data saved. Goodbye, legend![/green]")
                        break
            except Exception as e:
                console.print(f"[red]✗ Unexpected error:[/red] {e}")

    # ============================================================
    #                  DIARY OPERATIONS
    # ============================================================
    def write_diary_entry(self):
        console.print("\n📝 [bold]Enter your diary entry (type 'END' on a new line to finish):[/bold]")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)

        entry_text = "\n".join(lines).strip()
        if not entry_text:
            console.print("[yellow]No entry written. Returning to menu...[/yellow]")
            return

        with open(self.DIARY_FILE, "a", encoding="utf-8") as f:
            f.write(f"=== Entry [{date.today()}] ===\n{entry_text}\n=====================\n\n")
        console.print("[green]✓ Diary entry saved successfully![/green]")

    def view_diary_entries(self):
        console.print("\n📖 [bold cyan]Your Diary Entries[/bold cyan]\n")
        if not os.path.exists(self.DIARY_FILE):
            console.print("[yellow]No diary entries found yet![/yellow]")
            return
        with open(self.DIARY_FILE, "r", encoding="utf-8") as f:
            console.print(f.read())

    # ============================================================
    #                  EXPENSE OPERATIONS
    # ============================================================
    def add_expense(self):
        category = Prompt.ask("Enter expense category").strip().title()
        amount = FloatPrompt.ask("Enter expense amount (₹)")
        expense = Expense(category, amount)
        self.expenses.append(expense)
        self.save_expenses()
        console.print(f"[green]✓ Added:[/green] {expense}")

    def view_all_expenses(self):
        if not self.expenses:
            console.print("[yellow]No expenses recorded yet.[/yellow]")
            return

        table = Table(title="💸 All Expenses", show_header=True, header_style="bold magenta")
        table.add_column("Date", style="cyan")
        table.add_column("Category", style="green")
        table.add_column("Amount (₹)", justify="right")

        for exp in self.expenses:
            table.add_row(exp.date, exp.category, f"{exp.amount:.2f}")
        console.print(table)

    def expense_reports(self):
        if not self.expenses:
            console.print("[yellow]No expenses to report.[/yellow]")
            return

        console.print("\n📊 [bold cyan]Expense Report Options:[/bold cyan]")
        console.print("1️⃣  View by Category")
        console.print("2️⃣  View by Date")
        console.print("3️⃣  View by Amount Range")

        choice = Prompt.ask("Choose report type", choices=["1", "2", "3"])
        match choice:
            case "1":
                category = Prompt.ask("Enter category to filter").strip().title()
                filtered = [e for e in self.expenses if e.category == category]
                self.display_filtered_expenses(filtered, f"Category: {category}")
            case "2":
                date_str = Prompt.ask("Enter date (YYYY-MM-DD)")
                filtered = [e for e in self.expenses if e.date == date_str]
                self.display_filtered_expenses(filtered, f"Date: {date_str}")
            case "3":
                min_amt = FloatPrompt.ask("Enter minimum amount (₹)")
                max_amt = FloatPrompt.ask("Enter maximum amount (₹)")
                filtered = [e for e in self.expenses if min_amt <= e.amount <= max_amt]
                self.display_filtered_expenses(filtered, f"Range: ₹{min_amt:.2f} - ₹{max_amt:.2f}")

    def display_filtered_expenses(self, filtered, title):
        if not filtered:
            console.print(f"[yellow]No results found for {title}[/yellow]")
            return

        table = Table(title=f"📘 Expenses - {title}", show_header=True, header_style="bold magenta")
        table.add_column("Date", style="cyan")
        table.add_column("Category", style="green")
        table.add_column("Amount (₹)", justify="right")

        for e in filtered:
            table.add_row(e.date, e.category, f"{e.amount:.2f}")
        console.print(table)

    def show_total_expenses(self):
        total = sum(e.amount for e in self.expenses)
        console.print(f"\n💰 [bold green]Total Expenses: ₹{total:.2f}[/bold green]")

    # ============================================================
    #                 FILE HANDLING OPERATIONS
    # ============================================================
    def load_expenses(self):
        if not os.path.exists(self.EXPENSE_FILE):
            return
        try:
            with open(self.EXPENSE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.expenses = [Expense(**item) for item in data]
        except Exception as e:
            console.print(f"[red]✗ Error loading expenses:[/red] {e}")

    def save_expenses(self):
        try:
            with open(self.EXPENSE_FILE, "w", encoding="utf-8") as f:
                json.dump([e.to_dict() for e in self.expenses], f, indent=4)
        except Exception as e:
            console.print(f"[red]✗ Error saving expenses:[/red] {e}")


# ============================================================
#                        ENTRY POINT
# ============================================================
if __name__ == "__main__":
    app = DigitalDiaryX()
    app.start()
