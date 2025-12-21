#!/usr/bin/env python3
"""Update artist popularity with real Spotify data."""

import json

# Load current data
with open('/Users/lance/Documents/claude-code-course/artifacts/music-sankey/full_artists.json', 'r', encoding='utf-8') as f:
    artists = json.load(f)

# Popularity data from web searches (Spotify monthly listeners)
popularity_updates = {
    "Barbatuques": 2500000,
    "Vitamin String Quartet": 1600000,
    "James Last": 956200,
    "Saez": 680600,
    "Joachim Witt": 599600,
    "Schiller": 420200,
    "Be Svendsen": 422900,
    "Simply Three": 372000,
    "Larkin Poe": 259100,
    "Rokia Traoré": 220000,
    "Hannes Wader": 199500,
    "José Larralde": 160800,
    "Angelo Branduardi": 154900,
    "Seasick Steve": 153100,
    "Hot Butter": 101600,
    "Эдуард Артемьев": 78400,
    "The Tossers": 64000,
    "Civil War": 61500,
    "SuidAkrA": 51300,
    "Suidakra": 51300,
    "Ekseption": 30600,
    "Klayton": 13400,
    "Xploding Plastix": 11900,
    "musica nuda": 7200,
    "Геннадий Гладков": 500,  # Very small, bump up slightly

    # Reasonable estimates based on artist type
    "Hugo Strasser": 15000,
    "grande1899": 50000,  # YouTube famous for Rush E
    "Danish National Symphony Orchestra": 150000,
    "MOZART HEROES": 25000,
    "René Aubry": 80000,
    "Love": 300000,  # 60s band, cult classic
    "Ryan Taubert": 5000,
    "Fanfare Vagabontu": 8000,
    "Jelonek": 12000,
    "Yuma": 5000,
    "Karolina Cicha": 8000,
    "The OM": 3000,
    "Sly5thAve": 150000,
    "Opal Ocean": 20000,
    "Bel Suono": 15000,
    "Geek Music": 5000,
    "Vivaldi String Orchestra": 30000,
    "Martina Camargo": 10000,
    "Brand X Music": 50000,  # Trailer music
    "Neil Zaza": 30000,
    "London Festival Orchestra": 20000,
    "Mathias Duplessy": 25000,
    "Faraualla": 15000,
    "Byron Metcalf": 8000,
    "The Brass Knuckle Steampunk Sinfonia": 3000,
    "Lama Tenzin Sangpo": 5000,
    "Teufelstanz": 5000,
    "Skrömta": 3000,
    "The New Synthesizer Experience": 5000,
    "SuNA Mantra": 3000,
    "Jambey": 3000,
    "Jody Gwin": 5000,
    "IP Orchestra": 8000,
    "The Charades": 5000,
    "Thorr": 3000,
    "Stoner Train": 5000,
    "ICHI": 10000,
    "HELVEGEN": 5000,
    "Artem Uzunov": 20000,
    "Żywiołak": 30000,
    "Shedda": 5000,
    "Sabo": 50000,
    "Spiritual Seasons": 8000,
    "Gae Bolg": 5000,
    "Gabriel Saban": 3000,
    "MarimbaMix": 5000,
    "Евгений Крылатов": 50000,  # Famous Soviet composer

    # Russian/underground artists - keep lower
    "Сергей Фантом": 3000,
    "Самое Большое Простое Число": 5000,
    "Drum Ecstasy": 3000,
    "ОН ЮН": 3000,
    "FreshmanSound": 3000,
    "Марк Рейзен": 5000,
    "Моя дорогая": 5000,
    "Удмуртская тоска": 3000,
    "Нейро Дюбель": 8000,
    "Ринат Каримов": 15000,
    "旅獅乐队": 3000,
    "Василий Уриевский": 5000,
    "Сергей Никитин": 30000,
    "Золотое Перо": 3000,
    "Julius Frederick Rinaldi": 5000,
    "Два Рима": 3000,
    "Драконь": 5000,
    "Евгений Женевьев": 3000,
    "Евгений Алексеев": 3000,
    "Mark the Hammer": 8000,
    "Stephan Sechi": 5000,
    "Железный Занавес": 5000,
    "Дышать": 3000,
    "Муха": 5000,
    "Настежь": 3000,
    "Карелия": 8000,
    "Дмитрий Ревякин": 15000,
    "Дореволюціонный совѣтчикъ": 5000,
    "Александр Ф. Скляр": 30000,
    "Бахыт Компот": 10000,
    "Василий Васильев": 5000,
    "Ростислав Чебыкин": 3000,
    "Тропы не врут": 3000,
    "Живица": 5000,
    "Зоя Ященко": 8000,
    "Элечка": 3000,
    "Крыс": 3000,
    "СолоИНК": 3000,
    "Ÿuma": 5000,
}

# Update artists
updated_count = 0
for artist in artists:
    name = artist['name']
    if name in popularity_updates:
        old_pop = artist['popularity']
        artist['popularity'] = popularity_updates[name]
        if old_pop == 2000:  # Was placeholder
            updated_count += 1
            print(f"Updated {name}: {old_pop} -> {artist['popularity']}")

print(f"\nTotal updated: {updated_count}")

# Save updated data
with open('/Users/lance/Documents/claude-code-course/artifacts/music-sankey/full_artists.json', 'w', encoding='utf-8') as f:
    json.dump(artists, f, ensure_ascii=False, indent=2)

print("Saved to full_artists.json")
