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
spider = pygame.transform.scale(pygame.image.load("assets/bug.png"),(blockSize,blockSize))

entity = {
    "x":0,
    "y":0,
    "type":""
}



playerPos = [4,4]
health = 5
iFrames = 0
wasHit = False

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


tickCounter = 0


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

class Entity:
    def __init__(self,x,y,type) -> None:
        self.x = x
        self.y = y
        self.type = type
    def render(self):
        if self.type=="spider":
            game.blit(spider, (self.x*blockSize+50,self.y*blockSize+75))
        

entities = []

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

    tickCounter+=1
    if random.randint(0,100) == 50:
        if len(entities) < 5:
            entities.append(Entity(random.randint(0,7),random.randint(0,7),"spider"))

    for n in entities:
        if n.x == playerPos[0] and n.y == playerPos[1] and iFrames == 0:
            wasHit = True
            health -= 1
    if wasHit == True:
        iFrames += 1
        if iFrames > 30:
            iFrames = 0
            wasHit = False

    ### BIG SCREEN UPDATER FOLLOWS !!! 
    drawBase()
    game.blit(player,(playerPos[0]*blockSize+50,playerPos[1]*blockSize+75)) # draw player with offsets accounted for on grid
    pygame.draw.rect(screen,BLUE,pygame.Rect(0, 0, WIDTH, HEIGHT)) #background ocean
 
    if tickCounter >= 30:
        for n in entities:
            if playerPos[0] > n.x:
                n.x += 1
            elif playerPos[0] < n.x:
                n.x -= 1
            
            if playerPos[1] > n.y:
                n.y += 1
            elif playerPos[1] < n.y:
                n.y -= 1

            n.render()
        tickCounter = 0
    for n in entities:
        n.render()
        
   
    

    # UI
    healthUpdater(health)

    # debug prints
    print(tickCounter)

    # resizer
    screen.blit(pygame.transform.scale(game, (min(WIDTH,HEIGHT),min(WIDTH,HEIGHT))), ((WIDTH-min(WIDTH,HEIGHT))/2, (HEIGHT-min(WIDTH,HEIGHT))/2))

    #final update
    pygame.display.flip()

pygame.quit()