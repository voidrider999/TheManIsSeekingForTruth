import pygame
import os

pygame.init()

files = [
    "desert.jpg", "taiga.jpg", "ocean.jpg",
    "mountains.jpg", "forest.jpg", "steppe.jpg",
    "mushroom_plain.jpg", "icon.jpg"
]

print("Проверка наличия файлов в текущей папке:")
for file in files:
    if os.path.exists(file):
        print(f"✓ {file} — найден")
    else:
        print(f"✗ {file} — не найден. Проверьте имя и расположение")

print("\nПопытка загрузки файлов в PyGame:")
for file in files:
    try:
        img = pygame.image.load(file)
        print(f"✓ {file} — загружен успешно")
    except Exception as e:
        print(f"✗ {file} — ошибка загрузки: {e}")

pygame.quit()

