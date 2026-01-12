#!/usr/bin/env python3
"""
Generate animated demo GIF for eBay Listing Automation

This script creates an animated GIF showing the listing generation process.
Requires: Pillow

Usage: python generate_demo_gif.py
Output: demo.gif
"""

import os
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Installing Pillow...")
    os.system("pip install Pillow")
    from PIL import Image, ImageDraw, ImageFont


def create_frame(size, step, total_steps):
    """Create a single animation frame"""
    img = Image.new('RGB', size, '#1a1a2e')
    draw = ImageDraw.Draw(img)

    # Colors
    gold = '#ffd700'
    white = '#ffffff'
    green = '#00ff88'
    ebay_blue = '#0064d2'

    # Title
    draw.text((size[0]//2 - 200, 30), "eBay Listing Automation", fill=gold)
    draw.text((size[0]//2 - 180, 60), "AI-Powered Product Listings", fill=white)

    # Animation steps
    steps_text = [
        "Loading inventory data...",
        "Analyzing product images (GPT-4V)...",
        "Analyzing product images (Claude)...",
        "Generating SEO title...",
        "Creating product description...",
        "Setting pricing strategy...",
        "Mapping eBay category...",
        "Preparing listing data...",
        "Listing ready for upload!"
    ]

    # Progress bar
    progress = (step + 1) / total_steps
    bar_width = 400
    bar_x = (size[0] - bar_width) // 2
    bar_y = size[1] - 80

    draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + 20],
                   outline=white, width=2)

    fill_width = int(bar_width * progress)
    if fill_width > 0:
        draw.rectangle([bar_x + 2, bar_y + 2, bar_x + fill_width - 2, bar_y + 18],
                       fill=ebay_blue)

    current_text = steps_text[min(step, len(steps_text) - 1)]
    draw.text((size[0]//2 - 130, bar_y - 40), current_text, fill=white)

    y_pos = 120
    for i, text in enumerate(steps_text):
        if i < step:
            color = green
            prefix = "✓ "
        elif i == step:
            color = gold
            prefix = "→ "
        else:
            color = '#666666'
            prefix = "  "
        draw.text((80, y_pos + i * 25), prefix + text, fill=color)

    return img


def generate_demo_gif():
    """Generate the demo GIF"""
    size = (600, 450)
    total_steps = 9
    frames = []

    for step in range(total_steps):
        frame = create_frame(size, step, total_steps)
        for _ in range(3):
            frames.append(frame)

    for _ in range(5):
        frames.append(frames[-1])

    output_path = Path(__file__).parent / "demo.gif"
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=200,
        loop=0
    )

    print(f"✓ Demo GIF created: {output_path}")


if __name__ == "__main__":
    generate_demo_gif()
