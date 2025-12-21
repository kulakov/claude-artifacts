#!/usr/bin/env python3
"""Generate complete HTML visualization with all 206 artists, popularity-based Y-axis."""

import json

# Load artists
with open('/Users/lance/Documents/claude-code-course/artifacts/music-sankey/full_artists.json', 'r', encoding='utf-8') as f:
    artists = json.load(f)

# Generate artists JS for cards (2+ tracks)
card_artists = [a for a in artists if a['trackCount'] >= 2]
single_artists = [a for a in artists if a['trackCount'] == 1]

def escape_js(s):
    return s.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')

artists_js = []
for a in card_artists:
    tracks_js = []
    for t in a['tracks']:
        title = escape_js(t['title'])
        search = escape_js(f"{a['name']} {t['title']}")
        tracks_js.append(f"{{ title: '{title}', search: '{search}' }}")

    name = escape_js(a['name'])
    artists_js.append(f"            {{ id: '{a['id']}', name: '{name}', popularity: {a['popularity']}, tracks: [{', '.join(tracks_js)}] }},")

# Single tracks
singles_js = []
for a in single_artists:
    t = a['tracks'][0]
    title = escape_js(t['title'])
    name = escape_js(a['name'])
    search = escape_js(f"{a['name']} {t['title']}")
    singles_js.append(f"            {{ id: {t['id']}, title: '{title}', artist: '{name}', search: '{search}', popularity: {a['popularity']} }},")

html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Music DNA - 206 Artists</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --text-primary: #e8e8e8;
            --text-dim: #666;
            --card-bg: #1a1a24;
            --card-border: #2a2a3a;
            --accent-blue: #4a9eff;
            --accent-green: #22c55e;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background: var(--bg-primary); color: var(--text-primary); font-family: 'JetBrains Mono', monospace; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 20px; }}
        h1 {{ font-size: 1.2em; margin-bottom: 10px; color: var(--text-dim); }}

        .genres-row, .traits-row {{ display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; margin: 10px 0; max-width: 1400px; position: relative; z-index: 200; padding: 10px 20px; }}
        .genres-row {{ background: linear-gradient(to bottom, var(--bg-primary) 0%, transparent 100%); }}
        .traits-row {{ background: linear-gradient(to top, var(--bg-primary) 0%, transparent 100%); }}

        .genre-chip, .trait-chip {{ padding: 4px 12px; border-radius: 12px; font-size: 11px; cursor: pointer; transition: all 0.2s; border: 1px solid transparent; }}
        .genre-chip:hover, .trait-chip:hover {{ transform: scale(1.05); }}
        .genre-chip.active, .trait-chip.active {{ border-color: currentColor; box-shadow: 0 0 10px currentColor; }}

        #chart {{ position: relative; background: var(--bg-secondary); border-radius: 12px; overflow: hidden; margin: 10px 0; }}

        .timeline-axis {{ position: absolute; bottom: 5px; left: 50px; right: 20px; height: 20px; display: flex; justify-content: space-between; }}
        .timeline-tick {{ font-size: 10px; color: var(--text-dim); }}

        .pop-label {{ position: absolute; left: 5px; font-size: 9px; color: var(--text-dim); transform: translateY(-50%); }}

        .artist-card {{ position: absolute; width: 44px; height: 44px; background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 6px; padding: 3px; cursor: pointer; transition: all 0.3s ease; z-index: 10; }}
        .artist-card:hover, .artist-card.selected {{ transform: scale(1.15); box-shadow: 0 4px 20px rgba(0,0,0,0.5); z-index: 50; border-color: var(--accent-blue); }}
        .artist-card.selected {{ border-color: var(--accent-green); }}

        .artist-avatar {{ width: 100%; height: 100%; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 18px; background: linear-gradient(135deg, #333, #222); }}

        .artist-tooltip {{ position: absolute; bottom: 100%; left: 50%; transform: translateX(-50%); background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 4px; padding: 4px 8px; white-space: nowrap; font-size: 10px; opacity: 0; pointer-events: none; transition: opacity 0.2s; margin-bottom: 4px; z-index: 100; }}
        .artist-card:hover .artist-tooltip {{ opacity: 1; }}

        .track-dot {{ position: absolute; width: 8px; height: 8px; border-radius: 50%; cursor: pointer; transition: all 0.2s; transform: translate(-50%, -50%); z-index: 5; opacity: 0.7; }}
        .track-dot:hover {{ transform: translate(-50%, -50%) scale(1.5); opacity: 1; z-index: 60; }}

        .info-panel {{ position: fixed; right: 20px; top: 50%; transform: translateY(-50%); width: 280px; background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 12px; padding: 16px; z-index: 1000; display: none; }}
        .info-panel.visible {{ display: block; }}
        .info-panel h3 {{ margin-bottom: 8px; font-size: 14px; }}
        .info-panel .track-list {{ max-height: 300px; overflow-y: auto; }}
        .info-panel .track {{ padding: 6px 0; border-bottom: 1px solid var(--card-border); font-size: 11px; cursor: pointer; }}
        .info-panel .track:hover {{ color: var(--accent-blue); }}
        .info-panel .close {{ position: absolute; top: 8px; right: 12px; cursor: pointer; font-size: 18px; color: var(--text-dim); }}
    </style>
</head>
<body>
    <h1>Music DNA — 206 Artists, 314 Tracks</h1>

    <div class="genres-row" id="genresRow"></div>
    <div id="chart"></div>
    <div class="traits-row" id="traitsRow"></div>

    <div class="info-panel" id="infoPanel">
        <span class="close" onclick="deselectArtist()">×</span>
        <h3 id="panelTitle"></h3>
        <div class="track-list" id="trackList"></div>
    </div>

    <script>
        const genres = [
            {{ id: 'g1', name: 'Русский рок', color: '#ff6b6b' }},
            {{ id: 'g2', name: 'Рэп', color: '#ffd93d' }},
            {{ id: 'g3', name: 'World/Folk', color: '#6bcb77' }},
            {{ id: 'g4', name: 'Электроника', color: '#4ecdc4' }},
            {{ id: 'g5', name: 'Классика/Орк.', color: '#9d4edd' }},
            {{ id: 'g6', name: 'Метал', color: '#e63946' }},
            {{ id: 'g7', name: 'Авторская', color: '#ff85a2' }},
            {{ id: 'g8', name: 'Саундтреки', color: '#7b68ee' }}
        ];

        const traits = [
            {{ id: 't1', name: 'Протест', color: '#ef4444' }},
            {{ id: 't2', name: 'Ирония', color: '#f59e0b' }},
            {{ id: 't3', name: 'Поэзия', color: '#8b5cf6' }},
            {{ id: 't4', name: 'Этника', color: '#10b981' }},
            {{ id: 't5', name: 'Эпик', color: '#3b82f6' }},
            {{ id: 't6', name: 'Драйв', color: '#ec4899' }},
            {{ id: 't7', name: 'Меланхолия', color: '#6366f1' }},
            {{ id: 't8', name: 'Эксперимент', color: '#14b8a6' }}
        ];

        const artists = [
{chr(10).join(artists_js)}
        ];

        const singleTracks = [
{chr(10).join(singles_js)}
        ];

        // Genre connections (artist id -> genre ids)
        const genreToArtist = [
            // Russian rock
            {{ source: 'g1', targets: ['a17', 'a36', 'a41', 'a61', 'a64', 'a67', 'a69', 'a76', 'a84'] }},
            // Rap
            {{ source: 'g2', targets: ['a23', 'a29', 'a42', 'a43', 'a50', 'a51', 'a63', 'a85'] }},
            // World/Folk
            {{ source: 'g3', targets: ['a26', 'a33', 'a44', 'a54', 'a55', 'a66', 'a71', 'a91', 'a93'] }},
            // Electronic
            {{ source: 'g4', targets: ['a35', 'a39', 'a56', 'a86'] }},
            // Classical
            {{ source: 'g5', targets: ['a73', 'a75'] }},
            // Metal
            {{ source: 'g6', targets: ['a44', 'a47', 'a49', 'a54', 'a83'] }},
            // Author songs
            {{ source: 'g7', targets: ['a34', 'a62', 'a65', 'a66', 'a68', 'a77', 'a78', 'a79', 'a82', 'a87', 'a88', 'a89', 'a92', 'a94', 'a95', 'a96'] }},
            // Soundtracks
            {{ source: 'g8', targets: ['a8'] }}
        ];

        // Trait connections
        const artistToTrait = [
            {{ source: 'a17', targets: ['t1', 't7'] }},
            {{ source: 'a23', targets: ['t1', 't2'] }},
            {{ source: 'a26', targets: ['t4', 't8'] }},
            {{ source: 'a29', targets: ['t1', 't3'] }},
            {{ source: 'a33', targets: ['t6', 't4'] }},
            {{ source: 'a34', targets: ['t3', 't7'] }},
            {{ source: 'a36', targets: ['t7', 't3'] }},
            {{ source: 'a41', targets: ['t8', 't7'] }},
            {{ source: 'a42', targets: ['t1', 't2'] }},
            {{ source: 'a43', targets: ['t1', 't3'] }},
            {{ source: 'a44', targets: ['t4', 't6'] }},
            {{ source: 'a50', targets: ['t2', 't1'] }},
            {{ source: 'a51', targets: ['t1', 't5'] }},
            {{ source: 'a54', targets: ['t4', 't6'] }},
            {{ source: 'a55', targets: ['t4', 't7'] }},
            {{ source: 'a56', targets: ['t7', 't8'] }},
            {{ source: 'a60', targets: ['t4', 't8'] }},
            {{ source: 'a61', targets: ['t6', 't1'] }},
            {{ source: 'a62', targets: ['t1', 't3'] }},
            {{ source: 'a63', targets: ['t1', 't2'] }},
            {{ source: 'a64', targets: ['t1', 't7'] }},
            {{ source: 'a65', targets: ['t3', 't7'] }},
            {{ source: 'a66', targets: ['t4', 't3'] }},
            {{ source: 'a67', targets: ['t7', 't4'] }},
            {{ source: 'a68', targets: ['t3', 't1'] }},
            {{ source: 'a69', targets: ['t7'] }},
            {{ source: 'a71', targets: ['t4', 't7'] }},
            {{ source: 'a72', targets: ['t7', 't1'] }},
            {{ source: 'a77', targets: ['t3', 't7'] }},
            {{ source: 'a78', targets: ['t1', 't2'] }},
            {{ source: 'a79', targets: ['t2', 't7'] }},
            {{ source: 'a82', targets: ['t2', 't3'] }},
            {{ source: 'a83', targets: ['t4', 't7'] }},
            {{ source: 'a84', targets: ['t1', 't3'] }},
            {{ source: 'a85', targets: ['t1', 't2'] }},
            {{ source: 'a86', targets: ['t4', 't6'] }},
            {{ source: 'a87', targets: ['t1', 't3'] }},
            {{ source: 'a88', targets: ['t3', 't7'] }},
            {{ source: 'a89', targets: ['t1', 't6'] }},
            {{ source: 'a91', targets: ['t4', 't7'] }},
            {{ source: 'a92', targets: ['t3', 't6'] }},
            {{ source: 'a93', targets: ['t4', 't3'] }},
            {{ source: 'a94', targets: ['t1', 't2', 't3'] }},
            {{ source: 'a95', targets: ['t1', 't2'] }},
            {{ source: 'a96', targets: ['t7', 't3'] }}
        ];

        // Popularity tiers for Y-axis labels
        const popTiers = [
            {{ value: 1000000, label: '1M+' }},
            {{ value: 100000, label: '100K' }},
            {{ value: 10000, label: '10K' }},
            {{ value: 1000, label: '1K' }}
        ];

        // Calculate median year for each artist
        artists.forEach(a => {{
            // Dummy years based on typical release periods - you can enhance this
            a.medianYear = 2010; // Default
        }});

        // Setup
        const chart = document.getElementById('chart');
        const width = Math.min(1400, window.innerWidth - 40);
        const height = Math.min(600, window.innerHeight - 250);
        chart.style.width = width + 'px';
        chart.style.height = height + 'px';

        const minYear = 1968, maxYear = 2025;
        const leftPadding = 60, rightPadding = 20, topPadding = 50, bottomPadding = 50;
        const timelineWidth = width - leftPadding - rightPadding;
        const chartHeight = height - topPadding - bottomPadding;
        const cardSize = 44;

        function yearToX(year) {{
            return leftPadding + ((year - minYear) / (maxYear - minYear)) * timelineWidth;
        }}

        // Popularity to Y (log scale, higher = top)
        const minPop = Math.min(...artists.map(a => a.popularity), ...singleTracks.map(t => t.popularity));
        const maxPop = Math.max(...artists.map(a => a.popularity), ...singleTracks.map(t => t.popularity));
        const logMin = Math.log10(Math.max(100, minPop));
        const logMax = Math.log10(maxPop);

        function popularityToY(pop) {{
            const logPop = Math.log10(Math.max(100, pop));
            const normalized = 1 - (logPop - logMin) / (logMax - logMin);
            return topPadding + normalized * chartHeight;
        }}

        // Create SVG
        const svg = d3.select('#chart').append('svg')
            .attr('width', width)
            .attr('height', height);

        // Timeline axis
        const axisDiv = document.createElement('div');
        axisDiv.className = 'timeline-axis';
        for (let year = 1970; year <= 2020; year += 10) {{
            const tick = document.createElement('div');
            tick.className = 'timeline-tick';
            tick.textContent = year;
            tick.style.left = `${{((year - minYear) / (maxYear - minYear)) * 100}}%`;
            axisDiv.appendChild(tick);
        }}
        chart.appendChild(axisDiv);

        // Popularity labels
        popTiers.forEach(tier => {{
            if (tier.value >= minPop && tier.value <= maxPop) {{
                const label = document.createElement('div');
                label.className = 'pop-label';
                label.textContent = tier.label;
                label.style.top = `${{popularityToY(tier.value)}}px`;
                chart.appendChild(label);
            }}
        }});

        // Render genre chips
        const genresRow = document.getElementById('genresRow');
        genres.forEach(g => {{
            const chip = document.createElement('div');
            chip.className = 'genre-chip';
            chip.textContent = g.name;
            chip.style.background = g.color + '30';
            chip.style.color = g.color;
            chip.dataset.id = g.id;
            chip.onmouseenter = () => highlightGenre(g.id, true);
            chip.onmouseleave = () => highlightGenre(g.id, false);
            genresRow.appendChild(chip);
        }});

        // Render trait chips
        const traitsRow = document.getElementById('traitsRow');
        traits.forEach(t => {{
            const chip = document.createElement('div');
            chip.className = 'trait-chip';
            chip.textContent = t.name;
            chip.style.borderColor = t.color;
            chip.style.color = t.color;
            chip.dataset.id = t.id;
            chip.onmouseenter = () => highlightTrait(t.id, true);
            chip.onmouseleave = () => highlightTrait(t.id, false);
            traitsRow.appendChild(chip);
        }});

        // Position artists
        artists.forEach((artist, i) => {{
            artist.x = leftPadding + (i / artists.length) * timelineWidth - cardSize / 2;
            artist.y = popularityToY(artist.popularity) - cardSize / 2;

            // Clamp
            artist.x = Math.max(leftPadding, Math.min(artist.x, width - cardSize - rightPadding));
            artist.y = Math.max(topPadding, Math.min(artist.y, height - bottomPadding - cardSize));
        }});

        // Create artist cards
        let selectedArtist = null;
        const allDots = [];

        artists.forEach(artist => {{
            const card = document.createElement('div');
            card.className = 'artist-card';
            card.style.cssText = `left: ${{artist.x}}px; top: ${{artist.y}}px;`;
            card.dataset.id = artist.id;

            card.innerHTML = `
                <div class="artist-avatar">${{artist.name.charAt(0)}}</div>
                <div class="artist-tooltip">${{artist.name}}</div>
            `;

            card.onclick = () => selectArtist(artist);
            chart.appendChild(card);
        }});

        // Create dots for single tracks
        singleTracks.forEach(track => {{
            const dot = document.createElement('div');
            dot.className = 'track-dot';
            const x = leftPadding + Math.random() * timelineWidth;
            const y = popularityToY(track.popularity);
            dot.style.cssText = `left: ${{x}}px; top: ${{y}}px; background: #666;`;
            dot.title = `${{track.artist}} - ${{track.title}}`;
            dot.onclick = () => window.open(`https://www.youtube.com/results?search_query=${{encodeURIComponent(track.search)}}`, '_blank');
            chart.appendChild(dot);
            allDots.push({{ dot, popularity: track.popularity }});
        }});

        function selectArtist(artist) {{
            if (selectedArtist) {{
                document.querySelector(`.artist-card[data-id="${{selectedArtist.id}}"]`)?.classList.remove('selected');
            }}
            selectedArtist = artist;
            document.querySelector(`.artist-card[data-id="${{artist.id}}"]`)?.classList.add('selected');

            const panel = document.getElementById('infoPanel');
            document.getElementById('panelTitle').textContent = artist.name;
            document.getElementById('trackList').innerHTML = artist.tracks.map(t =>
                `<div class="track" onclick="window.open('https://www.youtube.com/results?search_query=${{encodeURIComponent(t.search)}}', '_blank')">${{t.title}}</div>`
            ).join('');
            panel.classList.add('visible');
        }}

        function deselectArtist() {{
            if (selectedArtist) {{
                document.querySelector(`.artist-card[data-id="${{selectedArtist.id}}"]`)?.classList.remove('selected');
            }}
            selectedArtist = null;
            document.getElementById('infoPanel').classList.remove('visible');
            updateHighlight(null);
        }}

        function highlightGenre(gid, on) {{
            const conn = genreToArtist.find(c => c.source === gid);
            const artistIds = conn ? new Set(conn.targets) : new Set();
            updateHighlight(on ? artistIds : null);

            document.querySelectorAll('.genre-chip').forEach(el => {{
                el.classList.toggle('active', on && el.dataset.id === gid);
            }});
        }}

        function highlightTrait(tid, on) {{
            const artistIds = new Set();
            artistToTrait.forEach(c => {{
                if (c.targets.includes(tid)) artistIds.add(c.source);
            }});
            updateHighlight(on ? artistIds : null);

            document.querySelectorAll('.trait-chip').forEach(el => {{
                el.classList.toggle('active', on && el.dataset.id === tid);
            }});
        }}

        function updateHighlight(artistIds) {{
            document.querySelectorAll('.artist-card').forEach(el => {{
                if (artistIds) {{
                    el.style.display = artistIds.has(el.dataset.id) ? 'block' : 'none';
                }} else {{
                    el.style.display = 'block';
                }}
            }});
        }}

        document.onclick = (e) => {{
            if (selectedArtist && !e.target.closest('.artist-card') && !e.target.closest('.info-panel')) {{
                deselectArtist();
            }}
        }};
    </script>
</body>
</html>
'''

with open('/Users/lance/Documents/claude-code-course/artifacts/music-sankey/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated HTML with {len(card_artists)} card artists and {len(single_artists)} single-track dots")
print(f"Total: {len(artists)} artists")
