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
RED       = (231, 71,  29)
DARKBLUE  = (40,  70,  140)
LIGHTBLUE = (80,  120, 200)
BLACK     = (0,   0,   0)
DIRECTION = "LEFT"

def main():
    global DISPLAYSURF, DIRECTION
    pygame.init()
    startFont = pygame.font.Font('PressStart2P-Regular.ttf', 30)
    nameFont = pygame.font.Font('Pixel Game.otf', 200)
    DISPLAYSURF = pygame.display.set_mode((WINDOW, WINDOW))
    pygame.display.set_caption('snake')
    x = 10
    y = 7

    snake = [(x - 3, y), (x - 2, y), (x - 1, y), (x, y)]
    fruitPos = placeFruit()

    startText = startFont.render("PRESS ENTER TO START", True, BLACK)
    startText_rect = startText.get_rect(center=(WINDOW // 2, WINDOW // 2))

    nameText = nameFont.render("SNAKE", True, DARKBLUE)
    nameText_rect = nameText.get_rect(center=(WINDOW // 2, WINDOW // 4))

    eatSound = pygame.mixer.Sound('little_robot_sound_factory_Collect_Point_01.mp3')
    eatSound.set_volume(0.3)
    pygame.mixer.music.load('flat-8-bit-gaming-music-instrumental-211547.mp3')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.3)

    gameStarted = False
    while True:
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    if DIRECTION == "DOWN":
                        continue
                    else:
                        DIRECTION = "UP"
                elif event.key == K_LEFT:
                    if DIRECTION == "RIGHT":
                        continue
                    else:
                        DIRECTION = "LEFT"
                elif event.key == K_DOWN:
                    if DIRECTION == "UP":
                        continue
                    else:
                        DIRECTION = "DOWN"
                elif event.key == K_RIGHT:
                    if DIRECTION == "LEFT":
                        continue
                    else:
                        DIRECTION = "RIGHT"
                if event.key == K_RETURN:
                    gameStarted = True

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                quitSnake()
        
        if not gameStarted:
            drawBoard()
            DISPLAYSURF.blit(startText, startText_rect)
            DISPLAYSURF.blit(nameText, nameText_rect)

        else:
            setNewHead(snake)
            if hasColided(snake, fruitPos):
                fruitPos = placeFruit()
                eatSound.play()
            elif snake:
                snake.pop()
            
            for i in snake[1:]:
                if i == snake[0]:
                    quitSnake()
                    
            if (snake[0][0] < 0 or
                snake[0][1] < 0 or
                snake[0][0] >= BOARD or
                snake[0][1] >= BOARD
            ):
                quitSnake()

            drawBoard()
            drawFruit(fruitPos[0], fruitPos[1])
            drawSnake(snake)

        pygame.display.update()
        fpsClock.tick(FPS)

def quitSnake():
    pygame.quit()
    sys.exit()

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
