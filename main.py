import pygame
from settings import *
from pygame import Vector2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
x, y = NUMCOLS // 2, NUMROWS// 2
snake = [Vector2(x, y), Vector2(x, y + 1), Vector2(x, y + 2),
         Vector2(x, y + 3), Vector2(x, y + 4), Vector2(x, y + 5)]
velocity = Vector2(0, -1)
time = 0
waitTime = 300
def update(dt):
    global time
    time += dt
    if time > waitTime:
        time = 0
        updateSnake()
def updateSnake():
    for i in range(len(snake) - 1, 0, -1):
        snake[i].x = snake[i - 1].x
        snake[i].y = snake[i - 1].y
    snake[0] += velocity

    

def draw():
    screen.fill(BGCOLOR)
    drawSnake()
    pygame.display.update()

def drawSnake():
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment.x * TILESIZE, segment.y * TILESIZE, TILESIZE, TILESIZE))

def onMousePress(x, y):
    pass

def onMouseMove(x, y):
    pass

def onMouseRelease(x, y):
    pass

def onKeyPress(key):
    pass

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
