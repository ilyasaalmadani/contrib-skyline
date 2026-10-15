#!/usr/bin/env python3
"""
contrib-skyline: Generate isometric skyline SVGs from contribution data.
A novel, customizable visualization for GitHub profiles.
"""

import math
import random
from datetime import datetime, timedelta

def generate_sample_data(days=365):
    """Generate realistic sample contribution data."""
    data = []
    start = datetime.now() - timedelta(days=days)
    for i in range(days):
        date = start + timedelta(days=i)
        # Simulate activity: higher on weekdays, some peaks
        weekday = date.weekday()
        base = 5 if weekday < 5 else 1
        if random.random() < 0.1:  # peak days
            contribs = random.randint(15, 40)
        else:
            contribs = max(0, int(random.gauss(base, 3)))
        data.append({"date": date.strftime("%Y-%m-%d"), "count": contribs})
    return data

def isometric_point(x, y, z, scale=20):
    """Convert 3D coords to 2D isometric."""
    iso_x = (x - y) * scale * math.cos(math.radians(30))
    iso_y = (x + y) * scale * math.sin(math.radians(30)) - z * scale * 0.5
    return iso_x, iso_y

def generate_svg(data, theme="neon", width=1200, height=600):
    """Generate an isometric skyline SVG."""
    themes = {
        "neon": {
            "bg": "#0a0a0a",
            "building": "#00ff9d",
            "window": "#00cc7a",
            "ground": "#1a1a1a",
            "text": "#ffffff"
        },
        "dark": {
            "bg": "#161b22",
            "building": "#39d353",
            "window": "#26a641",
            "ground": "#0d1117",
            "text": "#c9d1d9"
        },
        "ocean": {
            "bg": "#0c2340",
            "building": "#4fc3f7",
            "window": "#0288d1",
            "ground": "#082047",
            "text": "#e3f2fd"
        }
    }
    t = themes.get(theme, themes["neon"])
    
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        f'<rect width="100%" height="100%" fill="{t["bg"]}"/>',
        '<defs>',
        '<filter id="glow"><feGaussianBlur stdDeviation="3" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
        '</defs>'
    ]
    
    # Ground
    svg_parts.append(f'<polygon points="100,500 1100,500 1000,550 200,550" fill="{t["ground"]}"/>')
    
    # Buildings - group by weeks
    weeks = []
    current_week = []
    for i, day in enumerate(data[-52*7:]):  # last year
        current_week.append(day["count"])
        if len(current_week) == 7:
            weeks.append(sum(current_week))
            current_week = []
    
    max_height = max(weeks) if weeks else 1
    center_x = width // 2
    base_y = 480
    
    for i, week_total in enumerate(weeks[-20:]):  # last 20 weeks for visual
        height_scale = (week_total / max_height) * 200 + 20
        x_offset = (i - 10) * 40
        bx, by = isometric_point(i * 2, 0, 0)
        bx += center_x - 200
        by += base_y - 100
        
        # Building body
        svg_parts.append(
            f'<rect x="{bx-15}" y="{by - height_scale}" width="30" height="{height_scale}" '
            f'fill="{t["building"]}" opacity="0.85" filter="url(#glow)"/>'
        )
        # Windows
        for w in range(int(height_scale / 15)):
            wx = bx - 10 + (w % 2) * 12
            wy = by - height_scale + w * 15 + 5
            svg_parts.append(
                f'<rect x="{wx}" y="{wy}" width="8" height="8" fill="{t["window"]}" opacity="0.9"/>'
            )
    
    # Title
    svg_parts.append(
        f'<text x="50" y="50" fill="{t["text"]}" font-family="monospace" font-size="24" font-weight="bold">contrib-skyline</text>'
    )
    svg_parts.append(
        f'<text x="50" y="80" fill="{t["text"]}" font-family="monospace" font-size="14">Isometric GitHub Contribution Skyline</text>'
    )
    
    # Stats
    total = sum(d["count"] for d in data)
    svg_parts.append(
        f'<text x="50" y="{height-40}" fill="{t["text"]}" font-family="monospace" font-size="12">Sample: {total} contributions visualized</text>'
    )
    
    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)

if __name__ == "__main__":
    data = generate_sample_data()
    for theme in ["neon", "dark", "ocean"]:
        svg = generate_svg(data, theme)
        with open(f"examples/skyline-{theme}.svg", "w") as f:
            f.write(svg)
        print(f"Generated examples/skyline-{theme}.svg")
