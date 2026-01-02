#!/opt/homebrew/bin/python3

import random
import math
import pygame, sys
from pygame.locals import *

# Constants for the game window and board
WINDOW = 640  # Size of the game window in pixels
BOARD = 16    # Number of squares on the board (16x16)
SQUARE = 40   # Size of each square in pixels
FPS = 10      # Frames per second
fpsClock = pygame.time.Clock()

#             R    G    B
DARK      = (162, 209, 73 )
LIGHT     = (170, 215, 81 )
RED       = (231, 71 , 29 )
DARKBLUE  = (40 , 70 , 140)
LIGHTBLUE = (80 , 120, 200)
BLACK     = (0  , 0  , 0  )
WHITE     = (255, 255, 255)

# Initial direction of the snake
DIRECTION = "LEFT"

def main():
    """Main function for the game."""
    global DISPLAYSURF, DIRECTION
    pygame.init()

    # Font setup
    startFont = pygame.font.Font('PressStart2P-Regular.ttf', 30)
    nameFont = pygame.font.Font('Pixel Game.otf', 200)

    # Initialize the display surface
    DISPLAYSURF = pygame.display.set_mode((WINDOW, WINDOW))
    pygame.display.set_caption('snake')

    # Initial position of the snake
    x = 13
    y = 7

    # Variables for the floating text effect on the start screen
    floatTime = 0
    FLOAT_SPEED = 5
    FLOAT_AMPLITUDE = 10

    # Initial snake body
    snake = [(x - 3, y), (x - 2, y), (x - 1, y), (x, y)]
    # Place the first fruit
    fruitPos = placeFruit()

    # Text for the start screen
    startText = startFont.render("PRESS ENTER TO START", True, BLACK)
    startText_rect = startText.get_rect(center=(WINDOW // 2, WINDOW // 2))

    # Game title text
    nameText = nameFont.render("SNAKE", True, DARKBLUE)
    nameText_rect = nameText.get_rect(center=(WINDOW // 2, WINDOW // 4))

    # Score variables
    score = 0
    highScore = 0

    # Load sound effects and background music
    eatSound = pygame.mixer.Sound('little_robot_sound_factory_Collect_Point_01.mp3')
    eatSound.set_volume(0.3)
    deathSound = pygame.mixer.Sound('mixkit-retro-arcade-game-over-470.wav')
    deathSound.set_volume(0.3)
    pygame.mixer.music.load('flat-8-bit-gaming-music-instrumental-211547.mp3')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.3)

    # Load and scale the apple image
    apple = pygame.image.load("apple.png")
    apple = pygame.transform.scale(apple, (SQUARE, SQUARE))

    # Game state variables
    gameStarted = False
    died = False
    deadThisTurn = False
    blinkState = True
    blinkTimer = 0

    # Main game loop
    while True:
        delta_time = fpsClock.tick() / 1000
        if died:
            # Restart music after dying
            pygame.mixer.music.play(-1, 0.0)
            died = False

        # Update score and high score text
        scoreText = startFont.render("SCORE : " + str(score), True, BLACK)
        scoreText_rect = scoreText.get_rect(center=(WINDOW // 2, nameText_rect.center[1] + (SQUARE * 8)))

        highScoreText = startFont.render("HIGH SCORE : " + str(highScore), True, BLACK)
        highScoreText_rect = highScoreText.get_rect(center=(WINDOW // 2, scoreText_rect.center[1] + (SQUARE * 1)))

        # Event handling loop
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # Handle directional input
                if event.key == K_UP and gameStarted:
                    if DIRECTION != "DOWN":
                        DIRECTION = "UP"
                elif event.key == K_LEFT and gameStarted:
                    if DIRECTION != "RIGHT":
                        DIRECTION = "LEFT"
                elif event.key == K_DOWN and gameStarted:
                    if DIRECTION != "UP":
                        DIRECTION = "DOWN"
                elif event.key == K_RIGHT and gameStarted:
                    if DIRECTION != "LEFT":
                        DIRECTION = "RIGHT"
                # Start the game on ENTER press
                if event.key == K_RETURN:
                    gameStarted = True

            # Quit the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                quitSnake()
        
        # Display the start screen if the game hasn't started
        if not gameStarted:
            drawBoard()

            # Create floating effect for the title
            floatTime += FLOAT_SPEED * delta_time
            offsetY = int(math.sin(floatTime) * FLOAT_AMPLITUDE)

            floatingRect = nameText_rect.copy()
            floatingRect.y += offsetY
            
            # Create blinking effect for the "PRESS ENTER" text
            blinkTimer += delta_time
            if blinkTimer >= 0.07:
                blinkState = not blinkState
                blinkTimer = 0

            if blinkState:
                startText = startFont.render("PRESS ENTER TO START", True, BLACK)
                DISPLAYSURF.blit(startText, startText_rect)
            
            DISPLAYSURF.blit(nameText, floatingRect)
            DISPLAYSURF.blit(scoreText, scoreText_rect)
            DISPLAYSURF.blit(highScoreText, highScoreText_rect)
            pygame.display.update()
            continue
        else:
            # Game logic when the game is running
            setNewHead(snake)

            # Check for collision with the fruit
            if hasColided(snake, fruitPos):
                score += 1
                if score > highScore:
                    highScore += 1
                fruitPos = placeFruit()
                eatSound.play()
            else:
                # Remove the last segment of the snake if no fruit is eaten
                snake.pop()
            
            # Check for collision with the snake's own body
            for i in snake[1:]:
                if i == snake[0]:
                    gameOver(snake, x, y, deathSound)
                    died = True
                    deadThisTurn = True
                    score = 0
                    break

            # Check for collision with the walls
            if (snake[0][0] < 0 or
                snake[0][1] < 0 or
                snake[0][0] >= BOARD or
                snake[0][1] >= BOARD
            ):
                gameOver(snake, x, y, deathSound)
                died = True
                deadThisTurn = True
                score = 0
                continue
                
            # Handle the transition after death
            if deadThisTurn:
                deadThisTurn = False
                gameStarted = False
                drawBoard()
                DISPLAYSURF.blit(startText, startText_rect)
                DISPLAYSURF.blit(nameText, nameText_rect)
                pygame.display.update()
                continue

            # Draw the game elements
            drawBoard()
            drawFruit(fruitPos[0], fruitPos[1], apple)
            drawSnake(snake)

        # Update the display
        pygame.display.update()
        fpsClock.tick(FPS)

def quitSnake():
    """Quits Pygame and exits the program."""
    pygame.quit()
    sys.exit()

def gameOver(snake, x, y, sound):
    """Handles the game over state."""
    global DIRECTION, gameStarted
    pygame.mixer.music.stop()
    sound.play()
    playDeathAnimation()
    # Reset the snake to its initial state
    snake.clear()
    snake.extend([(x - 3, y), (x - 2, y), (x - 1, y), (x, y)])
    DIRECTION = "LEFT"
    gameStarted = False

def playDeathAnimation():
    """Plays a death animation by turning the screen white, square by square."""
    remainingSquares = BOARD * BOARD 
    while remainingSquares != 0:
        x = random.randrange(0, BOARD)
        y = random.randrange(0, BOARD)
        color = DISPLAYSURF.get_at((x * SQUARE, y * SQUARE))

        if color != WHITE:
            pygame.draw.rect(DISPLAYSURF, WHITE, (x * SQUARE, y * SQUARE, SQUARE, SQUARE))
            pygame.display.update()
            pygame.time.wait(5)
            remainingSquares -= 1

def placeFruit():
    """Places a fruit on a random square that is not occupied by the snake."""
    fruitx = random.randrange(0, BOARD)
    fruity = random.randrange(0, BOARD)
    color = DISPLAYSURF.get_at((fruitx * SQUARE, fruity * SQUARE))
    # Ensure the fruit doesn't spawn on the snake
    if color == DARKBLUE or color == LIGHTBLUE:
        return placeFruit()
    else:
        return (fruitx, fruity)

def drawFruit(fruitx, fruity, image):
    """Draws the fruit on the board."""
    DISPLAYSURF.blit(image, (fruitx * SQUARE, fruity * SQUARE))

def hasColided(snake, fruitPos):
    """Checks if the snake's head has collided with the fruit."""
    if not snake:
        return False
    return snake[0] == fruitPos

def drawSnake(snake):    
    """Draws the snake on the board."""
    for (i, j) in snake:
        if (i, j) == snake[0]:
            # Draw the head with a different color
            pygame.draw.rect(DISPLAYSURF, LIGHTBLUE, (i * SQUARE, j * SQUARE, SQUARE, SQUARE))
        else:
            # Draw the body
            pygame.draw.rect(DISPLAYSURF, DARKBLUE, (i * SQUARE, j * SQUARE, SQUARE, SQUARE))

def setNewHead(snake):
    """Moves the snake by adding a new head in the current direction."""
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
    """Draws the checkered game board."""
    presentColor = DARK
    y = 0

    for i in range(BOARD):
        x = 0
        for j in range(BOARD):
            pygame.draw.rect(DISPLAYSURF, presentColor, (x, y, SQUARE, SQUARE))
            # Alternate colors for the checkered pattern
            presentColor = LIGHT if presentColor == DARK else DARK
            x += SQUARE
        # Alternate colors for the next row
        presentColor = LIGHT if presentColor == DARK else DARK
        y += SQUARE    

if __name__ == '__main__':
    # Entry point of the program
    main()
