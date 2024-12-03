import pygame
import random


WIDTH = 612
HEIGHT = 612
FPS = 30

blockSize = int((WIDTH-(WIDTH/5))/8) #Set the size of the grid block

# Block sprites
grass = pygame.transform.scale(pygame.image.load("assets/grass.png"),(blockSize,blockSize))
player = pygame.transform.scale(pygame.image.load("assets/player.png"),(blockSize,blockSize))
heart = pygame.transform.scale(pygame.image.load("assets/heart.png"),(blockSize,blockSize))

playerPos = [4,4]
health = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 200)

## Initialize
pygame.init()
pygame.mixer.init()  
game = pygame.Surface((612,612))
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption("Islebound")
clock = pygame.time.Clock()

def healthUpdater(health):
    for x in range(health):
        game.blit(heart,(x*blockSize+15,5))

# utility stuff !!
def clamp(x,min,max):
    if min <= x <= max:
        return x
    elif min >= x:
        return min
    elif max <= x:
        return max
def min(a,b):
    if a>b:
        return b
    else:
        return a


def drawBase():
    pygame.draw.rect(game,BLUE,pygame.Rect(0, 0, WIDTH, HEIGHT))
    for x in range(50, int(612-612/5), blockSize):
        for y in range(50, int(612-612/5), blockSize):
            game.blit(grass,(x,y+25))

# Game loop
running = True
while running:

    clock.tick(FPS)     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_LEFT:
                    playerPos[0] -= 1
                case pygame.K_RIGHT:
                    playerPos[0] += 1
                case pygame.K_UP:
                    playerPos[1] -= 1
                case pygame.K_DOWN:
                    playerPos[1] += 1
            playerPos[0] = clamp(playerPos[0],0,7)
            playerPos[1] = clamp(playerPos[1],0,7)
        if event.type == pygame.VIDEORESIZE:
            screen.blit(pygame.transform.scale(screen, event.dict['size']), (0, 0))
            pygame.display.update()
            WIDTH,HEIGHT = event.dict['size']
        if event.type == pygame.VIDEOEXPOSE:  # handles window minimising/maximising
            screen.fill((0, 0, 0))
            screen.blit(pygame.transform.scale(screen, screen.get_size()), (0, 0))
        

    ### BIG SCREEN UPDATER FOLLOWS !!! 

    drawBase()
    game.blit(player,(playerPos[0]*blockSize+50,playerPos[1]*blockSize+75)) # draw player with offsets accounted for on grid
    pygame.draw.rect(screen,BLUE,pygame.Rect(0, 0, WIDTH, HEIGHT)) #background ocean
    healthUpdater(health)

    # resizer
    screen.blit(pygame.transform.scale(game, (min(WIDTH,HEIGHT),min(WIDTH,HEIGHT))), ((WIDTH-min(WIDTH,HEIGHT))/2, (HEIGHT-min(WIDTH,HEIGHT))/2))
    #final update
    pygame.display.flip()

pygame.quit()