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
✔ Optional Browser-Based Frontend

Author: Neil ⚡
───────────────────────────────────────────────
"""

import json
import math
import os
import re
import sys
from datetime import datetime, date
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
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
                self.expenses = [
                    Expense(item["category"], item["amount"], item.get("date"))
                    for item in data
                ]
        except Exception as e:
            console.print(f"[red]✗ Error loading expenses:[/red] {e}")

    def save_expenses(self):
        with open(self.EXPENSE_FILE, "w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in self.expenses], f, indent=4)


def create_web_server(app, host="127.0.0.1", port=8000):
    class DiaryRequestHandler(BaseHTTPRequestHandler):
        def send_json(self, status, payload):
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def read_json(self):
            try:
                content_length = int(self.headers.get("Content-Length", "0"))
            except ValueError as error:
                raise ValueError("Invalid Content-Length header.") from error
            if content_length <= 0 or content_length > 1_000_000:
                raise ValueError("Request body must be between 1 byte and 1 MB.")
            try:
                return json.loads(self.rfile.read(content_length))
            except (json.JSONDecodeError, UnicodeDecodeError) as error:
                raise ValueError("Request body must contain valid JSON.") from error

        def do_GET(self):
            if self.path == "/":
                try:
                    body = Path(__file__).with_name("index.html").read_bytes()
                except OSError:
                    self.send_error(500, "Could not read the frontend file.")
                    return
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            if self.path == "/api/expenses":
                self.send_json(200, [expense.to_dict() for expense in app.expenses])
                return

            if self.path == "/api/diary":
                entries = []
                if os.path.exists(app.DIARY_FILE):
                    with open(app.DIARY_FILE, "r", encoding="utf-8") as diary_file:
                        contents = diary_file.read()
                    pattern = r"=== Entry \[(.*?)\] ===\n(.*?)\n====================="
                    entries = [
                        {"date": entry_date, "text": text}
                        for entry_date, text in re.findall(pattern, contents, re.DOTALL)
                    ]
                self.send_json(200, entries)
                return

            self.send_error(404, "Not found.")

        def do_POST(self):
            try:
                payload = self.read_json()
                if not isinstance(payload, dict):
                    raise ValueError("Request body must be a JSON object.")

                if self.path == "/api/expenses":
                    category = payload.get("category")
                    amount = payload.get("amount")
                    expense_date = payload.get("date", date.today().isoformat())
                    if not isinstance(category, str) or not category.strip():
                        raise ValueError("Category is required.")
                    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
                        raise ValueError("Amount must be a positive number.")
                    try:
                        amount = float(amount)
                    except (OverflowError, ValueError) as error:
                        raise ValueError("Amount must be a positive number.") from error
                    if not math.isfinite(amount) or amount <= 0:
                        raise ValueError("Amount must be a positive number.")
                    if not isinstance(expense_date, str):
                        raise ValueError("Date must use YYYY-MM-DD format.")
                    try:
                        datetime.strptime(expense_date, "%Y-%m-%d")
                    except ValueError as error:
                        raise ValueError("Date must use YYYY-MM-DD format.") from error

                    expense = Expense(category, amount, expense_date)
                    app.expenses.append(expense)
                    try:
                        app.save_expenses()
                    except OSError:
                        app.expenses.pop()
                        raise
                    self.send_json(201, expense.to_dict())
                    return

                if self.path == "/api/diary":
                    text = payload.get("text")
                    if not isinstance(text, str) or not text.strip():
                        raise ValueError("Diary entry cannot be empty.")
                    entry_date = date.today().isoformat()
                    with open(app.DIARY_FILE, "a", encoding="utf-8") as diary_file:
                        diary_file.write(
                            f"=== Entry [{entry_date}] ===\n{text.strip()}\n"
                            "=====================\n\n"
                        )
                    self.send_json(201, {"date": entry_date, "text": text.strip()})
                    return

                self.send_error(404, "Not found.")
            except ValueError as error:
                self.send_json(400, {"error": str(error)})
            except OSError as error:
                self.send_error(500, f"Could not save data: {error}")

        def log_message(self, format_string, *args):
            console.print(f"[dim]Web: {format_string % args}[/dim]")

    return HTTPServer((host, port), DiaryRequestHandler)


def start_web_frontend(app, host="127.0.0.1", port=8000):
    server = create_web_server(app, host, port)
    console.print(f"[bold green]Digital Diary is ready at http://{host}:{server.server_port}[/bold green]")
    console.print("[dim]Press Ctrl+C to stop the web server.[/dim]")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        console.print("\n[yellow]Web server stopped.[/yellow]")
    finally:
        server.server_close()


# ============================================================
#                        ENTRY POINT
# ============================================================
if __name__ == "__main__":
    app = DigitalDiaryX()
    if len(sys.argv) > 1 and sys.argv[1] == "--web":
        start_web_frontend(app)
    else:
        app.start()
