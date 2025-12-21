#!/usr/bin/env python3
"""Update index.html popularity by matching artist names."""

import json
import re

# Popularity data from Spotify web searches
popularity_by_name = {
    "Barbatuques": 2500000,
    "Vitamin String Quartet": 1600000,
    "James Last": 956200,
    "Saez": 680600,
    "Joachim Witt": 599600,
    "Schiller": 420200,
    "Be Svendsen": 422900,
    "Simply Three": 372000,
    "Larkin Poe": 259100,
    "Rokia Traoré": 220000,
    "Hannes Wader": 199500,
    "José Larralde": 160800,
    "Angelo Branduardi": 154900,
    "Seasick Steve": 153100,
    "Hot Butter": 101600,
    "Эдуард Артемьев": 78400,
    "The Tossers": 64000,
    "Civil War": 61500,
    "SuidAkrA": 51300,
    "Suidakra": 51300,
    "Ekseption": 30600,
    "Klayton": 13400,
    "Xploding Plastix": 11900,
    "musica nuda": 7200,

    # Additional estimates
    "Hugo Strasser": 15000,
    "grande1899": 50000,
    "Danish National Symphony Orchestra": 150000,
    "MOZART HEROES": 25000,
    "René Aubry": 80000,
    "Love": 300000,
    "Sly5thAve": 150000,
    "Opal Ocean": 20000,
    "Mathias Duplessy": 25000,
    "Faraualla": 15000,
    "Byron Metcalf": 8000,
    "Neil Zaza": 30000,
    "Żywiołak": 30000,
    "Sabo": 50000,
}

# Read HTML
with open('/Users/lance/Documents/claude-code-course/artifacts/music-sankey/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

updated = 0
for name, pop in popularity_by_name.items():
    # Escape special regex characters in name
    escaped_name = re.escape(name)
    # Pattern: name: 'ArtistName', ... popularity: NUMBER
    pattern = rf"(name: '{escaped_name}'[^}}]*popularity: )(\d+)"
    if re.search(pattern, html):
        html = re.sub(pattern, rf"\g<1>{pop}", html)
        updated += 1
        print(f"Updated {name}: -> {pop}")

# Save
with open('/Users/lance/Documents/claude-code-course/artifacts/music-sankey/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTotal updated: {updated}")
