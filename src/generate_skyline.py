#!/usr/bin/env python3
"""
contrib-skyline
Generate beautiful isometric skyline SVGs from GitHub contribution data.
Supports real data (via GraphQL) or high-quality sample data.
"""

import math
import os
import random
import json
import urllib.request
from datetime import datetime, timedelta
from typing import List, Dict, Optional

def generate_sample_data(days: int = 365) -> List[Dict]:
    data = []
    start = datetime.now() - timedelta(days=days)
    for i in range(days):
        date = start + timedelta(days=i)
        weekday = date.weekday()
        base = 6 if weekday < 5 else 2
        if random.random() < 0.08:
            contribs = random.randint(18, 45)
        elif random.random() < 0.15:
            contribs = random.randint(8, 16)
        else:
            contribs = max(0, int(random.gauss(base, 4)))
        data.append({"date": date.strftime("%Y-%m-%d"), "count": contribs})
    return data

def fetch_github_contributions(username: str, token: str, days: int = 365) -> Optional[List[Dict]]:
    """Fetch real contribution data using GitHub GraphQL API."""
    if not token or not username:
        return None

    query = """
    query($username: String!) {
      user(login: $username) {
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """

    payload = json.dumps({
        "query": query,
        "variables": {"username": username}
    }).encode()

    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "contrib-skyline"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
            result = []
            for week in weeks:
                for day in week["contributionDays"]:
                    result.append({
                        "date": day["date"],
                        "count": day["contributionCount"]
                    })
            return result[-days:]
    except Exception as e:
        print(f"Warning: Could not fetch real data ({e}). Falling back to sample.")
        return None

def isometric(x: float, y: float, z: float, scale: float = 18) -> tuple:
    iso_x = (x - y) * scale * math.cos(math.radians(30))
    iso_y = (x + y) * scale * math.sin(math.radians(30)) - z * scale * 0.6
    return iso_x, iso_y

THEMES = {
    "neon": {"bg": "#0a0a0a", "building": "#00ff9d", "window": "#39ff14", "ground": "#111111", "text": "#ffffff", "accent": "#00ff9d"},
    "dark": {"bg": "#0d1117", "building": "#39d353", "window": "#26a641", "ground": "#161b22", "text": "#c9d1d9", "accent": "#58a6ff"},
    "ocean": {"bg": "#0c2340", "building": "#4fc3f7", "window": "#81d4fa", "ground": "#082047", "text": "#e3f2fd", "accent": "#29b6f6"},
    "synthwave": {"bg": "#1a0a2e", "building": "#ff6ec7", "window": "#ff9aeb", "ground": "#2d1b4e", "text": "#ffffff", "accent": "#f72585"},
    "matrix": {"bg": "#000000", "building": "#00ff41", "window": "#00cc33", "ground": "#001100", "text": "#00ff41", "accent": "#00ff41"},
    "sakura": {"bg": "#1a1225", "building": "#ffb7c5", "window": "#ffc1cc", "ground": "#2d1b36", "text": "#fff5f7", "accent": "#ff6b9d"},
}

def generate_svg(data: List[Dict], theme: str = "neon", weeks_to_show: int = 26, username: str = "") -> str:
    t = THEMES.get(theme, THEMES["neon"])
    width, height = 1400, 700

    weeks = []
    current = []
    for day in data[-365:]:
        current.append(day["count"])
        if len(current) == 7:
            weeks.append(sum(current))
            current = []
    if current:
        weeks.append(sum(current))

    weeks = weeks[-weeks_to_show:]
    max_val = max(weeks) if weeks else 1
    total = sum(d["count"] for d in data)
    active_days = sum(1 for d in data if d["count"] > 0)
    max_streak = current_streak = 0
    for d in data:
        if d["count"] > 0:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        f'<rect width="100%" height="100%" fill="{t["bg"]}"/>',
        '<defs><filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="4" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
    ]

    svg.append(f'<polygon points="80,520 1320,520 1200,580 200,580" fill="{t["ground"]}"/>')

    center_x = width // 2
    base_y = 500

    for i, week_sum in enumerate(weeks):
        height_px = 30 + (week_sum / max_val) * 280
        bx, by = isometric(i * 1.8 - weeks_to_show * 0.9, 0, 0)
        bx += center_x
        by += base_y - 180

        svg.append(
            f'<rect x="{bx-18}" y="{by - height_px}" width="36" height="{height_px}" '
            f'fill="{t["building"]}" opacity="0.9" filter="url(#glow)"/>'
        )
        window_rows = max(1, int(height_px / 18))
        for r in range(window_rows):
            for c in range(2):
                wx = bx - 12 + c * 16
                wy = by - height_px + r * 18 + 6
                svg.append(f'<rect x="{wx}" y="{wy}" width="7" height="7" fill="{t["window"]}" opacity="0.95"/>')

    title = f"@{username}" if username else "contrib-skyline"
    svg.append(f'<text x="60" y="50" fill="{t["text"]}" font-family="ui-monospace, monospace" font-size="28" font-weight="700">{title}</text>')
    svg.append(f'<text x="60" y="82" fill="{t["accent"]}" font-family="monospace" font-size="15">{theme.upper()} THEME</text>')

    stats_y = height - 50
    svg.append(f'<text x="60" y="{stats_y}" fill="{t["text"]}" font-family="monospace" font-size="13">Total: {total:,}  •  Active days: {active_days}  •  Longest streak: {max_streak} days</text>')
    svg.append('</svg>')
    return "\n".join(svg)

def main():
    username = os.environ.get("GITHUB_USERNAME", "ilyasaalmadani")
    token = os.environ.get("GITHUB_TOKEN")

    data = fetch_github_contributions(username, token) or generate_sample_data()
    source = "real" if token else "sample"
    print(f"Using {source} data for @{username}")

    themes = ["neon", "dark", "ocean", "synthwave", "matrix", "sakura"]
    os.makedirs("examples", exist_ok=True)
    for theme in themes:
        svg = generate_svg(data, theme, username=username)
        path = f"examples/skyline-{theme}.svg"
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"Generated {path}")

if __name__ == "__main__":
    main()
