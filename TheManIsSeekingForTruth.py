import pygame
import random
pygame.init()
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("TheManIsSeekingForTruth")
CELL_SIZE = 30
GRID_SIZE = 16
player_x, player_y = 8, 8
colors = [[(random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
          for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
clock = pygame.time.Clock()
img = pygame.image.load('icon.gif')
pygame.display.set_icon(img)
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
            rect = pygame.Rect(start_x + x * CELL_SIZE, start_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if x == player_x and y == player_y:
                pygame.draw.rect(window, (255, 255, 0), rect)
            else:
                pygame.draw.rect(window, colors[y][x], rect)
    pygame.draw.rect(window, (50, 50, 80), (650, 50, 120, 180))
    pygame.draw.rect(window, (200, 200, 200), (650, 50, 120, 180), 2)
    pygame.draw.rect(window, colors[player_y][player_x], (660, 70, 100, 100))
    pygame.display.update()
    clock.tick(60)
pygame.quit()
