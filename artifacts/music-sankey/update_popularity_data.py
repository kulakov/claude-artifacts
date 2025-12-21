#!/usr/bin/env python3
"""Update artist popularity in index.html"""

import re

# New popularity data
popularity_updates = {
    'Barbatuques': 176266,
    'Civil War': 20000,
    'Drum Ecstasy': 287,
    'Jelonek': 30364,
    'Karolina Cicha': 10000,
    'Larkin Poe': 260000,
    'Suidakra': 46900,
    'Sly5thAve': 36273,
    'The New Synthesizer Experience': 500,
    'Удмуртская тоска': 677,
}

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

updated = 0
for name, pop in popularity_updates.items():
    # Pattern to find artist and update popularity
    pattern = rf"(name: '{re.escape(name)}'[^}}]*?)popularity: \d+"
    replacement = rf"\1popularity: {pop}"
    new_html, count = re.subn(pattern, replacement, html)
    if count > 0:
        html = new_html
        updated += 1
        print(f"  {name}: {pop}")
    else:
        print(f"  {name}: NOT FOUND")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nUpdated {updated} artists")
