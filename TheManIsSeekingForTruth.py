import pygame
import random
pygame.init()
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("TheManIsSeekingForTruth")
CELL_SIZE = 30
GRID_SIZE = 16
player_x, player_y = 8, 8
color_to_sprite = {
    (255, 255, 0): "desert.jpg",
    (0, 100, 0): "taiga.jpg",
    (0, 0, 255): "ocean.jpg",
    (128, 128, 128): "mountains.jpg",
    (0, 128, 0): "forest.jpg",
    (165, 42, 42): "steppe.jpg",
    (128, 0, 128): "mushroom_plain.jpg"
}
color_palette = list(color_to_sprite.keys())
sprites = {}
for color, sprite_file in color_to_sprite.items():
    sprite = pygame.image.load(sprite_file)
    sprites[color] = pygame.transform.scale(sprite, (CELL_SIZE, CELL_SIZE))
colors = [[random.choice(color_palette) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player_x > 0:
                player_x -= 1
            elif event.key == pygame.K_RIGHT and player_x < GRID_SIZE - 1:
                player_x += 1
            elif event.key == pygame.K_UP and player_y > 0:
                player_y -= 1
            elif event.key == pygame.K_DOWN and player_y < GRID_SIZE - 1:
                player_y += 1
    window.fill((234, 212, 252))
    start_x = 20
    start_y = (600 - GRID_SIZE * CELL_SIZE) // 2
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect_pos = (start_x + x * CELL_SIZE, start_y + y * CELL_SIZE)
            color = colors[y][x]
            if x == player_x and y == player_y:
                pygame.draw.rect(window, (255, 255, 0), (*rect_pos, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(window, color, (*rect_pos, CELL_SIZE, CELL_SIZE))
    current_color = colors[player_y][player_x]
    current_sprite = sprites[current_color]
    window.blit(current_sprite, (660, 70))
    pygame.draw.rect(window, (50, 50, 80), (650, 50, 120, 180))
    pygame.draw.rect(window, (200, 200, 200), (650, 50, 120, 180), 2)
    pygame.display.update()
    clock.tick(60)
pygame.quit()
