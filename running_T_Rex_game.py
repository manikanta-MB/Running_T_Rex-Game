import os
import time
import random
import pygame
from pygame.locals import *
class Lamp:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(os.getcwd()+"/resources/fire_lamp_3.jpg")
        self.x = [876]*5
        self.y = [150]*5
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
    def draw(self):
        self.modify()
        # self.parent_screen.fill((255,255,255))
        for i in range(5):
            if(random.randint(0,1)):
                self.parent_screen.blit(self.image,(self.x[i],self.y[i]))
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
    def draw(self):
        self.modify()
        self.parent_screen.fill((255,255,255))
        for i in range(5):
            self.parent_screen.blit(self.image,(self.x[i],self.y[i]))
class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1095,500))
        self.grass = Grass(self.surface)
        self.grass.draw()
        self.lamp = Lamp(self.surface)
        self.lamp.draw()
    def play(self):
        self.grass.draw()
        self.lamp.draw()
        pygame.display.flip()
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False
            
            self.play()
            time.sleep(0.5)

if __name__=="__main__":
    game = Game()
    game.run()
