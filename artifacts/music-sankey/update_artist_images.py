#!/usr/bin/env python3
"""Update artist images in index.html with Spotify photos."""

import json
import re
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# Load image mapping
with open(os.path.join(script_dir, 'artist_image_map.json'), 'r') as f:
    image_map = json.load(f)

# Read HTML
with open(os.path.join(script_dir, 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

# Artist name mappings for special cases
name_mappings = {
    'Высоцкий': 'Владимир Высоцкий',
    'БГ': 'Борис Гребенщиков',
    'Пушной': 'Александр Пушной',
    'Ольга Арефьева': 'Ольга Арефьева и Ковчег',
}

updated = 0

# Find all artist entries and update images
def replace_image(match):
    global updated
    full_match = match.group(0)
    name_match = re.search(r"name: '([^']+)'", full_match)
    if not name_match:
        return full_match

    name = name_match.group(1)

    # Try direct match first
    if name in image_map:
        new_image = image_map[name]
    # Try mapped name
    elif name in name_mappings and name_mappings[name] in image_map:
        new_image = image_map[name_mappings[name]]
    else:
        print(f"  No match: {name}")
        return full_match

    # Replace image property
    old_image = re.search(r"image: '[^']+'", full_match)
    if old_image:
        new_match = full_match.replace(old_image.group(0), f"image: '{new_image}'")
        updated += 1
        print(f"  Updated: {name} -> {new_image}")
        return new_match

    return full_match

# Pattern to match artist object definitions
pattern = r"\{ id: 'a\d+'[^}]+\}"
html = re.sub(pattern, replace_image, html)

# Save
with open(os.path.join(script_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nUpdated {updated} artist images")
