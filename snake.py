#!/opt/homebrew/bin/python3

import random
import pygame, sys
from pygame.locals import *


WINDOW = 640
BOARD = 16
SQUARE = 40
FPS = 30

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
    
    drawBoard()
    placeFruit()
    drawSnake()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
               pygame.quit()
               sys.exit()
        pygame.display.update() 


def placeFruit():
    fruitx = random.randrange(0, WINDOW, SQUARE)
    fruity = random.randrange(0, WINDOW, SQUARE)
    color = DISPLAYSURF.get_at((fruitx, fruity))
    
    if color == DARKBLUE:
        return placeFruit()
    else:
        pygame.draw.ellipse(DISPLAYSURF, RED, (fruitx, fruity, SQUARE, SQUARE))

def getSquareX():
    posX = 6
   
    squareX = SQUARE * posX
    
    return squareX

def getSquareY():
    posY = 7
    squareY = SQUARE * posY

    return squareY

def drawSnake():
    pygame.draw.rect(DISPLAYSURF, DARKBLUE, (getSquareX() ,getSquareY(), SQUARE * 4, SQUARE))

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
