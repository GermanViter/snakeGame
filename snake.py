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
    fruitPos = placeFruit()
    drawFruit(fruitPos[0], fruitPos[1])
    drawBoard()
    drawSnake(snake)

    pygame.mixer.music.load('music.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.3)

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
                elif event.key == K_RETURN:
                    gameStarted = True

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        if gameStarted:
            setNewHead(snake)          # ajouter la tête
            if hasColided(snake, fruitPos):  # collision avec fruit
                fruitPos = placeFruit()      # générer un nouveau fruit
            elif snake:                     # si snake non vide, supprimer la queue
                snake.pop()

        drawBoard()
        drawFruit(fruitPos[0], fruitPos[1])
        drawSnake(snake)

        pygame.display.update()
        fpsClock.tick(FPS)

def placeFruit():
    fruitx = random.randrange(0, BOARD)
    fruity = random.randrange(0, BOARD)
    color = DISPLAYSURF.get_at((fruitx * SQUARE, fruity * SQUARE))
    
    if color == DARKBLUE:
        return placeFruit()
    else:
        return (fruitx, fruity)

def drawFruit(fruitx, fruity):
    pygame.draw.ellipse(DISPLAYSURF, RED, (fruitx * SQUARE, fruity * SQUARE, SQUARE, SQUARE))

def hasColided(snake, fruitPos):
    if not snake:
        return False
    return snake[0] == fruitPos

def drawSnake(snake):    
    for (i, j) in snake:
        if (i, j) == snake[0]:
            pygame.draw.rect(DISPLAYSURF, LIGHTBLUE, (i * SQUARE, j * SQUARE, SQUARE, SQUARE))
        else:
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
