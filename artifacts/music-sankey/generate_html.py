#!/usr/bin/env python3
"""Generate the full visualization HTML with all 314 tracks."""

import json
import re

# Load artists data
with open('/Users/lance/Documents/claude-code-course/artifacts/music-sankey/full_artists.json', 'r', encoding='utf-8') as f:
    artists = json.load(f)

# Generate JavaScript array
js_artists = []
for a in artists:
    # Only include artists with 2+ tracks as cards
    if a['trackCount'] >= 2:
        tracks_js = []
        for t in a['tracks']:
            title = t['title'].replace("'", "\\'").replace('"', '\\"')
            search = f"{a['name']} {t['title']}".replace("'", "\\'").replace('"', '\\"')
            tracks_js.append(f"{{ id: {t['id']}, title: '{title}', search: '{search}' }}")

        name = a['name'].replace("'", "\\'")
        js_artists.append(f"""            {{ id: '{a['id']}', name: '{name}', popularity: {a['popularity']}, tracks: [{', '.join(tracks_js)}] }}""")

# Generate single tracks for artists with only 1 track (shown as dots only)
single_tracks = []
for a in artists:
    if a['trackCount'] == 1:
        t = a['tracks'][0]
        title = t['title'].replace("'", "\\'").replace('"', '\\"')
        name = a['name'].replace("'", "\\'")
        search = f"{a['name']} {t['title']}".replace("'", "\\'").replace('"', '\\"')
        single_tracks.append(f"""            {{ id: {t['id']}, title: '{title}', artist: '{name}', search: '{search}', popularity: {a['popularity']} }}""")

# Count
card_artists = [a for a in artists if a['trackCount'] >= 2]
dot_only = [a for a in artists if a['trackCount'] == 1]
total_tracks = sum(a['trackCount'] for a in artists)

print(f"Artists with cards: {len(card_artists)}")
print(f"Artists as dots only: {len(dot_only)}")
print(f"Total tracks: {total_tracks}")

# Save the JS code
with open('/Users/lance/Documents/claude-code-course/artifacts/music-sankey/artists_js.txt', 'w', encoding='utf-8') as f:
    f.write("// Artists with 2+ tracks (shown as cards)\n")
    f.write("const artists = [\n")
    f.write(',\n'.join(js_artists))
    f.write("\n        ];\n\n")
    f.write("// Single tracks (shown as dots only, no artist card)\n")
    f.write("const singleTracks = [\n")
    f.write(',\n'.join(single_tracks))
    f.write("\n        ];")

print("\nSaved to artists_js.txt")
