import os
from rich.console import Console
from rich.panel import Panel

from modules.phone import phone_lookup
from modules.email import email_lookup
from modules.domain import domain_lookup
from modules.username import username_lookup

console = Console()

def save_report(data):
    os.makedirs("reports", exist_ok=True)

    filename = "reports/report.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)

    console.print("[green]Report saved:[/green] reports/report.txt")

def menu():

    while True:

        console.print(Panel.fit("Advanced OSINT Toolkit"))

        console.print("1 - Phone Lookup")
        console.print("2 - Email Lookup")
        console.print("3 - Domain Lookup")
        console.print("4 - Username Check")
        console.print("5 - Exit")

        choice = input("Select: ").strip()

        result = ""

        if choice == "1":
            target = input("Phone Number: ")
            result = phone_lookup(target)

        elif choice == "2":
            target = input("Email: ")
            result = email_lookup(target)

        elif choice == "3":
            target = input("Domain: ")
            result = domain_lookup(target)

        elif choice == "4":
            target = input("Username: ")
            result = username_lookup(target)

        elif choice == "5":
            break

        else:
            console.print("[red]Invalid choice[/red]")
            continue

        console.print(result)
        save_report(result)

if __name__ == "__main__":
    menu()
