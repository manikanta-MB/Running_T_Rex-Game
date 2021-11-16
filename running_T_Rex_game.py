import os
import time
#import random
from collections import deque
import pygame
from pygame.locals import *

class Dino:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(os.getcwd()+"/resources/dino_image_3.jpg").convert()
        self.x = 0
        self.y = 150
    def move_up(self):
        self.y = max(self.y-100,0)
    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))
        self.y = min(self.y+30,150)
class Lamp:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(os.getcwd()+"/resources/fire_lamp_3.jpg").convert()
        self.x = [876]*5
        self.y = [150]*5
        self.positions_to_display = deque([False,False,False,True,True])
    def swap_positions(self):
        first_ele = self.positions_to_display.popleft()
        self.positions_to_display.append(first_ele)
    def shift(self):
        for i in range(len(self.x)-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
    def modify(self):
        if(self.x[0]-219 < 0):
            self.x.append(-1)
            self.y.append(-1)
            self.shift()
            del self.x[0],self.y[0]
        else:
            self.shift()
            self.x[0] -= 219
    '''
    def draw(self):
        self.modify()
        # self.parent_screen.fill((255,255,255))
        for i in range(5):
            if(random.randint(0,1)):
                self.parent_screen.blit(self.image,(self.x[i],self.y[i]))
    '''
class Grass:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(os.getcwd()+"/resources/grass_image_4.jpg").convert()
        self.x = [876]*5
        self.y = [200]*5
    def shift(self):
        for i in range(len(self.x)-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
    def modify(self):
        if(self.x[0]-219 < 0):
            self.x.append(-1)
            self.y.append(-1)
            self.shift()
            del self.x[0],self.y[0]
        else:
            self.shift()
            self.x[0] -= 219
    '''
    def draw(self):
        self.modify()
        self.parent_screen.fill((255,255,255))
        for i in range(5):
            self.parent_screen.blit(self.image,(self.x[i],self.y[i]))
    '''
class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1095,500))
        self.grass = Grass(self.surface)
        # self.grass.draw()
        self.lamp = Lamp(self.surface)
        # self.lamp.draw()
        self.dino = Dino(self.surface)
    def draw(self):
        self.grass.modify()
        self.lamp.modify()
        self.surface.fill((255,255,255))
        for i in range(5):
            self.surface.blit(self.grass.image,(self.grass.x[i],self.grass.y[i]))
            if(self.lamp.positions_to_display[i]):
                self.surface.blit(self.lamp.image,(self.lamp.x[i],self.lamp.y[i]))
        self.lamp.swap_positions()
        self.dino.draw()
    def play(self):
        self.draw()
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_SPACE:
                        self.dino.move_up()
                elif event.type == QUIT:
                    running = False
            
            self.play()
            time.sleep(0.5)

if __name__=="__main__":
    game = Game()
    game.run()
