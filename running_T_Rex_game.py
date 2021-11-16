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
        self.y = min(self.y+50,150)
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
    def draw(self):
        self.modify()
        # self.parent_screen.fill((255,255,255))
        for i in range(5):
            if(self.positions_to_display[i]):
                self.parent_screen.blit(self.image,(self.x[i],self.y[i]))
        self.swap_positions()
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
        self.lamp = Lamp(self.surface)
        self.dino = Dino(self.surface)
        self.countdown = 60
    '''
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
    '''
    def reset(self):
        self.grass = Grass(self.surface)
        self.lamp = Lamp(self.surface)
        self.dino = Dino(self.surface)
        self.countdown = 60
    def display_time(self):
        mins, secs = divmod(self.countdown, 60)
        timer = "Timer: {:02d}:{:02d}".format(mins, secs)
        font = pygame.font.SysFont('arial',20)
        timer_block = font.render(timer,True,(0,0,0))
        self.surface.blit(timer_block,(850,10))
        self.countdown -= 1
    def show_game_win_message(self):
        self.surface.fill((255,255,255))
        font = pygame.font.SysFont('arial',30)
        line1 = font.render("Congrats! You Won the Game",True,(0,0,0))
        line2 = font.render("Want to Play Again, press Enter",True,(0,0,0))
        self.surface.blit(line1,(300,200))
        self.surface.blit(line2,(300,250))
        pygame.display.flip()
    def play(self):
        if(self.countdown == 0):
            raise TimeoutError
        self.grass.draw()
        self.lamp.draw()
        self.dino.draw()
        self.display_time()
        pygame.display.flip()
        
    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                    if not pause:
                        if event.key == K_SPACE:
                            self.dino.move_up()
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except TimeoutError:
                self.show_game_win_message()
                pause = True
                self.reset()
            time.sleep(0.5)

if __name__=="__main__":
    game = Game()
    game.run()
