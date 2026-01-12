#!/usr/bin/env python3
"""eBay Listing Automation - Marketing Demo"""
import time
import sys

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.align import Align
    from rich import box
except ImportError:
    print("Run: pip install rich")
    sys.exit(1)

console = Console()

def pause(s=1.5):
    time.sleep(s)

def step(text):
    console.print(f"\n[bold white on #1a1a2e]  {text}  [/]\n")
    pause(0.8)

# INTRO
console.clear()
console.print()
intro = Panel(
    Align.center("[bold yellow]eBAY LISTING AUTOMATION[/]\n\n[white]Photo to Complete Listing in 60 Seconds[/]"),
    border_style="cyan",
    width=60,
    padding=(1, 2)
)
console.print(intro)
pause(2)

# STEP 1
step("STEP 1: DROP PRODUCT PHOTO")

console.print("[dim]$[/] python ebay_lister.py [cyan]./photos/watch.jpg[/]\n")
pause(1)

console.print("  Loading image............", end="")
pause(0.5)
console.print(" [green]4032x3024 JPEG[/]")

console.print("  Detecting product........", end="")
pause(0.6)
console.print(" [green]Watch detected[/]")

console.print("  Analyzing quality........", end="")
pause(0.4)
console.print(" [green]Excellent[/]")

pause(0.8)

photo = Panel(
    "[bold]vintage_watch.jpg[/]\n\n"
    "[dim]Resolution:[/]  4032 x 3024\n"
    "[dim]Quality:[/]     [green]Excellent[/] (sharp, well-lit)\n"
    "[dim]Background:[/]  [green]Clean[/]",
    title="[cyan]Image Loaded[/]",
    border_style="cyan",
    width=50
)
console.print(photo)
pause(1.5)

# STEP 2
step("STEP 2: AI VISION ANALYSIS")

console.print("  [bold]GPT-4 Vision identifying product...[/]\n")
pause(0.8)

detections = [
    ("Brand", "Omega Seamaster"),
    ("Model", "Planet Ocean 600M"),
    ("Reference", "232.30.42.21.01.001"),
    ("Condition", "Excellent (9/10)"),
    ("Case Size", "42mm"),
]

for label, value in detections:
    console.print(f"  {label}:", end="")
    pause(0.3)
    console.print(f" [green]{value}[/]")

pause(1)

# STEP 3
step("STEP 3: MARKET RESEARCH")

console.print("  Searching eBay sold listings...", end="")
pause(0.8)
console.print(" [green]47 comparables found[/]\n")

market = Table(box=box.ROUNDED, width=55)
market.add_column("Date", style="dim")
market.add_column("Condition")
market.add_column("Price", justify="right", style="green")

market.add_row("Jan 10", "Excellent", "$4,850")
market.add_row("Jan 8", "Very Good", "$4,600")
market.add_row("Jan 5", "Excellent", "$4,925")
market.add_row("Jan 3", "Good", "$4,200")

console.print(market)
pause(1)

price = Panel(
    "[bold]Price Analysis[/]\n\n"
    "  Average Sale:     [bold green]$4,665[/]\n"
    "  Recommended:      [bold cyan]$4,899[/]\n"
    "  Min Best Offer:   [bold yellow]$4,400[/]",
    border_style="green",
    width=45
)
console.print(price)
pause(1.5)

# STEP 4
step("STEP 4: GENERATE LISTING")

console.print("  Creating SEO title.......", end="")
pause(0.5)
console.print(" [green]78/80 chars[/]")

console.print("  Writing description......", end="")
pause(0.5)
console.print(" [green]Done[/]")

console.print("  Auto-filling specifics...", end="")
pause(0.5)
console.print(" [green]12 fields[/]")

pause(0.8)

title = Panel(
    "[bold]Omega Seamaster Planet Ocean 600M 42mm Black Dial Steel 232.30.42.21.01.001[/]\n\n"
    "[dim]Characters:[/] 78/80 [green]OK[/]\n"
    "[dim]SEO Score:[/]  [green]94/100[/]",
    title="[green]Generated Title[/]",
    border_style="green",
    width=55
)
console.print(title)
pause(1.5)

# STEP 5
step("STEP 5: ITEM SPECIFICS")

specs = Table(box=box.SIMPLE, width=50)
specs.add_column("Field", style="dim")
specs.add_column("Value", style="white")

specs.add_row("Brand", "Omega")
specs.add_row("Model", "Seamaster Planet Ocean")
specs.add_row("Case Size", "42mm")
specs.add_row("Movement", "Automatic")
specs.add_row("Case Material", "Stainless Steel")
specs.add_row("Water Resistance", "600m")

console.print(specs)
console.print("\n  [green]>[/] All 12 specifics auto-filled")
pause(1.5)

# STEP 6
step("STEP 6: READY TO LIST")

final = Panel(
    Align.center(
        "[bold green]LISTING COMPLETE[/]\n\n"
        "[bold]Price:[/] $4,899 (Best Offer enabled)\n"
        "[bold]Shipping:[/] Free Priority + Insurance\n"
        "[bold]Photos:[/] 8 images optimized\n\n"
        "[dim]Schedule: Sunday 7PM (peak traffic)[/]"
    ),
    title="[bold yellow]READY[/]",
    border_style="green",
    width=50
)
console.print(final)
pause(2)

# FOOTER
console.print()
footer = Panel(
    Align.center(
        "[dim]GPT-4 Vision + eBay API[/]\n"
        "[bold cyan]github.com/jjshay/ebay-listing-automation[/]"
    ),
    title="[dim]eBay Listing Automation v1.5[/]",
    border_style="dim",
    width=50
)
console.print(footer)
pause(3)
