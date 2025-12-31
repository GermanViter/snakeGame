#!/opt/homebrew/bin/python3

import random
import pygame, sys
from pygame.locals import *


WINDOW = 640
BOARD = 16
SQUARE = 40
FPS = 10
fpsClock = pygame.time.Clock()

#             R    G    B
DARK      = (162, 209, 73)
LIGHT     = (170, 215, 81)
RED       = (231, 71, 29)
DARKBLUE  = (40, 70, 140)
LIGHTBLUE = (80, 120, 200)

DIRECTION = "RIGHT"

def main():
    global DISPLAYSURF, DIRECTION
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOW, WINDOW))
    pygame.display.set_caption('snake')
    x = 6
    y = 7

    snake = [(x - 3, y), (x - 2, y), (x - 1, y), (x, y)]

    drawBoard()
    placeFruit()
    drawSnake(snake)

    gameStarted = False
    while True:
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    DIRECTION = "UP"
                elif event.key == K_LEFT:
                    DIRECTION = "LEFT"
                elif event.key == K_DOWN:
                    DIRECTION = "DOWN"
                elif event.key == K_RIGHT:
                    DIRECTION = "RIGHT"
                elif event.key == K_SPACE:
                    gameStarted = True
                    print("ENTER PRESSÉ")

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        if gameStarted:
            setNewHead(snake)
            snake.pop()
        

        drawBoard()
        drawSnake(snake)

        pygame.display.update()
        fpsClock.tick(FPS)

def placeFruit():
    fruitx = random.randrange(0, WINDOW, SQUARE)
    fruity = random.randrange(0, WINDOW, SQUARE)
    color = DISPLAYSURF.get_at((fruitx, fruity))
    
    if color == DARKBLUE:
        return placeFruit()
    else:
        pygame.draw.ellipse(DISPLAYSURF, RED, (fruitx, fruity, SQUARE, SQUARE))


def drawSnake(snake):    
    for (i, j) in snake:
        pygame.draw.rect(DISPLAYSURF, DARKBLUE, (i * SQUARE, j * SQUARE, SQUARE, SQUARE))


def setNewHead(snake):
    headX, headY = snake[0]
    if DIRECTION == "RIGHT":
        new_head = (headX + 1, headY)
    elif DIRECTION == "LEFT":
        new_head = (headX - 1, headY)
    elif DIRECTION == "UP":
        new_head = (headX, headY - 1)
    elif DIRECTION == "DOWN":
        new_head = (headX, headY + 1)

    snake.insert(0, new_head)

def drawBoard():
    presentColor = DARK
    y = 0

    for i in range(BOARD):
        x = 0
        for j in range(BOARD):
            pygame.draw.rect(DISPLAYSURF, presentColor, (x, y, SQUARE, SQUARE))
            presentColor = LIGHT if presentColor == DARK else DARK
            x += SQUARE
        presentColor = LIGHT if presentColor == DARK else DARK
        y += SQUARE    

if __name__ == '__main__':
    main()
