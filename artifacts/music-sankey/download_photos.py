#!/usr/bin/env python3
"""Download artist photos from Spotify URLs to local images folder."""

import json
import os
import re
import time
from urllib.request import urlopen, Request
from urllib.error import HTTPError

def sanitize_filename(name):
    """Convert artist name to safe filename."""
    # Replace spaces and special chars
    name = name.lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s]+', '-', name)
    return name[:50]  # Limit length

def download_image(url, filepath):
    """Download image from URL."""
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=30) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"    Error: {e}")
        return False

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, 'images')

    # Create images dir if needed
    os.makedirs(images_dir, exist_ok=True)

    # Load all photos
    with open(os.path.join(script_dir, 'artist_photos_all.json'), 'r') as f:
        photos = json.load(f)

    print(f"Processing {len(photos)} artists...")

    downloaded = 0
    skipped = 0
    failed = 0

    # Track filename mapping
    mapping = {}

    for i, artist in enumerate(photos):
        name = artist['name']
        url = artist.get('photoUrl')

        if not url:
            skipped += 1
            continue

        # Generate filename
        filename = f"spotify-{sanitize_filename(name)}.jpg"
        filepath = os.path.join(images_dir, filename)

        # Skip if exists
        if os.path.exists(filepath):
            mapping[name] = filename
            print(f"  [{i+1}/{len(photos)}] {name}: exists")
            continue

        print(f"  [{i+1}/{len(photos)}] {name}: downloading...")

        if download_image(url, filepath):
            downloaded += 1
            mapping[name] = filename
        else:
            failed += 1

        time.sleep(0.1)

    # Save mapping
    mapping_file = os.path.join(script_dir, 'artist_image_map.json')
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print(f"\nDone!")
    print(f"  Downloaded: {downloaded}")
    print(f"  Skipped (no URL): {skipped}")
    print(f"  Failed: {failed}")
    print(f"  Mapping saved to: {mapping_file}")

if __name__ == '__main__':
    main()
