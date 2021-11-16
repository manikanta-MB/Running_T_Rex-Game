import os
import time
from collections import deque
import pygame
from pygame.locals import *

class CollisionError(Exception):
    def __init__(self,message):
        self.message = message

class Dino:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(os.getcwd()+"/resources/dino_image_3.jpg").convert()
        self.x = 0
        self.y = 250
        self.image_height = 100
        self.direction = "down"
    def is_collision(self):
        if self.y+self.image_height < 270:
            return False
        else:
            return True
    def move_up(self):
        self.y = max(self.y-100,0)
        self.direction = "up"
    def draw(self):
        if(self.direction == "down"):
            self.y = min(self.y+50,250)
        self.parent_screen.blit(self.image,(self.x,self.y))
        self.direction = "down"
        # self.y = min(self.y+50,150)
class Lamp:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(os.getcwd()+"/resources/fire_lamp_3.jpg").convert()
        self.x = [916]*5
        self.y = [250]*5
        self.positions_to_display = deque([True,False,False,False,True])
    def swap_positions(self):
        first_ele = self.positions_to_display.popleft()
        self.positions_to_display.append(first_ele)
    def shift(self):
        for i in range(len(self.x)-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
    def modify(self):
        if(self.x[0]-219 < 0):
            pass
        else:
            self.shift()
            self.x[0] -= 219
    def draw(self):
        self.modify()
        # self.parent_screen.fill((255,255,255))
        self.swap_positions()
        for i in range(5):
            if(self.positions_to_display[i]):
                self.parent_screen.blit(self.image,(self.x[i],self.y[i]))
class Grass:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(os.getcwd()+"/resources/grass_image_4.jpg").convert()
        self.x = [876]*5
        self.y = [300]*5
    def shift(self):
        for i in range(len(self.x)-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
    def modify(self):
        if(self.x[0]-219 < 0):
            pass
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
        pygame.mixer.init()
        self.surface = pygame.display.set_mode((1095,500))
        self.play_background_music()
        self.grass = Grass(self.surface)
        self.lamp = Lamp(self.surface)
        self.dino = Dino(self.surface)
        self.countdown = 60
    def play_background_music(self):
        pygame.mixer.music.load(os.getcwd()+"/resources/bg_music_1.mp3")
        pygame.mixer.music.play()
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
        line1 = font.render("Congrats! You Won the Game",True,(0,255,0))
        line2 = font.render("Want to Play Again, press Enter",True,(0,0,255))
        self.surface.blit(line1,(300,200))
        self.surface.blit(line2,(300,250))
        pygame.display.flip()
    def show_game_lost_message(self):
        self.surface.fill((255,255,255))
        font = pygame.font.SysFont('arial',30)
        line1 = font.render("Oh! You lost the game",True,(255,0,0))
        line2 = font.render("Wanna Play Again!, press Enter",True,(0,0,255))
        self.surface.blit(line1,(300,200))
        self.surface.blit(line2,(300,250))
        pygame.display.flip()
    def play_sound(self,file_path):
        sound = pygame.mixer.Sound(file_path)
        pygame.mixer.Sound.play(sound)
    def play(self):
        if(self.countdown == 0):
            pygame.mixer.music.pause()
            raise TimeoutError
        self.grass.draw()
        self.lamp.draw()
        self.dino.draw()
        self.display_time()
        pygame.display.flip()
        if self.lamp.positions_to_display[0] and self.lamp.x[0]==40:
            if self.dino.is_collision():
                pygame.mixer.music.pause()
                self.play_sound(os.getcwd()+"/resources/crash.mp3")
                raise CollisionError("collision occured.")
        
    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
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
            except CollisionError:
                time.sleep(2.0)
                self.show_game_lost_message()
                pause = True
                self.reset()
            time.sleep(0.5)

if __name__=="__main__":
    game = Game()
    game.run()
