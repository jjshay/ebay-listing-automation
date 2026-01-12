#!/usr/bin/env python3
"""Marketing Demo - eBay Listing Automation"""
import time
import sys

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich import box
    console = Console()
except ImportError:
    print("Run: pip install rich")
    sys.exit(1)

def pause(seconds=2):
    time.sleep(seconds)

def clear():
    console.clear()

# SCENE 1: Hook
clear()
console.print("\n" * 5)
console.print("[bold yellow]         STILL WRITING EBAY LISTINGS BY HAND?[/bold yellow]", justify="center")
pause(2)

# SCENE 2: Problem
clear()
console.print("\n" * 3)
console.print(Panel("""
[bold red]YOU'RE WASTING HOURS:[/bold red]

   • 15 minutes per listing
   • Copy-pasting the same fields
   • Guessing prices
   • Writing descriptions from scratch

[dim]There's a faster way.[/dim]
""", title="❌ Manual Listings = Lost Time", border_style="red", width=60), justify="center")
pause(3)

# SCENE 3: Solution
clear()
console.print("\n" * 3)
console.print(Panel("""
[bold green]DROP AN IMAGE. GET A LISTING.[/bold green]

   ✓ AI reads your product image
   ✓ Auto-generates title & description
   ✓ Suggests optimal price
   ✓ Uploads directly to eBay

[bold]From photo to LIVE in 30 seconds.[/bold]
""", title="✅ eBay Listing Automation", border_style="green", width=60), justify="center")
pause(3)

# SCENE 4: Example
clear()
console.print("\n\n")
console.print("[bold cyan]              📸 WATCH THE MAGIC[/bold cyan]", justify="center")
console.print()
pause(1)

console.print("[dim]                 Dropping image...[/dim]", justify="center")
pause(1)
console.print("[bold white]                 shepard-fairey-hope.jpg[/bold white]", justify="center")
pause(2)

# SCENE 5: AI Analysis
clear()
console.print("\n\n")
console.print("[bold magenta]              🤖 AI ANALYZING IMAGE...[/bold magenta]", justify="center")
console.print()
pause(1)

fields = [
    ("Artist", "Shepard Fairey"),
    ("Title", "Hope (2008)"),
    ("Medium", "Screen Print"),
    ("Size", '24" x 36"'),
    ("Edition", "450/500"),
    ("Condition", "Excellent"),
    ("Price", "$1,200.00"),
]

table = Table(box=box.ROUNDED, width=50)
table.add_column("Field", style="cyan")
table.add_column("AI Detected", style="gold1")

for field, value in fields:
    table.add_row(field, value)
    console.clear()
    console.print("\n\n")
    console.print("[bold magenta]              🤖 AI ANALYZING IMAGE...[/bold magenta]", justify="center")
    console.print()
    console.print(table, justify="center")
    pause(0.4)

pause(2)

# SCENE 6: Result
clear()
console.print("\n" * 2)
console.print(Panel("""
[bold green]
           ██╗     ██╗██╗   ██╗███████╗██╗
           ██║     ██║██║   ██║██╔════╝██║
           ██║     ██║██║   ██║█████╗  ██║
           ██║     ██║╚██╗ ██╔╝██╔══╝  ╚═╝
           ███████╗██║ ╚████╔╝ ███████╗██╗
           ╚══════╝╚═╝  ╚═══╝  ╚══════╝╚═╝
[/bold green]

[bold]Listing #123456789012 is now LIVE on eBay![/bold]

   Total time: [green]28 seconds[/green]

   ebay.com/itm/123456789012
""", title="📤 UPLOADED!", border_style="green", width=60), justify="center")
pause(3)

# SCENE 7: Stats
clear()
console.print("\n" * 2)
console.print("[bold yellow]              📊 BATCH RESULTS TODAY[/bold yellow]", justify="center")
console.print()

stats = Table(box=box.ROUNDED, width=50)
stats.add_column("Metric", style="cyan")
stats.add_column("Value", style="green", justify="right")
stats.add_row("Listings Created", "8")
stats.add_row("Total Value", "$12,075")
stats.add_row("Time Saved", "2 hours")
stats.add_row("Accuracy", "100%")
console.print(stats, justify="center")
pause(3)

# SCENE 8: CTA
clear()
console.print("\n" * 4)
console.print("[bold yellow]          ⭐ AUTOMATE YOUR LISTINGS TODAY ⭐[/bold yellow]", justify="center")
console.print()
console.print("[bold white]         github.com/jjshay/ebay-listing-automation[/bold white]", justify="center")
console.print()
console.print("[dim]                     python demo.py[/dim]", justify="center")
pause(3)
