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



def main():
    global DISPLAYSURF
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOW, WINDOW))
    pygame.display.set_caption('snake')

    snakeX = 6
    snakeY = 7

    drawBoard()
    placeFruit()
    drawSnake(snakeX, snakeY)
    
    gameStarted = False
    while True:
        if gameStarted:
            drawBoard()
            snakeX += 1
            drawSnake(snakeX, snakeY)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    gameStarted = True

            if event.type == QUIT:
               pygame.quit()
               sys.exit()
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


def drawSnake(x, y):
    #pygame.draw.rect(DISPLAYSURF, DARKBLUE, (x, y, SQUARE * 4, SQUARE))
    snake = [(x, y), (x + 1, y), (x + 2, y), (x + 3, y)]

    for i in range(BOARD):
        for j in range(BOARD):
            if (i, j) in snake:
                pygame.draw.rect(DISPLAYSURF, DARKBLUE, (i * SQUARE, j * SQUARE, SQUARE, SQUARE))

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
