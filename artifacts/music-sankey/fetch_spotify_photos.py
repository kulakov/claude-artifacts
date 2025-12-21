#!/usr/bin/env python3
"""Fetch artist photos from Spotify API."""

import json
import os
import base64
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

# Load environment variables from .env
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
    """Get Spotify access token using client credentials flow."""
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        print("ERROR: Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET in .env")
        print("\nAdd these lines to /Users/lance/Documents/claude-code-course/.env:")
        print("SPOTIFY_CLIENT_ID=your_client_id")
        print("SPOTIFY_CLIENT_SECRET=your_client_secret")
        print("\nGet credentials at: https://developer.spotify.com/dashboard")
        return None

    # Encode credentials
    credentials = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    # Request token
    url = "https://accounts.spotify.com/api/token"
    data = urlencode({"grant_type": "client_credentials"}).encode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    req = Request(url, data=data, headers=headers)
    try:
        with urlopen(req) as response:
            result = json.loads(response.read().decode())
            return result.get("access_token")
    except HTTPError as e:
        print(f"Error getting token: {e.code} {e.reason}")
        return None

def get_artist_info(artist_id, access_token):
    """Get artist info including images from Spotify API."""
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    req = Request(url, headers=headers)
    try:
        with urlopen(req) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        print(f"Error fetching artist {artist_id}: {e.code}")
        return None

def extract_spotify_id(url):
    """Extract Spotify artist ID from URL."""
    # URL format: https://open.spotify.com/artist/XXXXX
    if '/artist/' in url:
        return url.split('/artist/')[-1].split('?')[0]
    return None

def main():
    # Load artist data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'artist_spotify_urls.json')
    output_file = os.path.join(script_dir, 'artist_photos.json')

    with open(input_file, 'r', encoding='utf-8') as f:
        artists = json.load(f)

    print(f"Loaded {len(artists)} artists")

    # Get access token
    token = get_access_token()
    if not token:
        return

    print("Got access token, fetching artist data...")

    results = []
    for i, artist in enumerate(artists):
        spotify_url = artist.get('spotifyUrl', '')
        spotify_id = extract_spotify_id(spotify_url)

        if not spotify_id:
            print(f"  Skipping {artist['name']} - no valid Spotify URL")
            results.append({
                "artistId": artist['artistId'],
                "name": artist['name'],
                "photoUrl": None,
                "spotifyId": None
            })
            continue

        # Fetch artist info
        info = get_artist_info(spotify_id, token)

        if info and info.get('images'):
            # Get largest image (first in array)
            images = info['images']
            photo_url = images[0]['url'] if images else None

            results.append({
                "artistId": artist['artistId'],
                "name": artist['name'],
                "photoUrl": photo_url,
                "spotifyId": spotify_id,
                "followers": info.get('followers', {}).get('total'),
                "genres": info.get('genres', [])
            })
            print(f"  [{i+1}/{len(artists)}] {artist['name']}: OK")
        else:
            results.append({
                "artistId": artist['artistId'],
                "name": artist['name'],
                "photoUrl": None,
                "spotifyId": spotify_id
            })
            print(f"  [{i+1}/{len(artists)}] {artist['name']}: No image")

        # Rate limiting
        time.sleep(0.1)

    # Save results
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Count results
    with_photos = sum(1 for r in results if r.get('photoUrl'))
    print(f"\nDone! {with_photos}/{len(results)} artists with photos")
    print(f"Saved to: {output_file}")

if __name__ == '__main__':
    main()
