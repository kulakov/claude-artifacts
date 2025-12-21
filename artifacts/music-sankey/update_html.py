#!/usr/bin/env python3
"""Update index.html with new popularity data from full_artists.json."""

import json
import re

# Load artists data
with open('/Users/lance/Documents/claude-code-course/artifacts/music-sankey/full_artists.json', 'r', encoding='utf-8') as f:
    artists = json.load(f)

# Create mapping of artist id to popularity
pop_map = {a['id']: a['popularity'] for a in artists}

# Read HTML file
with open('/Users/lance/Documents/claude-code-course/artifacts/music-sankey/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update popularity values in the artists array
# Pattern: { id: 'a123', ... popularity: NUMBER, ...}
def replace_pop(match):
    artist_id = match.group(1)
    old_pop = match.group(2)
    if artist_id in pop_map:
        new_pop = pop_map[artist_id]
        return match.group(0).replace(f'popularity: {old_pop}', f'popularity: {new_pop}')
    return match.group(0)

# Match artist entries with id and popularity
pattern = r"\{ id: '(a\d+)', [^}]*popularity: (\d+)"
html = re.sub(pattern, replace_pop, html)

# Also update singleTracks popularity
# Pattern in singleTracks: { id: NUMBER, ... popularity: NUMBER }
for artist in artists:
    if artist['trackCount'] == 1:
        for track in artist['tracks']:
            old_pattern = f"{{ id: {track['id']}, [^}}]*popularity: 2000"
            if re.search(old_pattern.replace('[^}}]*', '[^}]*'), html):
                html = re.sub(
                    f"({{ id: {track['id']}, [^}}]*popularity: )2000",
                    f"\\g<1>{artist['popularity']}",
                    html
                )

# Save updated HTML
with open('/Users/lance/Documents/claude-code-course/artifacts/music-sankey/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with new popularity values")
