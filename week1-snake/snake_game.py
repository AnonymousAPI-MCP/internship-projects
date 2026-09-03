import random
import sys

import pygame
import tkinter as tk
from tkinter import messagebox


class Cube:
    rows = 20
    width = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (
            (self.pos[0] + self.dirnx) % self.rows,
            (self.pos[1] + self.dirny) % self.rows,
        )

    def draw(self, surface, eyes=False):
        dis = self.width // self.rows
        i, j = self.pos
        x = i * dis
        y = j * dis

        pygame.draw.rect(surface, self.color, (x + 1, y + 1, dis - 2, dis - 2))

        if eyes:
            centre = dis // 2
            radius = 3
            circle_a = (x + centre - radius - 4, y + 8)
            circle_b = (x + dis - radius * 2 - 4, y + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_a, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_b, radius)


class Snake:
    def __init__(self, color, pos):
        self.color = color
        self.dirnx = 1
        self.dirny = 0
        self.head = Cube(pos, self.dirnx, self.dirny)
        self.body = [self.head]
        self.turns = {}

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.dirnx != 1:
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos] = [self.dirnx, self.dirny]
        elif keys[pygame.K_RIGHT] and self.dirnx != -1:
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos] = [self.dirnx, self.dirny]
        elif keys[pygame.K_UP] and self.dirny != 1:
            self.dirny = -1
            self.dirnx = 0
            self.turns[self.head.pos] = [self.dirnx, self.dirny]
        elif keys[pygame.K_DOWN] and self.dirny != -1:
            self.dirny = 1
            self.dirnx = 0
            self.turns[self.head.pos] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.dirnx = 1
        self.dirny = 0
        self.head = Cube(pos, self.dirnx, self.dirny)
        self.body = [self.head]
        self.turns = {}

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            new_pos = (tail.pos[0] - 1, tail.pos[1])
        elif dx == -1 and dy == 0:
            new_pos = (tail.pos[0] + 1, tail.pos[1])
        elif dx == 0 and dy == 1:
            new_pos = (tail.pos[0], tail.pos[1] - 1)
        else:
            new_pos = (tail.pos[0], tail.pos[1] + 1)

        self.body.append(Cube(new_pos, dx, dy))

    def draw(self, surface):
        for i, c in enumerate(self.body):
            c.draw(surface, eyes=(i == 0))

    def hit_self(self):
        head_pos = self.body[0].pos
        return head_pos in [c.pos for c in self.body[1:]]


def drawGrid(w, rows, surface):
    size_between = w // rows
    x = 0
    y = 0
    for _ in range(rows):
        x += size_between
        y += size_between
        pygame.draw.line(surface, (64, 64, 64), (x, 0), (x, w))
        pygame.draw.line(surface, (64, 64, 64), (0, y), (w, y))


def redrawWindow(surface, snake_obj, snack, rows, width):
    surface.fill((0, 0, 0))
    snake_obj.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(rows, snake_obj):
    occupied = [c.pos for c in snake_obj.body]

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if (x, y) not in occupied:
            return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except tk.TclError:
        pass


def main():
    width = 500
    height = 500
    rows = 20

    Cube.rows = rows
    Cube.width = width

    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake")

    s = Snake((255, 0, 0), (10, 10))
    snack = Cube(randomSnack(rows, s), color=(0, 255, 0))

    clock = pygame.time.Clock()
    flag = True

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()

        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = Cube(randomSnack(rows, s), color=(0, 255, 0))

        if s.hit_self():
            print("Score:", len(s.body))
            message_box("You Lost!", f"Final score: {len(s.body)}. Play again...")
            s.reset((10, 10))

        redrawWindow(win, s, snack, rows, width)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main()