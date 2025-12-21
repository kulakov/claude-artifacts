#!/usr/bin/env python3
"""Parse playlist-database.md and extract all artists with their tracks."""

import re
import json
from collections import defaultdict

# Read the playlist file
with open('/Users/lance/lance-claude/07-ЛИЧНОЕ/Я/Психология/playlist-database.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Parse the markdown table
lines = content.strip().split('\n')
tracks = []

for line in lines:
    # Match table rows: | ID | Song Title | Artist | Additional Info | Features |
    match = re.match(r'\|\s*(\d+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]*)\s*\|\s*([^|]*)\s*\|', line)
    if match:
        track_id = int(match.group(1))
        title = match.group(2).strip()
        artist_raw = match.group(3).strip()
        info = match.group(4).strip()
        features = match.group(5).strip()

        # Parse multiple artists (split by comma, but be careful with band names)
        # Main artist is the first one
        artists = [a.strip() for a in artist_raw.split(',')]
        main_artist = artists[0]

        # Clean up artist name variations
        # Remove suffixes like "(Kasta)", "& Интеллигенты", etc.
        clean_artist = re.sub(r'\s*\([^)]+\)\s*$', '', main_artist)
        clean_artist = re.sub(r'\s*&\s*.*$', '', clean_artist)
        clean_artist = clean_artist.strip()

        tracks.append({
            'id': track_id,
            'title': title,
            'artist_raw': artist_raw,
            'artist': clean_artist,
            'info': info,
            'features': features
        })

# Group tracks by artist
artists_tracks = defaultdict(list)
for track in tracks:
    artists_tracks[track['artist']].append(track['title'])

# Sort by number of tracks
sorted_artists = sorted(artists_tracks.items(), key=lambda x: -len(x[1]))

print(f"Total tracks: {len(tracks)}")
print(f"Unique artists: {len(sorted_artists)}")
print("\nArtists with 2+ tracks:")
for artist, track_list in sorted_artists:
    if len(track_list) >= 2:
        print(f"  {artist}: {len(track_list)} tracks")

# Output JSON for easy use
output = []
for artist, track_list in sorted_artists:
    output.append({
        'name': artist,
        'tracks': track_list,
        'count': len(track_list)
    })

with open('/Users/lance/Documents/claude-code-course/artifacts/music-sankey/artists_data.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("\nSaved to artists_data.json")
