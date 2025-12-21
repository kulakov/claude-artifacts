#!/usr/bin/env python3
"""Search Spotify for artists without URLs and get their photos."""

import json
import os
import base64
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode, quote

# Load environment variables
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env()

SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

def get_access_token():
    """Get Spotify access token."""
    credentials = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    encoded = base64.b64encode(credentials.encode()).decode()

    req = Request(
        "https://accounts.spotify.com/api/token",
        data=urlencode({"grant_type": "client_credentials"}).encode(),
        headers={
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    with urlopen(req) as response:
        return json.loads(response.read().decode())["access_token"]

def search_artist(name, token):
    """Search for artist by name."""
    url = f"https://api.spotify.com/v1/search?q={quote(name)}&type=artist&limit=5"
    req = Request(url, headers={"Authorization": f"Bearer {token}"})

    try:
        with urlopen(req) as response:
            data = json.loads(response.read().decode())
            artists = data.get('artists', {}).get('items', [])

            # Try to find exact match first
            for artist in artists:
                if artist['name'].lower() == name.lower():
                    return artist

            # Return first result if no exact match
            return artists[0] if artists else None
    except HTTPError as e:
        print(f"  Error searching {name}: {e.code}")
        return None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Load existing photos
    photos_file = os.path.join(script_dir, 'artist_photos.json')
    with open(photos_file, 'r') as f:
        existing_photos = json.load(f)
    existing_names = {p['name'] for p in existing_photos}

    # Load scrobbles to get all artists
    with open(os.path.join(script_dir, 'scrobbles.json'), 'r') as f:
        scrobbles = json.load(f)
    all_artists = set(t['artist'] for t in scrobbles)

    # Find missing
    missing = all_artists - existing_names
    print(f"Searching Spotify for {len(missing)} missing artists...")

    token = get_access_token()

    new_photos = []
    found = 0

    for i, name in enumerate(sorted(missing)):
        result = search_artist(name, token)

        if result and result.get('images'):
            photo_url = result['images'][0]['url']
            new_photos.append({
                "artistId": f"search_{i}",
                "name": name,
                "photoUrl": photo_url,
                "spotifyId": result['id'],
                "followers": result.get('followers', {}).get('total'),
                "genres": result.get('genres', []),
                "searchMatch": result['name']  # Actual Spotify name
            })
            found += 1
            match_note = f" (matched: {result['name']})" if result['name'] != name else ""
            print(f"  [{i+1}/{len(missing)}] {name}: OK{match_note}")
        else:
            new_photos.append({
                "artistId": f"search_{i}",
                "name": name,
                "photoUrl": None,
                "spotifyId": None
            })
            print(f"  [{i+1}/{len(missing)}] {name}: Not found")

        time.sleep(0.1)

    # Save new photos
    output_file = os.path.join(script_dir, 'artist_photos_search.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(new_photos, f, ensure_ascii=False, indent=2)

    print(f"\nFound {found}/{len(missing)} artists")
    print(f"Saved to: {output_file}")

    # Merge with existing
    all_photos = existing_photos + [p for p in new_photos if p.get('photoUrl')]
    merged_file = os.path.join(script_dir, 'artist_photos_all.json')
    with open(merged_file, 'w', encoding='utf-8') as f:
        json.dump(all_photos, f, ensure_ascii=False, indent=2)

    with_photos = sum(1 for p in all_photos if p.get('photoUrl'))
    print(f"Total: {with_photos} artists with photos")
    print(f"Merged file: {merged_file}")

if __name__ == '__main__':
    main()
