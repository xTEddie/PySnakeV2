import pygame
import time
import random

## images
IMG_SNAKE = pygame.image.load("SnakeHead.png")
IMG_APPLE = pygame.image.load("Apple.png")
ICON = pygame.image.load("logo.png")

## colors
WHITE = (255,255,255)
BLACK= (0,0,0)
RED = (255,0,0)
GREEN = (0,100,0)
BLUE = (0,0,255)

## variables
NAME = "PySnake"
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
FPS = 15
BLOCK_SIZE = 20
APPLE_SIZE = 30
direction = "right"
lastDirection = direction

pygame.init()
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
pygame.display.set_icon(ICON)
pygame.display.set_caption(NAME)

## object to control framerate
clock = pygame.time.Clock() 

## fonts
SMALL_FONT = pygame.font.SysFont("comicsansms", 25, True) 
MEDIUM_FONT = pygame.font.SysFont("comicsansms", 50, True) 
LARGE_FONT = pygame.font.SysFont("comicsansms", 80, True)

def getTextSurface(text,color,size):
    ## draw text on a new Surface
    if size == "small":
        textSurface = SMALL_FONT.render(text, True, color) 
    elif size == "medium":
        textSurface = MEDIUM_FONT.render(text, True, color)
    elif size == "large":
        textSurface = LARGE_FONT.render(text, True, color)
    return textSurface,textSurface.get_rect()
    
def blitText(msg,color,x_displace=0,y_displace=0,size="small"):
    ## draw surface on another surface
    textSurf, textRect = getTextSurface(msg,color,size)
    textRect.center = (DISPLAY_WIDTH/2) + x_displace, (DISPLAY_HEIGHT/2) + y_displace
    gameDisplay.blit(textSurf, textRect) 

def generateApple():
    applePositionX = round(random.randrange(0, DISPLAY_WIDTH - APPLE_SIZE))
    applePositionY = round(random.randrange(0, DISPLAY_HEIGHT - APPLE_SIZE))
    return applePositionX, applePositionY

def drawSnake(block_size, snakeList):
    ## rotate snake head according to direction variable
    if direction == "right":
        snakeHead = pygame.transform.rotate(IMG_SNAKE, 270)
    elif direction == "left":
        snakeHead = pygame.transform.rotate(IMG_SNAKE, 90)
    elif direction == "up":
        snakeHead = IMG_SNAKE
    elif direction == "down":
        snakeHead = pygame.transform.rotate(IMG_SNAKE, 180)

    ## draw head of snake    
    gameDisplay.blit(snakeHead, (snakeList[-1][0], snakeList[-1][1]))
    for coordinate in snakeList[:-1]: ## exclude last element 
        ## draw rectangle [x,y,w,h]
        pygame.draw.rect(gameDisplay, GREEN, [coordinate[0],coordinate[1],block_size,block_size])

def updateScore(score):
    text = SMALL_FONT.render("Score: "+str(score), True, WHITE)
    gameDisplay.blit(text, [0,0])

def pauseGame():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
##        gameDisplay.fill(WHITE)
        blitText("Pause", WHITE, y_displace=-100,size="large")
        blitText("Press C to continue or Q to quit", WHITE, 25)
        pygame.display.update()
        clock.tick(5) ## change FPS
    
def startScreen():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if quit button is pressed
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                    runGame()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_r:
                    showRule()
                        
        gameDisplay.fill(BLACK)
        blitText("PySnake", GREEN, y_displace=-100, size="large")
        blitText("by Edward Tran", WHITE, y_displace=0, x_displace=200, size="medium")
        blitText("Press C to play, R for rules, P to pause or Q to quit", WHITE, y_displace=180)
        pygame.display.update()
        clock.tick(15) ## change FPS

def showRule():
    inRule = True

    while inRule:
         for event in pygame.event.get():
            if event.type == pygame.QUIT: #if quit button is pressed
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    inRule = False
                    startScreen()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
         gameDisplay.fill(BLACK)
         blitText("HOW TO PLAY", RED, y_displace=-100, size="medium")
         blitText("The objective of the game is to eat red apples", WHITE, y_displace=-30)
         blitText("The more apples you eat, the longer you get", WHITE, y_displace=10)
         blitText("If you run into yourself, or the edges, you die!", WHITE, y_displace=50)
         blitText("Press B to go back or Q to quit", WHITE, y_displace=180)
         pygame.display.update()
         clock.tick(15)
         
def runGame():
    
    global direction ## to update direction
    global lastDirection
    gameExit = False
    gameOver = False

    ## x and y position of the snake head
    headPositionX = DISPLAY_WIDTH/2
    headPositionY = DISPLAY_HEIGHT/2

    headPositionXChange = BLOCK_SIZE
    headPositionYChange = 0

    snakeList = []
    snakeLength = 1

    applePositionX, applePositionY = generateApple()

    while not gameExit:
        
        while gameOver == True:
            gameDisplay.fill(BLACK)
            blitText("Game Over", RED, y_displace=-50, size="large")
            blitText("Press C to play again or Q to quit", WHITE, y_displace=50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: #if quit button is pressed
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_c:
                        direction = "right" 
                        runGame()
            
        for event in pygame.event.get(): ## loop through list of events
            if event.type == pygame.QUIT: ## if quit button is pressed
                gameExit = True
            if event.type == pygame.KEYDOWN:
                ## making sure snake can only move forward and not backward
                if event.key == pygame.K_LEFT and direction != "right":
                    headPositionXChange = -BLOCK_SIZE
                    headPositionYChange = 0
                    lastDirection = direction
                    direction = "left"
                elif event.key == pygame.K_RIGHT and direction != "left":
                    headPositionXChange = BLOCK_SIZE
                    headPositionYChange = 0
                    lastDirection = direction
                    direction = "right"
                elif event.key == pygame.K_UP and direction != "down":
                    headPositionYChange = -BLOCK_SIZE
                    headPositionXChange = 0
                    lastDirection = direction
                    direction = "up"
                elif event.key == pygame.K_DOWN and direction != "up":
                    headPositionYChange = BLOCK_SIZE
                    headPositionXChange = 0
                    lastDirection = direction
                    direction = "down"
                elif event.key == pygame.K_p:
                    pauseGame()
                            
        headPositionX += headPositionXChange
        headPositionY += headPositionYChange

        ## game over if snake goes outside screen size
        if headPositionX >= DISPLAY_WIDTH or  headPositionX < 0 or headPositionY >= DISPLAY_HEIGHT or headPositionY < 0:
            gameOver = True

        ## fix snake and apple overlapping 
        if headPositionX > applePositionX and headPositionX < applePositionX + APPLE_SIZE or headPositionX + BLOCK_SIZE > applePositionX and headPositionX + BLOCK_SIZE < applePositionX + APPLE_SIZE:
            if headPositionY > applePositionY and headPositionY < applePositionY + APPLE_SIZE or headPositionY + BLOCK_SIZE > applePositionY and headPositionY + BLOCK_SIZE < applePositionY + APPLE_SIZE:
                applePositionX, applePositionY = generateApple()
                snakeLength += 1

        gameDisplay.fill(BLACK) ## change background color
##        pygame.draw.rect(gameDisplay, RED, [applePositionX, applePositionY, APPLE_SIZE, APPLE_SIZE])
        gameDisplay.blit(IMG_APPLE, (applePositionX, applePositionY))
   
        snakeHead = []
        ## get head coordinate  
        snakeHead.append(headPositionX)
        snakeHead.append(headPositionY)
        ## append coordinate in list
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength: ## if there is more blocks allowed in snake, fix list 
            del snakeList[0]
        for eachSegment in snakeList[:-1]: ## if snake eats itself
            if eachSegment == snakeHead:
                ## making sure eating its head does not end the game
                if direction == "left" and lastDirection != "right" or direction == "right" and lastDirection != "left" or direction == "up" and lastDirection != "down" or direction == "down" and lastDirection != "up":
                    gameOver = True
                
        drawSnake(BLOCK_SIZE, snakeList) 
        updateScore(snakeLength-1) ## score is snake length - 1
        pygame.display.update() ## update change
        clock.tick(FPS) 

    pygame.quit()
    quit()
    
startScreen()
