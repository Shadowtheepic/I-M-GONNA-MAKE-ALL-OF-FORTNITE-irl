import pygame
import random
import time

pygame.init()
pygame.display.set_caption("Inchaders")
ScreenWidth = 800
ScreenHeight = 800
screen = pygame.display.set_mode((ScreenWidth,ScreenHeight))
clock = pygame.time.Clock()
green = (0, 255,0)
blu = (0, 0, 255)
player = pygame.image.load('I CAN1.gif')


doExit = False
xpos = 0
ypos = 700
Vx = 0
#constants
LEFT = 0
RIGHT = 1
SPACE = 2
keys = [False, False, False]
timer = 0
lives = 3

misslist = list()
justShot = 0


class Wall:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.numHits = 0
    def draw(self):
        if self.numHits == 0:
            pygame.draw.rect(screen, (250, 250, 20), (self.xpos, self.ypos, 30, 30))
        if self.numHits == 1:
            pygame.draw.rect(screen, (150, 150, 10), (self.xpos, self.ypos, 30, 30))
        if self.numHits == 2:
            pygame.draw.rect(screen, (50, 50, 0), (self.xpos, self.ypos, 30, 30))
            
    def collide(self, BulletX, BulletY):
        if self.numHits < 3:
            if BulletX > self.xpos:
                if BulletX < self.xpos + 30:
                    if BulletY < self.ypos + 30:
                        if BulletY > self.ypos:
                            print("hit!")
                            self.numHits += 1
                            return False
        return True
        

walls = []
for k in range(4):
    for i in range(2):
        for j in range(3):
            walls.append(Wall(j*30+200 * k + 50, i * 30 + 600))

class Alien:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = True
        self.direction = 1
    def draw(self):
        if self.isAlive == True:
            pygame.draw.rect(screen, (250, 250, 250), (self.xpos, self.ypos, 40, 40))
        
    def move(self, time):
        
        #reset what direction you're moving every 8 moves:
        if time % 800 == 0:
            self.ypos += 100
            self.direction *= -1
            return 0
        
        if timer%100 == 0:
            self.xpos += 50 * self.direction
        
        return time
    
    def collide(self, BulletX, BulletY):
        if self.isAlive:
            if BulletX > self.xpos:
                if BulletX < self.xpos + 50:
                    if BulletY < self.ypos + 20:
                        if BulletY > self.ypos:
                            print("hit!")
                            self.isAlive = False
                            return False
        return True

armada = []
for i in range (4):
    for j in range(12):
        armada.append(Alien(j*60 + 70, i *50 + 70))
class Missile:
    def __init__(self):
        self.xpos = -10
        self.ypos = -10
        self.isAlive = False
        
    

class Bullet:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = False
        
    def move(self, xpos, ypos):
        if self.isAlive == True:
            self.ypos -=5
        if self.ypos < 0:
            self.isAlive = False
            self.xpos = xpos
            self.ypos = ypos
    
    def draw(self):
        if self.isAlive == True:
            pygame.draw.rect(screen, (250, 250, 250), (self.xpos, self.ypos, 3, 20))
#instantiate bullet object
bullet = Bullet(xpos+28, ypos)

class Missile:
    def __init__(self):
        self.xpos = -10
        self.ypos = -10
        self.isAlive = False
    def move(self):
        if self.isAlive == True:
            self.ypos +=5
        if self.ypos > 800:
            self.isAlive = False
            self.xpos = xpos
            self.ypos = ypos
    def draw(self):
        if self.isAlive == True:
            pygame.draw.rect(screen, (250, 250, 250), (self.xpos, self.ypos, 2, 10))

misslies = []

for i in range(10):
    misslies.append(Missile())

        


while lives > 0:
    clock.tick(60)
    timer += 1;
    
    for event in pygame.event.get(): #quit game if x is pressed in top corner
        if event.type == pygame.QUIT:
            gameover = True
      
        if event.type == pygame.KEYDOWN: #keyboard input
            if event.key == pygame.K_LEFT:
                keys[LEFT]=True
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT]=True
            if event.key == pygame.K_SPACE:
                keys[SPACE] = True

            
        if event.type == pygame.KEYUP: #keyboard input
            if event.key == pygame.K_LEFT:
                keys[LEFT]=False
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT]=False
            if event.key == pygame.K_SPACE:
                keys[SPACE] = False
                
    if keys[SPACE] == True:
        bullet.isAlive = True
        
    if bullet.isAlive == True:
        bullet.move(xpos+28, ypos)
        if bullet.isAlive == True:
            #alien collision
            for i in range(len(armada)):
                bullet.isAlive = armada[i].collide(bullet.xpos, bullet.ypos)
                if bullet.isAlive == False:
                    break
        if bullet.isAlive == True:
            for i in range(len(walls)):
                bullet.isAlive = walls[i].collide(bullet.xpos, bullet.ypos)
                if bullet.isAlive == False:
                    break
        
        
                
       
    
    else:
        bullet.xpos = xpos+28
        bullet.ypos = ypos
    
    
    for i in range(len(walls)):
        for j in range(len(misslies)):
            if misslies[j].isAlive == True:
                if walls[i].collide(misslies[j].xpos, misslies[j].ypos) == False:
                    misslies[j].isAlive = False
                    break
        
    buffa = random.randrange(100)
    if buffa < 2:
        armbruh = random.randrange(len(armada))
        if armada[armbruh].isAlive == True:
            for i in range(len(misslies)):
                if misslies[i].isAlive == False:
                    misslies[i].isAlive = True
                    misslies[i].xpos = armada[i].xpos + 5
                    misslies[i].ypos = armada[i].ypos
                    break
                
    #player collision
    for i in range(len(misslies)):
         if misslies[i].isAlive:
             if misslies[i].xpos > xpos:
                 if misslies[i].xpos < xpos + 40:
                     if misslies[i].ypos < ypos + 40:
                         if misslies[i].ypos > ypos:
                             lives -= 1
                             time.sleep(1)
                             xpos = 0
                             
    for i in range(len(armada)):
            if armada[i].ypos > ypos:
                        lives -= 3
                        print("Bruh how did they get this low")
                        time.sleep(1)
                        break
                        
                             
    
                
    #left movement            
    if keys[LEFT]==True:
        Vx = -5
        direction = LEFT
        
    #Right Movement
    elif keys[RIGHT]==True:
        Vx = 5
        direction = RIGHT
        
    else:
        Vx = 0
    #updating player
    xpos += Vx
    
    for i in range(len(armada)):
        armada[i].move(timer)
    for i in range(len(misslies)):
        misslies[i].move()

    
    screen.fill((0,0,0))
    
    
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render('LIVES:', False, (255, 0, 0))
    number = my_font.render(str(lives), False, (255,0,0))
    
    
    screen.blit(player, (xpos, ypos))
    for i in range(len(armada)):
        armada[i].draw()
    for i in range(len(walls)):
        walls[i].draw()
    bullet.draw()
    for i in range(len(misslies)):
        misslies[i].draw()
    
    screen.blit(text_surface, (0,0))
    screen.blit(number, (100,0))
    
    
    pygame.display.flip()
    
print("RIP")

pygame.quit()
