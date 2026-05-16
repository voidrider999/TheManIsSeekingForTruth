import pygame
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true')
args = parser.parse_args()

SCREEN_W, SCREEN_H = 800, 600
GRID_X, GRID_Y = 20, 20 # Левый верхний угол таблицы в пикселях
PLAYER_DEBUG_COLOR = (0, 0, 0)

pygame.init()
window = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("TheManIsSeekingForTruth")

pygame.mixer.init()
pygame.mixer_music.load('harmony_in_the_mists_loop.ogg')
pygame.mixer.music.play(-1)

def randpos():
    return random.choice(list(range(0, 4)) + list(range(13, 17)))

player_col, player_row = randpos(), randpos()
truth_pos = None

steps_count = 0
font = pygame.font.SysFont(None, 32) # Стандартный шрифт, размер 32
victory_font = pygame.font.SysFont(None, 100)

biomes = {
    (255, 255, 0): "desert.jpg",
    (0, 100, 0): "taiga.jpg",
    (0, 0, 255): "ocean.jpg",
    (128, 128, 128): "mountains.jpg",
    (0, 128, 0): "forest.jpg",
    (165, 42, 42): "steppe.jpg",
    (128, 0, 128): "mushroom_plain.jpg"
}
biome_colors = list(biomes.keys())
biome_images = {}
for biome_color, biome_file in biomes.items():
    image = pygame.image.load(biome_file)
    biome_images[biome_color] = pygame.transform.scale(image, (204, 204))

grid = []
for row in range(17):
    grid_row = []
    for col in range(17):
        biome_color = random.choice(biome_colors)
        grid_row.append(biome_color)
    grid.append(grid_row)

game_over = False
overlay = pygame.Surface((SCREEN_W, SCREEN_H))
overlay.set_alpha(128)
overlay.fill((0, 0, 0))

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            old_pos = (player_col, player_row)
            if event.key == pygame.K_LEFT and player_col > 0:
                player_col -= 1
            elif event.key == pygame.K_RIGHT and player_col < 16:
                player_col += 1
            elif event.key == pygame.K_UP and player_row > 0:
                player_row -= 1
            elif event.key == pygame.K_DOWN and player_row < 16:
                player_row += 1

            # Если кортеж координат изменился — прибавляем шаг
            if (player_col, player_row) != old_pos:
                steps_count += 1

    if player_row == 8 and player_col == 8 and truth_pos is None:
        truth_pos = (randpos(), randpos())

    if truth_pos and (player_row, player_col) == truth_pos:
        game_over = True

    window.fill((234, 212, 252))
    for row in range(17):
        for col in range(17):
            rect = (col * 30 + GRID_X, row * 30 + GRID_Y)
            biome_color = grid[row][col]
            if args.debug and (row, col) == (player_row, player_col):
                pygame.draw.rect(window, PLAYER_DEBUG_COLOR, (rect[0], rect[1], 30, 30))
            else:
                pygame.draw.rect(window, biome_color, (rect[0], rect[1], 30, 30))

    # Рисовать биом
    current_color = grid[player_row][player_col]
    biome_image = biome_images[current_color]
    window.blit(biome_image, (565, 20))

    # Рисовать мини-карту
    if truth_pos:
        for row in range(17):
            for col in range(17):
                rect = (565 + col * 12, 240 + row * 12, 12, 12)
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
    steps_text = font.render(f"Шаги: {steps_count}", True, (0, 0, 0)) # Черный текст
    window.blit(steps_text, (GRID_X, 540)) # 10 пикселей отступ под сеткой

    if game_over:
        window.blit(overlay, (0, 0))
        victory_text = victory_font.render("ПОБЕДА", True, (255, 0, 0))
        text_rect = victory_text.get_rect(center=(SCREEN_W // 2, SCREEN_H - 35))
        window.blit(victory_text, text_rect)

    pygame.display.update()
    clock.tick(60)
pygame.quit()
