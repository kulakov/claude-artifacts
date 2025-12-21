#!/usr/bin/env python3
"""
Скрипт для скачивания и обрезки фото артистов через Last.fm API
Результат: квадратные фото 300x300 в папке artists_photos/
"""

import requests
from PIL import Image
from io import BytesIO
import os
import time
import re

# ============================================
# НАСТРОЙКИ
# ============================================

# Получите бесплатный API ключ здесь: https://www.last.fm/api/account/create
LASTFM_API_KEY = "bb56796a71ba3fc00d2e8106b6215c3f"

OUTPUT_DIR = "artists_photos"
SIZE = 300

# ============================================
# СПИСОК АРТИСТОВ
# ============================================

ARTISTS = [
    # Международные
    "Barbatuques",
    "Be Svendsen",
    "Bel Suono",
    "Blackmore's Night",  # уточнённое имя для Blackmore
    "Brand X Music",
    "Civil War",
    "Danish National Symphony Orchestra",
    "Drum Ecstasy",
    "Fanfare Vagabontu",
    "FreshmanSound",
    "Geek Music",
    "Jelonek",
    "Jody Gwin",
    "José Larralde",
    "Julius Frederick Rinaldi",
    "Karolina Cicha",
    "Klayton",
    "Lama Tenzin Sangpo",
    "Larkin Poe",
    "Love",
    "MarimbaMix",
    "Martina Camargo",
    "Opal Ocean",
    "Ryan Taubert",
    "Sly5thAve",
    "Steve Roach",  # уточнённое имя для Steve
    "Suidakra",
    "The Charades",
    "Om",  # The OM
    "Vivaldi String Orchestra",
    "Yuma",
    "Zodiac",
    "Grandayy",  # grande1899

    # Русскоязычные
    "Василий Уриевский",
    "Владимир Федосеев",
    "Два Рима",
    "Заточка",
    "Золотое Перо",
    "Кирилл Комаров",
    "Марк Рейзен",
    "Моя Дорогая",
    "Он Юн",
    "Ринат Каримов",
    "Ростислав Чебыкин",
    "Самое Большое Простое Число",
    "Сергей Никитин",
    "Сергей Фантом",
    "Эрнесто Заткнитесь",
]

# ============================================
# ФУНКЦИИ
# ============================================

def sanitize_filename(name):
    """Очистка имени файла от недопустимых символов"""
    return re.sub(r'[<>:"/\\|?*]', '_', name)


def get_lastfm_image(artist_name, api_key):
    """Получить URL изображения артиста через Last.fm API"""
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "artist.getinfo",
        "artist": artist_name,
        "api_key": api_key,
        "format": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if "artist" in data and "image" in data["artist"]:
            images = data["artist"]["image"]
            # Берём самое большое изображение (последнее в списке)
            for img in reversed(images):
                if img.get("#text"):
                    return img["#text"]
    except Exception as e:
        print(f"  Ошибка API: {e}")

    return None


def download_and_crop(image_url, output_path, size=300):
    """Скачать изображение и обрезать до квадрата"""
    try:
        response = requests.get(image_url, timeout=15)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content))

        # Конвертируем в RGB если нужно (для PNG с прозрачностью)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        # Обрезаем до квадрата по центру
        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim

        img = img.crop((left, top, right, bottom))

        # Изменяем размер до 300x300
        img = img.resize((size, size), Image.LANCZOS)

        # Сохраняем
        img.save(output_path, "JPEG", quality=90)
        return True

    except Exception as e:
        print(f"  Ошибка скачивания: {e}")
        return False


def main():
    if LASTFM_API_KEY == "YOUR_API_KEY_HERE":
        print("=" * 60)
        print("ОШИБКА: Нужен API ключ Last.fm!")
        print()
        print("1. Перейдите на: https://www.last.fm/api/account/create")
        print("2. Создайте приложение (любое название)")
        print("3. Скопируйте API Key")
        print("4. Вставьте в переменную LASTFM_API_KEY в этом файле")
        print("=" * 60)
        return

    # Создаём папку для фото
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Скачивание фото для {len(ARTISTS)} артистов...")
    print(f"Папка: {OUTPUT_DIR}/")
    print("-" * 50)

    success = 0
    failed = []

    for i, artist in enumerate(ARTISTS, 1):
        print(f"[{i}/{len(ARTISTS)}] {artist}...", end=" ")

        # Получаем URL изображения
        image_url = get_lastfm_image(artist, LASTFM_API_KEY)

        if not image_url:
            print("❌ не найдено на Last.fm")
            failed.append(artist)
            continue

        # Формируем имя файла
        filename = sanitize_filename(artist) + ".jpg"
        output_path = os.path.join(OUTPUT_DIR, filename)

        # Скачиваем и обрезаем
        if download_and_crop(image_url, output_path, SIZE):
            print(f"✅ сохранено")
            success += 1
        else:
            print("❌ ошибка скачивания")
            failed.append(artist)

        # Пауза чтобы не перегружать API
        time.sleep(0.3)

    # Итоги
    print("-" * 50)
    print(f"Готово! Успешно: {success}/{len(ARTISTS)}")

    if failed:
        print(f"\nНе удалось найти ({len(failed)}):")
        for name in failed:
            print(f"  - {name}")
        print("\nДля этих артистов нужно скачать фото вручную.")


if __name__ == "__main__":
    main()
