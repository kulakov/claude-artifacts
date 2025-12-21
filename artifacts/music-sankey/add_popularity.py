#!/usr/bin/env python3
"""Replace geo with popularity for all artists."""

import re

# Popularity estimates for the 28 artists (Spotify monthly listeners)
popularity_map = {
    'a1': 1300000,   # КИНО
    'a2': 800000,    # Высоцкий
    'a3': 651000,    # Noize MC
    'a4': 500000,    # БГ
    'a5': 50000,     # Василий К.
    'a6': 560000,    # Heilung
    'a7': 5000000,   # Hans Zimmer
    'a8': 1500000,   # Rodrigo y Gabriela
    'a9': 300000,    # Каста
    'a10': 4300000,  # Nick Cave
    'a11': 100000,   # Nine Treasures
    'a12': 1200000,  # Jean-Michel Jarre
    'a13': 150000,   # Пушной
    'a14': 400000,   # Oxxxymiron
    'a15': 200000,   # Corvus Corax
    'a16': 300000,   # Krishna Das
    'a17': 600000,   # Сплин
    'a18': 400000,   # Дельфин
    'a19': 200000,   # Порнофильмы
    'a20': 30000,    # Леона
    'a21': 250000,   # Anacondaz
    'a22': 500000,   # Nautilus Pompilius
    'a23': 150000,   # Гражданская оборона
    'a24': 400000,   # Алиса
    'a25': 100000,   # Влади
    'a26': 20000,    # Драконь
    'a27': 50000,    # Atlantida Project
    'a28': 80000,    # Ольга Арефьева
}

# Read file
with open('/Users/lance/Documents/claude-code-course/artifacts/music-sankey/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace geo with popularity for each artist
for artist_id, pop in popularity_map.items():
    # Pattern: id: 'aX', ... geo: 'something',
    pattern = rf"(id: '{artist_id}'[^}}]*?)geo: '[^']+'"
    replacement = rf"\1popularity: {pop}"
    content = re.sub(pattern, replacement, content)

# Save
with open('/Users/lance/Documents/claude-code-course/artifacts/music-sankey/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Replaced geo with popularity for all artists")
