#!/usr/bin/env python3
"""Auto-classify artists by genre and traits."""

import json
import re

# Load unclassified artists
with open('unclassified_artists.json', 'r') as f:
    artists = json.load(f)

# Genre keywords/patterns
genre_rules = {
    'soviet-rock': [
        'Алиса', 'Пикник', 'Ляпис', 'Би-2', 'LOUNA', 'Ноль', 'Аукцыон',
        'Гражданская оборона', 'Nautilus', 'Сплин', 'Кино', 'Аквариум',
        'Борис Гребенщиков', 'Янка', 'Настежь', 'Сурганова', 'Найк Борзов',
        'Ундервуд', 'Немного нервно', 'Дельфин', 'Монеточка', 'Нейро Дюбель'
    ],
    'world': [
        'Heilung', 'Corvus', 'Eivør', 'Heidevolk', 'Cruachan', 'Wardruna',
        'Nine Treasures', 'Anoushka', 'Krishna', 'Lama', 'Mathias Duplessy',
        'Faraualla', 'Dobranotch', 'Живица', 'Мельница', 'Żywiołak',
        'Celtic', 'Skrömta', 'Teufelstanz', 'Blackmore', 'Steeleye',
        'Rokia', 'Barbatuques', 'José Larralde', 'Nolwenn', 'Angelo',
        'Hannes Wader', 'Joanna Stingray', 'Yodelice', 'Brazzaville'
    ],
    'electronic': [
        'Jarre', 'Zimmer', 'Schiller', 'Klaus Schulze', 'Juno Reactor',
        'Max Cooper', 'Oliver Koletzki', 'Moby', 'Эдуард Артемьев',
        'Ramin Djawadi', 'Synthesizer', 'Ekseption', 'Zodiac', 'Sabo',
        'Xploding Plastix', 'Be Svendsen', 'Hot Butter'
    ],
    'neofolk': [
        'Corvus Corax', 'Heilung', 'Wardruna', 'Eivør', 'Heidevolk',
        'Die Apokalyptischen', 'Cruachan', 'Blackmore', 'Gae Bolg',
        'Teufelstanz', 'HELVEGEN', 'Spiritual Seasons', 'Suidakra',
        'Civil War', 'Sabaton', 'The Dreadnoughts', 'The Tossers'
    ],
    'virtuoso': [
        'Tommy Emmanuel', 'Rodrigo y Gabriela', 'Neil Zaza', 'Steve.*Seagulls',
        'Simply Three', 'Vitamin String', 'London Festival', 'MOZART HEROES',
        'musica nuda', 'Seasick Steve', 'ICHI', 'Larkin Poe', 'King Crimson',
        'Rainbow', 'Jelonek', 'Artem Uzunov', 'Mark the Hammer'
    ],
    'author': [
        'Высоцкий', 'Василий К', 'Драконь', 'Леона', 'Ольга Арефьева',
        'Вера Полозкова', 'Екатерина Яшникова', 'Тим Скоренко', 'Михаил Башаков',
        'Умка', 'Зоя Ященко', 'Евгений Алексеев', 'Евгений Женевьев',
        'Кирилл Комаров', 'Сергей Никитин', 'Leonard Cohen', 'Bob Dylan',
        'Tom Waits', 'Nick Cave', 'Saez', 'Joachim Witt'
    ],
    'modern-rap': [
        'Noize MC', 'Oxxxymiron', 'Каста', 'Anacondaz', 'Влади', 'Лигалайз',
        'ST1M', 'HORUS', 'DEEP-EX-SENSE', 'PALC', 'Эрнесто Заткнитесь',
        'Крыс', 'GREEN CROW'
    ],
    'soundtrack': [
        'Hans Zimmer', 'Ramin Djawadi', 'Эдуард Артемьев', 'Геннадий Гладков',
        'Seatbelts', 'Brand X Music', 'Ryan Taubert', 'Gabriel Saban',
        'Danish National', 'Vivaldi String', 'James Last', 'IP Orchestra',
        'Евгений Крылатов'
    ],
    'spiritual': [
        'Krishna Das', 'Lama Tenzin', 'Byron Metcalf', 'SuNA Mantra',
        'Jambey', 'Atlantida Project', 'Борис Гребенщиков', 'Аквариум'
    ],
    'irony': [
        'Bo Burnham', 'Пушной', 'Anacondaz', 'Дореволюціонный',
        'Бахыт Компот', 'Элечка', 'Markscheider', 'Django Django',
        'Phil Collins', 'Fleetwood Mac', 'David Bowie'
    ],
    'protest': [
        'Noize MC', 'Порнофильмы', 'Гражданская оборона', 'Ляпис',
        'LOUNA', 'Янка', 'Влади', 'Железный Занавес', 'Алиса'
    ],
    'melancholy': [
        'Nick Cave', 'Дельфин', 'Леона', 'Сплин', 'Tom Waits',
        'Leonard Cohen', 'Moby', 'Saez', 'Eivør', 'Янка Дягилева',
        'Ноль', 'Nautilus'
    ]
}

# Trait keywords
trait_rules = {
    't1': ['world', 'spiritual', 'electronic', 'neofolk'],  # Открытость
    't2': ['protest', 'modern-rap'],  # Антиавторитарность
    't3': ['world', 'virtuoso'],  # Космополитизм
    't4': ['melancholy', 'author'],  # Меланхолия
    't5': ['spiritual', 'electronic'],  # Созерцательность
    't6': ['irony'],  # Ирония
    't7': ['author', 'neofolk', 'soviet-rock'],  # Аутентичность
    't8': ['author', 'soviet-rock'],  # Интеллигенция
}

# Classify each artist
results = []
for artist in artists:
    name = artist['name']
    aid = artist['id']

    genres_found = []
    for genre, keywords in genre_rules.items():
        for kw in keywords:
            if re.search(kw, name, re.IGNORECASE):
                if genre not in genres_found:
                    genres_found.append(genre)
                break

    # Derive traits from genres
    traits_found = []
    for trait, genre_list in trait_rules.items():
        if any(g in genres_found for g in genre_list):
            if trait not in traits_found:
                traits_found.append(trait)

    results.append({
        'id': aid,
        'name': name,
        'genres': genres_found if genres_found else ['world'],  # default
        'traits': traits_found if traits_found else ['t1']  # default: Открытость
    })

# Output for review
print("| Артист | Жанры | Свойства |")
print("|--------|-------|----------|")

genre_names = {
    'soviet-rock': 'Рок', 'protest': 'Протест', 'world': 'World',
    'spiritual': 'Медитатив', 'author': 'Авторская', 'neofolk': 'Неофолк',
    'electronic': 'Электроника', 'virtuoso': 'Виртуозы', 'irony': 'Ирония',
    'soundtrack': 'Саундтреки', 'modern-rap': 'Рэп', 'melancholy': 'Меланхолия'
}

trait_names = {
    't1': 'Открытость', 't2': 'Антиавторитарность', 't3': 'Космополитизм',
    't4': 'Меланхолия', 't5': 'Созерцательность', 't6': 'Ирония',
    't7': 'Аутентичность', 't8': 'Интеллигенция'
}

for r in results:
    g = ', '.join([genre_names.get(x, x) for x in r['genres']])
    t = ', '.join([trait_names.get(x, x) for x in r['traits']])
    print(f"| {r['name']} | {g} | {t} |")

# Save for later use
with open('classification_draft.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
