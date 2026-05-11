import pygame
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true')
args = parser.parse_args()

SCREEN_W, SCREEN_H = 800, 600
GRID_X, GRID_Y = 20, 20 # Левый верхний угол таблицы в пикселях
PLAYER_DEBUG_COLOR = (0, 0, 0)

def randpos():
    return random.choice(list(range(0, 4)) + list(range(13, 17)))

player_col, player_row = randpos(), randpos()

pygame.init()
window = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("TheManIsSeekingForTruth")

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
    biome_images[biome_color] = pygame.transform.scale(image, (200, 200))
grid = [[random.choice(biome_colors) for _ in range(17)] for _ in range(17)]

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player_col > 0:
                player_col -= 1
            elif event.key == pygame.K_RIGHT and player_col < 16:
                player_col += 1
            elif event.key == pygame.K_UP and player_row > 0:
                player_row -= 1
            elif event.key == pygame.K_DOWN and player_row < 16:
                player_row += 1

    window.fill((234, 212, 252))
    for row in range(17):
        for col in range(17):
            cell_pos = (col * 30 + GRID_X, row * 30 + GRID_Y)
            biome_color = grid[row][col]
            if args.debug and (row, col) == (player_row, player_col):
                pygame.draw.rect(window, PLAYER_DEBUG_COLOR, (cell_pos[0], cell_pos[1], 30, 30))
            else:
                pygame.draw.rect(window, biome_color, (cell_pos[0], cell_pos[1], 30, 30))

    current_color = grid[player_row][player_col]
    current_image = biome_images[current_color]
    window.blit(current_image, (565, 20))
    pygame.display.update()
    clock.tick(60)
pygame.quit()
