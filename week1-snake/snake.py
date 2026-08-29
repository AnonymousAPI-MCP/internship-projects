import pygame
import random

pygame.init()

WIDTH =600
HEIGHT =400
screen =pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

BLACK =(0, 0, 0)
GREEN =(0,255,0)
RED =(255,0,0)
WHITE =(255,255,255)

BLOCK =20
clock = pygame.time.Clock()

snake = [[100,100]]
snake_dir =[BLOCK, 0]

food = [random.randrange(0, WIDTH, BLOCK) , random.randrange(0, HEIGHT, BLOCK)]
score = 0 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake_dir = [0, -BLOCK]
            if event.key == pygame.K_DOWN:
                snake_dir = [0, BLOCK]
            if event.key == pygame.K_LEFT:
                snake_dir = [-BLOCK, 0]
            if event.key == pygame.K_RIGHT:
                snake_dir = [BLOCK, 0]

    new_head = [snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1]]
    snake.insert(0, new_head)

    if new_head == food:
        food = [random.randrange(0, WIDTH, BLOCK), random.randrange(0, HEIGHT, BLOCK)]
        score += 1
    else:
        snake.pop()

    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        running = False

    if new_head in snake[1:]:
        running = False

    screen.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK, BLOCK))
    pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK, BLOCK))

    pygame.display.update()
    clock.tick(10)

pygame.quit()