#!/usr/bin/env python3
import urllib.request
import json
import os
import ssl

# Disable SSL verification for old LibreSSL
ssl._create_default_https_context = ssl._create_unverified_context

os.chdir('/Users/lance/Documents/claude-code-course/music-sankey/images')

artists = {
    'kino.jpg': 'Viktor_Tsoi',
    'vysotsky.jpg': 'Vladimir_Vysotsky',
    'noize-mc.jpg': 'Noize_MC',
    'bg.jpg': 'Boris_Grebenshchikov',
    'heilung.jpg': 'Heilung',
    'hans-zimmer.jpg': 'Hans_Zimmer',
    'rodrigo-gabriela.jpg': 'Rodrigo_y_Gabriela',
    'nick-cave.jpg': 'Nick_Cave',
    'nine-treasures.jpg': 'Nine_Treasures',
    'jarre.jpg': 'Jean-Michel_Jarre',
    'pushnoy.jpg': 'Alexander_Pushnoy',
    'oxxxymiron.jpg': 'Oxxxymiron',
    'corvus-corax.jpg': 'Corvus_Corax_(band)',
    'krishna-das.jpg': 'Krishna_Das_(singer)',
}

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}

for filename, wiki_title in artists.items():
    try:
        api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_title}"
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())

        if 'thumbnail' in data and 'source' in data['thumbnail']:
            img_url = data['thumbnail']['source']
            # Try to get larger version
            img_url = img_url.replace('/324px-', '/400px-').replace('/320px-', '/400px-')

            img_req = urllib.request.Request(img_url, headers=headers)
            with urllib.request.urlopen(img_req, timeout=15) as img_resp:
                img_data = img_resp.read()
                with open(filename, 'wb') as f:
                    f.write(img_data)
                print(f"✓ {filename} ({len(img_data)} bytes)")
        else:
            print(f"✗ {filename}: no thumbnail")
    except Exception as e:
        print(f"✗ {filename}: {e}")

print("\nDone!")
