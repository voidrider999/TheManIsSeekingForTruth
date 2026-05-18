import argparse
import math
import random

import pygame

parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true')
args = parser.parse_args()

SCREEN_W, SCREEN_H = 800, 600
GRID_X, GRID_Y = 20, 20 # Левый верхний угол таблицы в пикселях
PLAYER_DEBUG_COLOR = (0, 0, 0)
MAX_STEPS = 80

pygame.init()
window = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("TheManIsSeekingForTruth")

pygame.mixer.init()
pygame.mixer_music.load('harmony_in_the_mists_loop.ogg')
pygame.mixer.music.play(-1)

STATHAM_QUOTES = [
    "Если тебе где-то не рады в трусах, значит, пришел в шубе. Запомни.",
    "Неважно, с какой скоростью ты двигаешься, главное — не останавливаться.",
    "Если упал — встань. Если встал — упал, значит шнурки связались.",
    "Лучше быть последним в списке миллионеров, чем первым на уборку.",
    "Живи, кайфуй, гуляй, делай грязь... Главное, чтобы мама не узнала."
]
current_quote = random.choice(STATHAM_QUOTES)

def randpos():
    return random.choice(list(range(0, 4)) + list(range(13, 17)))

def draw_biome(window, base_image, player_pos, truth_pos, draw_pos, gameover):
    player_row, player_col = player_pos

    # 1. Если это центр ИЛИ игра окончена — картинка статична (масштаб 1.0)
    if (player_row == 8 and player_col == 8) or gameover:
        pulse = 1.0
    else:
        # 2. Обычный расчет пульса для игрового процесса
        target_row, target_col = (8, 8) if truth_pos is None else truth_pos
        distance = abs(player_row - target_row) + abs(player_col - target_col)
        distance = max(1.0, min(distance, 16.0))

        heart_rate = 0.0099 - (distance * 0.0004)
        time_val = pygame.time.get_ticks() * heart_rate

        beat1 = math.sin(time_val) ** 16
        beat2 = 0.5 * math.sin(time_val + 0.4) ** 16
        cardiogram = beat1 + beat2
        pulse = 1.0 + cardiogram * 0.08

    # 3. Расчет геометрии и отрисовка
    orig_w, orig_h = base_image.get_size()
    new_w = int(orig_w * pulse)
    new_h = int(orig_h * pulse)

    offset_x = (204 - new_w) // 2
    offset_y = (204 - new_h) // 2
    start_x, start_y = draw_pos

    animated_image = pygame.transform.scale(base_image, (new_w, new_h))
    window.blit(animated_image, (start_x + offset_x, start_y + offset_y))

def draw_word_wrap_text(window, text, font, color, rect):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        if font.size(test_line)[0] <= rect.width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    y = rect.top
    for line in lines:
        text_surface = font.render(line, True, color)
        window.blit(text_surface, (rect.left, y))  # Здесь теперь тоже window
        y += font.get_linesize()

player_col, player_row = randpos(), randpos()
truth_pos = None

steps_count = 0
font = pygame.font.SysFont(None, 32) # Стандартный шрифт, размер 32
gameover_font = pygame.font.SysFont(None, 100)

morpheus_small = pygame.image.load("morpheus.jpg")
morpheus_small = pygame.transform.scale(morpheus_small, (30, 30))

biomes = {
    (0, 0, 0): "morpheus.jpg",
    (255, 255, 0): "desert.jpg",
    (0, 100, 0): "taiga.jpg",
    (0, 0, 255): "ocean.jpg",
    (128, 128, 128): "mountains.jpg",
    (0, 128, 0): "forest.jpg",
    (165, 42, 42): "steppe.jpg",
    (128, 0, 128): "mushroom_plain.jpg"
}
biome_colors = list(biomes.keys())[1:] # все кроме Морфеуса
biome_images = {}
for biome_color, biome_file in biomes.items():
    image = pygame.image.load(biome_file)
    biome_images[biome_color] = pygame.transform.scale(image, (204, 204))

grid = []
oceans = []
for row in range(17):
    grid_row = []
    for col in range(17):
        if row == 8 and col == 8:
            biome_color = (0, 0, 0)  # Морфеус в центре
        else:
            biome_color = random.choice(biome_colors)
            if biome_color == (0, 0, 255):
                oceans.append((row, col))
        grid_row.append(biome_color)
    grid.append(grid_row)

gameover = False
overlay = pygame.Surface((SCREEN_W, SCREEN_H))
overlay.set_alpha(128)
overlay.fill((0, 0, 0))

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not gameover:
            old_pos = (player_row, player_col)
            new_row, new_col = player_row, player_col

            # 1. Рассчитываем новые координаты от нажатия кнопки
            if event.key == pygame.K_LEFT:
                new_col -= 1
            elif event.key == pygame.K_RIGHT:
                new_col += 1
            elif event.key == pygame.K_UP:
                new_row -= 1
            elif event.key == pygame.K_DOWN:
                new_row += 1

            # 2. Проверяем выход за границы карты
            if new_row < 0 or new_row > 16 or new_col < 0 or new_col > 16:
                current_quote = "Путь заблокирован. Здесь не пройти."
                continue

            # 3. Проверяем, не уперлись ли мы в Горы (Серый цвет)
            target_biome = grid[new_row][new_col]
            if target_biome == (128, 128, 128):
                current_quote = "Путь заблокирован. Здесь не пройти."
                continue

            # 4. Телепорт Океана (Синий цвет)
            if target_biome == (0, 0, 255) and len(oceans) > 1:
                teleport_targets = oceans.copy()
                teleport_targets.remove((new_row, new_col)) # Исключаем клетку захода
                new_row, new_col = random.choice(teleport_targets) # Прыгаем в случайный океан

            # 5. Применяем итоговые координаты
            player_row, player_col = new_row, new_col

            # Если шаг успешно сделан (и это не был удар об стену)
            if (player_row, player_col) != old_pos:
                steps_count += 1
                current_quote = random.choice(STATHAM_QUOTES)

    steps_left = MAX_STEPS - steps_count
    if steps_left == 0:
        gameover = True

    if player_row == 8 and player_col == 8 and truth_pos is None:
        while True:
            truth_pos = (randpos(), randpos())
            truth_biome = grid[truth_pos[0]][truth_pos[1]]
            # Если это не горы (128, 128, 128) и не океан (0, 0, 255), то берем
            if truth_biome != (128, 128, 128) and truth_biome != (0, 0, 255):
                break

    if truth_pos and (player_row, player_col) == truth_pos:
        gameover = True

    window.fill((234, 212, 252))
    for row in range(17):
        for col in range(17):
            rect = (col * 30 + GRID_X, row * 30 + GRID_Y)
            biome_color = grid[row][col]
            if args.debug and (row, col) == (player_row, player_col):
                pygame.draw.rect(window, PLAYER_DEBUG_COLOR, (rect[0], rect[1], 30, 30))
            elif row == 8 and col == 8:
                window.blit(morpheus_small, (rect[0], rect[1]))
            else:
                pygame.draw.rect(window, biome_color, (rect[0], rect[1], 30, 30))

    # Рисовать биом
    current_color = grid[player_row][player_col]
    biome_image = biome_images[current_color]
    player_pos = (player_row, player_col)
    draw_biome(window, biome_image, player_pos, truth_pos, (565, 20), gameover)

    quote_rect = pygame.Rect(565, 235, 204, 130)
    quote_font = pygame.font.SysFont(None, 20, bold=True)
    draw_word_wrap_text(window, current_quote, quote_font, (50, 20, 50), quote_rect)

    # Рисовать мини-карту
    if truth_pos:
        for row in range(17):
            for col in range(17):
                rect = (565 + col * 12, 326 + row * 12, 12, 12)
                biome_color = grid[row][col]

                if (row, col) == truth_pos:
                    if (pygame.time.get_ticks() // 500) % 2 == 0:
                        display_color = (255, 0, 255)
                    else:
                        display_color = (50, 200, 200)
                else:
                    display_color = biome_color

                pygame.draw.rect(window, display_color, rect)

    # Отрисовка текста под основной картой
    steps_text = font.render(f"Осталось шагов: {steps_left}", True, (0, 0, 0))
    window.blit(steps_text, (GRID_X, 540)) # 10 пикселей отступ под сеткой

    if gameover:
        window.blit(overlay, (0, 0))
        if truth_pos and (player_row, player_col) == truth_pos:
            gameover_text = gameover_font.render("ПОБЕДА", True, (255, 0, 0))
        else:
            gameover_text = gameover_font.render("ПОРАЖЕНИЕ", True, (255, 0, 0))
        text_rect = gameover_text.get_rect(center=(SCREEN_W // 2, SCREEN_H - 35))
        window.blit(gameover_text, text_rect)

    pygame.display.update()
    clock.tick(60)
pygame.quit()
