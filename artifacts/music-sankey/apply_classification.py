#!/usr/bin/env python3
"""Apply classification to index.html"""

import json
import re

# Load classification
with open('classification_draft.json', 'r') as f:
    classification = json.load(f)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Build new genreToArtist entries
genre_entries = []
for artist in classification:
    aid = artist['id']
    for genre in artist['genres']:
        genre_entries.append(f"{{ source: '{genre}', target: '{aid}' }}")

# Build new artistToTrait entries
trait_entries = []
for artist in classification:
    aid = artist['id']
    for trait in artist['traits']:
        trait_entries.append(f"{{ source: '{aid}', target: '{trait}' }}")

# Find existing genreToArtist and append
genre_match = re.search(r'const genreToArtist = \[([\s\S]*?)\];', html)
if genre_match:
    existing = genre_match.group(1).strip().rstrip(',')
    new_genres = existing + ',\n            ' + ',\n            '.join(genre_entries)
    html = html[:genre_match.start()] + f'const genreToArtist = [{new_genres}\n        ];' + html[genre_match.end():]
    print(f"Added {len(genre_entries)} genre connections")

# Find existing artistToTrait and append
trait_match = re.search(r'const artistToTrait = \[([\s\S]*?)\];', html)
if trait_match:
    existing = trait_match.group(1).strip().rstrip(',')
    new_traits = existing + ',\n            ' + ',\n            '.join(trait_entries)
    html = html[:trait_match.start()] + f'const artistToTrait = [{new_traits}\n        ];' + html[trait_match.end():]
    print(f"Added {len(trait_entries)} trait connections")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done!")
