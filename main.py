import pygame
from settings import *
from pygame import Vector2
from random import randrange
from writer import Writer
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
x, y = NUMCOLS // 2, NUMROWS// 2
# snake = [Vector2(x, y), Vector2(x, y + 1), Vector2(x, y + 2),
#          Vector2(x, y + 3), Vector2(x, y + 4), Vector2(x, y + 5)]
snake = [Vector2(x, y), Vector2(x, y + 1)]
directions = (Vector2(0, -1), Vector2(1, 0), Vector2(0, 1), Vector2(-1, 0))
velocity = directions[0]
moves = []
time = 0
waitTime = 150
turnedThisUpdate = False
walls = []
alive = True
paused = False
for i in range(NUMCOLS):
    walls.append((i, 0))
    walls.append((i, NUMROWS - 1))
for i in range(NUMROWS):
    walls.append((0, i))
    walls.append((NUMCOLS - 1, i))
""" Level 2"""
for i in range(7):
    walls.append((22, 7 + i))
    walls.append((22, 16 + i))
    walls.append((7, 7 + i))
    walls.append((7, 16 + i))

writer = Writer(screen, size = 30, color= SILVER)
    
applesMade = 0
while applesMade < 1:
    row = randrange(0, NUMROWS)
    col = randrange(0, NUMCOLS)
    if (row, col) not in walls:
        apple = (row, col)
        applesMade += 1
def update(dt):
    global time, turnedThisUpdate
    time += dt
    if time > waitTime and alive == True and paused == False:
        time = 0
        #turnedThisUpdate = False
        updateSnake()
def updateSnake():
    global alive, waitTime, velocity
    for i in range(len(snake) - 1, 0, -1):
        snake[i].x = snake[i - 1].x
        snake[i].y = snake[i - 1].y
    currentDirection = directions.index(velocity)
    if len(moves) > 0:
        move = moves.pop(0)
    else:
        move = None
    if move == 'left':
        currentDirection -= 1
        currentDirection %= len(directions)
    elif move == 'right':
        currentDirection += 1
        currentDirection %= len(directions)
    velocity = directions[currentDirection]
    snake[0] += velocity
    loc = (int(snake[0].x), int(snake[0].y))
    if loc == apple:
        makeNewApple()
        waitTime -= 1
        snake.append(Vector2(-1, -1))
    elif snake[0] in snake[1 :] or loc in walls:
        alive = False
    
def makeNewApple():
    global applesMade, apple
    newCount = applesMade + 1
    while applesMade < newCount:
        row = randrange(0, NUMROWS)
        col = randrange(0, NUMCOLS)
        if (row, col) not in walls and Vector2(row, col) not in snake:
            apple = (row, col)
            applesMade += 1
            
def draw():
    screen.fill(BGCOLOR)
    drawSnake()
    drawWalls()
    drawApple()
    if alive == False:
        drawScore()
    pygame.display.update()

def drawScore():
    writer.setText(str(len(snake) - 2) + ' apples eaten.')
    writer.writeText(WIDTH // 2 - 80, HEIGHT // 2)
    writer.setText('Play again? Y/N')
    writer.writeText(WIDTH // 2 - 81, HEIGHT // 2 + 80)
def drawSnake():
    segment = snake[0]
    pygame.draw.rect(screen, DARKGREEN, (segment.x * TILESIZE, segment.y * TILESIZE, TILESIZE, TILESIZE))
    pygame.draw.rect(screen, BLACK, (segment.x * TILESIZE, segment.y * TILESIZE, TILESIZE, TILESIZE), width = 1)    
    for segment in snake[1:]:
        pygame.draw.rect(screen, GREEN, (segment.x * TILESIZE, segment.y * TILESIZE, TILESIZE, TILESIZE))
        pygame.draw.rect(screen, BLACK, (segment.x * TILESIZE, segment.y * TILESIZE, TILESIZE, TILESIZE), width = 1)

def drawWalls():
    for wall in walls:
        pygame.draw.rect(screen, ORANGE, (wall[0] * TILESIZE, wall[1] * TILESIZE, TILESIZE, TILESIZE))
        pygame.draw.rect(screen, BLACK, (wall[0] * TILESIZE, wall[1] * TILESIZE, TILESIZE, TILESIZE), width = 1)

def drawApple():
    pygame.draw.rect(screen, RED, (apple[0] * TILESIZE, apple[1] * TILESIZE, TILESIZE, TILESIZE))
    pygame.draw.rect(screen, BLACK, (apple[0] * TILESIZE, apple[1]* TILESIZE, TILESIZE, TILESIZE), width = 1)

def resetGame():
    global snake, alive, velocity, waitTime
    x, y = NUMCOLS // 2, NUMROWS// 2
    snake = [Vector2(x, y), Vector2(x, y + 1)]
    velocity = directions[0]
    alive = True
    waitTime = 150
    
def onMousePress(x, y):
    pass

def onMouseMove(x, y):
    pass

def onMouseRelease(x, y):
    pass

def onKeyPress(key):
    global velocity, turnedThisUpdate, paused
    """
    if key == pygame.K_UP:
        velocity = directions[0]
    if key == pygame.K_RIGHT:
        velocity = directions[1]
    if key == pygame.K_DOWN:
        velocity = directions[2]
    if key == pygame.K_LEFT:
        velocity = directions[3]
    """
    """
    if turnedThisUpdate == False:
        currentDirection = directions.index(velocity)
        if key == pygame.K_LEFT:
            currentDirection -= 1
            currentDirection %= len(directions)
        elif key == pygame.K_RIGHT:
            currentDirection += 1
            currentDirection %= len(directions)
        velocity = directions[currentDirection]
        turnedThisUpdate = True
    """
    if key == pygame.K_LEFT:
        moves.append('left')
    elif key == pygame.K_RIGHT:
        moves.append('right')
    if key == pygame.K_p:
        paused = not paused
    if alive == False and key == pygame.K_n:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    elif alive == False and key == pygame.K_y:
        resetGame()
        
def onKeyRelease(key):
    pass
    

def mainloop():
    running = True
    clock = pygame.time.Clock()
    while running:
        update(clock.tick(FPS))
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEMOTION:
                onMouseMove(event.pos[0], event.pos[1])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                onMousePress(event.pos[0], event.pos[1])
            elif event.type == pygame.MOUSEBUTTONUP:
                onMouseRelease(event.pos[0], event.pos[1])
            elif event.type == pygame.KEYDOWN:
                onKeyPress(event.key)
            elif event.type == pygame.KEYUP:
                onKeyRelease(event.key)
        


pygame.init()
mainloop()
