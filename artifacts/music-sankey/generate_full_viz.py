#!/usr/bin/env python3
"""Generate full visualization with all tracks."""

import json
import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))

# Load data
with open(os.path.join(script_dir, 'track_years.json'), 'r') as f:
    tracks_data = json.load(f)

with open(os.path.join(script_dir, 'scrobbles.json'), 'r') as f:
    scrobbles_data = json.load(f)

with open(os.path.join(script_dir, 'artist_image_map.json'), 'r') as f:
    image_map = json.load(f)

with open(os.path.join(script_dir, 'artist_photos_all.json'), 'r') as f:
    photos_data = json.load(f)

# Create scrobbles lookup
scrobbles_lookup = {}
for s in scrobbles_data:
    key = f"{s['artist']}|{s['title']}"
    scrobbles_lookup[key] = s['scrobbles']

# Create artist followers lookup
followers_lookup = {}
for p in photos_data:
    if p.get('followers'):
        followers_lookup[p['name']] = p['followers']

# Group tracks by artist
artists_tracks = {}
for t in tracks_data:
    artist = t['artist']
    if artist not in artists_tracks:
        artists_tracks[artist] = []

    key = f"{t['artist']}|{t['title']}"
    scrobbles = scrobbles_lookup.get(key, 100)  # Default scrobbles

    artists_tracks[artist].append({
        'title': t['title'],
        'year': t['year'],
        'scrobbles': scrobbles
    })

print(f"Total artists: {len(artists_tracks)}")
print(f"Total tracks: {len(tracks_data)}")

# Calculate median year and total scrobbles for each artist
artists_list = []
for name, tracks in artists_tracks.items():
    # Filter tracks with valid years
    valid_tracks = [t for t in tracks if t['year']]
    if not valid_tracks:
        continue

    years = sorted([t['year'] for t in valid_tracks])
    median_year = years[len(years) // 2]

    # Get popularity (followers or sum of scrobbles)
    popularity = followers_lookup.get(name, sum(t['scrobbles'] for t in tracks))

    # Get image
    image = image_map.get(name, None)

    artists_list.append({
        'name': name,
        'tracks': valid_tracks,
        'medianYear': median_year,
        'popularity': max(1000, popularity),  # Min 1000 for log scale
        'image': image
    })

# Sort by popularity
artists_list.sort(key=lambda a: -a['popularity'])

print(f"Artists with valid tracks: {len(artists_list)}")

# Generate color palette
def generate_color(index, total):
    hue = (index * 360 / total) % 360
    return f"hsl({hue}, 70%, 50%)"

# Build JavaScript arrays
artists_js = []
for i, a in enumerate(artists_list):
    color = generate_color(i, len(artists_list))
    tracks_str = ", ".join([
        f"{{ title: '{t['title'].replace(chr(39), chr(92)+chr(39))}', year: {t['year'] or 2000} }}"
        for t in a['tracks']
    ])

    image_str = f"image: '{a['image']}'," if a['image'] else ""

    artists_js.append(
        f"{{ id: 'a{i+1}', name: '{a['name'].replace(chr(39), chr(92)+chr(39))}', "
        f"bgColor: '{color}', popularity: {a['popularity']}, {image_str} "
        f"tracks: [{tracks_str}] }}"
    )

# Build scrobbles lookup
scrobbles_js = []
for s in scrobbles_data:
    key = f"{s['artist']}|{s['title']}"
    scrobbles_js.append(f'"{key}": {s["scrobbles"]}')

# Read template
with open(os.path.join(script_dir, 'index.html'), 'r') as f:
    html = f.read()

# Replace artists array
artists_pattern = r"const artists = \[[\s\S]*?\];"
new_artists = "const artists = [\n            " + ",\n            ".join(artists_js) + "\n        ];"

# Find and replace
match = re.search(artists_pattern, html)
if match:
    html = html[:match.start()] + new_artists + html[match.end():]
    print("Replaced artists array")

# Replace scrobbles lookup
scrobbles_pattern = r"const trackScrobbles = \{[\s\S]*?\};"
new_scrobbles = "const trackScrobbles = {\n            " + ",\n            ".join(scrobbles_js) + "\n        };"

match = re.search(scrobbles_pattern, html)
if match:
    html = html[:match.start()] + new_scrobbles + html[match.end():]
    print("Replaced scrobbles lookup")

# Save
output_file = os.path.join(script_dir, 'index-full.html')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nGenerated: {output_file}")
print(f"Artists: {len(artists_list)}, Tracks: {sum(len(a['tracks']) for a in artists_list)}")
