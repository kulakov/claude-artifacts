#!/usr/bin/env python3
"""Generate full artists data with popularity estimates."""

import re
import json
from collections import defaultdict

# Known popularity from Spotify (monthly listeners)
KNOWN_POPULARITY = {
    'Hans Zimmer': 14400000,
    'Nick Cave': 4300000,
    'КИНО': 1300000,
    'Jean-Michel Jarre': 733000,
    'Noize MC': 651000,
    'Krishna Das': 591000,
    'Heilung': 560000,
    'Oxxxymiron': 407000,
    'Rodrigo y Gabriela': 398000,
    'Сплин': 385000,
    'Nautilus Pompilius': 334000,
    'Каста': 246000,
    'Порнофильмы': 217000,
    'Corvus Corax': 214000,
    'Anacondaz': 168000,
    'Дельфин': 120000,
    'Atlantida Project': 95000,
    'Алиса': 93000,
    'Высоцкий': 86000,
    'Владимир Высоцкий': 86000,
    'Гражданская оборона': 82000,
    'БГ': 69000,
    'Борис Гребенщиков': 69000,
    'Аквариум': 69000,
    'Влади': 30000,
    'Пушной': 20000,
    'Александр Пушной': 20000,
    'Nine Treasures': 19000,
    'Ольга Арефьева': 5000,
    'Ольга Арефьева и Ковчег': 5000,
    'Леона': 5000,
    'Василий К.': 4000,
    'Драконь': 2000,
    # International known artists
    'Phil Collins': 25000000,
    'David Bowie': 22000000,
    'Fleetwood Mac': 21000000,
    'Bob Dylan': 14000000,
    'Leonard Cohen': 8000000,
    'Moby': 5000000,
    'Tom Waits': 3500000,
    'King Crimson': 2000000,
    'Rainbow': 1800000,
    'Mike Oldfield': 1500000,
    'Klaus Schulze': 300000,
    'Ramin Djawadi': 4000000,
    'Bo Burnham': 3000000,
    'Sabaton': 3500000,
    'Anoushka Shankar': 500000,
    'Tommy Emmanuel': 400000,
    'Juno Reactor': 350000,
    'Django Django': 800000,
    'Celtic Woman': 700000,
    'Steeleye Span': 200000,
    'Oliver Koletzki': 600000,
    # Russian known artists
    'Би-2': 800000,
    'Мельница': 150000,
    'LOUNA': 180000,
    'Пикник': 250000,
    'АлоэВера': 80000,
    'Монеточка': 1500000,
    'Ляпис Трубецкой': 400000,
    'Найк Борзов': 150000,
    'Аукцыон': 50000,
    'Янка Дягилева': 40000,
    'Ноль': 30000,
    'Ундервуд': 60000,
    'Лигалайз': 200000,
    'Сурганова и Оркестр': 100000,
    'HORUS': 150000,
    'ST1M': 300000,
    'DEEP-EX-SENSE': 100000,
    # World music
    'Eivør': 400000,
    'Nolwenn Leroy': 500000,
    'Heidevolk': 150000,
    'Die Apokalyptischen Reiter': 200000,
    'Cruachan': 50000,
    'Steve \'n\' Seagulls': 800000,
    'Blackmore\'s Night': 300000,
    # Smaller/niche
    'PALC': 10000,
    'GREEN CROW': 15000,
    'Joker James': 8000,
    'Joanna Stingray': 5000,
    'Вера Полозкова': 25000,
    'Немного нервно': 20000,
    'Заточка': 15000,
    'Умка и Броневик': 10000,
    'Эрнесто Заткнитесь': 5000,
    'Тим Скоренко': 3000,
    'Екатерина Яшникова': 8000,
    'Михаил Башаков': 5000,
    'Кирилл Комаров': 3000,
    'Markscheider Kunst': 20000,
    'Brazzaville': 50000,
    'Zodiac': 30000,
    'The Dreadnoughts': 150000,
    'Dobranotch': 10000,
    'Seatbelts': 200000,
    'Yodelice': 100000,
    'Max Cooper': 300000,
    # Estimate for unknowns: 1000-5000
}

# Read and parse playlist
with open('/Users/lance/lance-claude/07-ЛИЧНОЕ/Я/Психология/playlist-database.md', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.strip().split('\n')
all_tracks = []

for line in lines:
    match = re.match(r'\|\s*(\d+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]*)\s*\|\s*([^|]*)\s*\|', line)
    if match:
        track_id = int(match.group(1))
        title = match.group(2).strip()
        artist_raw = match.group(3).strip()

        # Get main artist
        artists = [a.strip() for a in artist_raw.split(',')]
        main_artist = artists[0]
        clean_artist = re.sub(r'\s*\([^)]+\)\s*$', '', main_artist)
        clean_artist = re.sub(r'\s*&\s*.*$', '', clean_artist)
        clean_artist = clean_artist.strip()

        all_tracks.append({
            'id': track_id,
            'title': title,
            'artist': clean_artist,
            'artist_raw': artist_raw
        })

# Group by artist
artists_data = defaultdict(lambda: {'tracks': [], 'popularity': 2000})

for track in all_tracks:
    artist = track['artist']
    artists_data[artist]['tracks'].append({
        'id': track['id'],
        'title': track['title']
    })

    # Set popularity
    for known, pop in KNOWN_POPULARITY.items():
        if known.lower() in artist.lower() or artist.lower() in known.lower():
            artists_data[artist]['popularity'] = pop
            break

# Assign IDs and finalize
final_artists = []
for i, (name, data) in enumerate(sorted(artists_data.items(), key=lambda x: -x[1]['popularity'])):
    final_artists.append({
        'id': f'a{i+1}',
        'name': name,
        'popularity': data['popularity'],
        'tracks': data['tracks'],
        'trackCount': len(data['tracks'])
    })

# Output
print(f"Total artists: {len(final_artists)}")
print(f"Total tracks: {len(all_tracks)}")

# Save
with open('/Users/lance/Documents/claude-code-course/artifacts/music-sankey/full_artists.json', 'w', encoding='utf-8') as f:
    json.dump(final_artists, f, ensure_ascii=False, indent=2)

print("\nTop 20 by popularity:")
for a in final_artists[:20]:
    print(f"  {a['name']}: {a['popularity']:,} ({a['trackCount']} tracks)")

print("\nSaved to full_artists.json")
