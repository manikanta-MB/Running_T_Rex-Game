import os
import time
from collections import deque
import pygame
from pygame.locals import *

WHITE_COLOR = (255,255,255)
BLACK_COLOR = (0,0,0)
RED_COLOR = (255,0,0)
GREEN_COLOR = (0,255,0)
BLUE_COLOR = (0,0,255)

# Custom Exception Classes
class CollisionError(Exception):
    """This is a Collision Exception Class that we will use when the collision occurs."""
    def __init__(self,message):
        self.message = message

class TimeUp(Exception):
    """This is a TimeUp Exception Class that we will use when the time
    for the game is completed.
    """
    def __init__(self,message):
        self.message = message

class Dino:
    """This Class is designed for the Dinosaur object in the Game.
    It will take care about all the operations that dinosaur will do,
    like moving up, moving down, collision with lamp.
    """
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        # loading the dinosaur image.
        self.image = pygame.image.load(os.getcwd()+"/resources/dino_image_5.jpg").convert()
        self.x = 0
        self.y = 250
        self.image_height = 100 # It is the height of the dinosaur image.
        # By default we specify the direction as down unless user presses the "Space Bar".
        # Space Bar changes the direction to "up".
        self.direction = "down"
    def is_collision(self):
        # It is checking if the dinosaur hits the lamp(it starts at 250 on y-axis)
        if self.y+self.image_height < 270:
            return False
        else:
            return True
    def move_up(self):
        #It is moving the dinosaur towards top, upto 0 on y-axis.
        self.y = max(self.y-100,100)
        self.direction = "up"
    def draw(self):
        """It draws the dinosaur image on the given position"""
        # if the user didn't press on space bar, it(dinosaur) will automatically move towards bottom.
        if(self.direction == "down"):
            self.y = min(self.y+50,250)
        self.parent_screen.blit(self.image,(self.x,self.y))
        # Regardless of Previous direction, we will always set the direction as down after 
        # drawing dinosaur image on Game Board.
        self.direction = "down"

class Lamp:
    """This Class is designed for the Lamp object in the Game.
    It will take care about all the operations like moving lamps left alternatively
    and circularly, and at the same time displaying lamps on the game board.
    """
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(os.getcwd()+"/resources/fire_lamp_3.jpg").convert()
        # Pre-defined x-axis values for the Lamps based on the resolution of the Game Board.
        self.x = [40,259,478,697,916]*5
        self.y = 250
        # It will maintain the positions of the lamp to be displayed.
        self.positions_to_display = deque([True,False,False,False,True])
    def swap_positions(self):
        """It will swap the positions of the lamp to be displayed,
        circulary.
        """
        first_ele = self.positions_to_display.popleft()
        self.positions_to_display.append(first_ele)
    def draw(self):
        """It draws the Lamps circulary on game board."""
        self.swap_positions()
        for i in range(5):
            if(self.positions_to_display[i]):
                self.parent_screen.blit(self.image,(self.x[i],self.y))

class Grass:
    """This Class is designed for the Grass object in the Game.
    It will take care about all the operations like moving grass left circularly
    and at the same time displaying grass on the game board.
    """
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(os.getcwd()+"/resources/grass_image_4.jpg").convert()
        # Pre-defined x-axis values for the Grass based on the resolution of the Game Board.
        self.x = [0,219,438,657,876]*5
        self.y = 300
    def draw(self):
        """It draws the Grass on the Game Board."""
        self.parent_screen.fill(WHITE_COLOR)
        for i in range(5):
            self.parent_screen.blit(self.image,(self.x[i],self.y))

class Game:
    """It is Main Class for this game.It will run the entire game with the help of
    above sub classes.
    """
    def __init__(self):
        pygame.init() # initializing the game board.
        pygame.mixer.init() # intializing the music in game.
        game_board_width = 1095
        game_board_height = 500
        # setting the resolution of game board.
        self.surface = pygame.display.set_mode((game_board_width,game_board_height))
        self.play_background_music() # playing background music for this game.
        # Initializing all the helper Classes.
        self.grass = Grass(self.surface)
        self.lamp = Lamp(self.surface)
        self.dino = Dino(self.surface)
        self.countdown = 60 # It is a time constraint for the game to be completed within that duration.
    def play_background_music(self):
        """It will play the background music."""
        pygame.mixer.music.load(os.getcwd()+"/resources/bg_music_1.mp3")
        pygame.mixer.music.play()
    def reset(self):
        """It resets the objects when the game is completed or failed, 
        to play the game from initial state.
        """
        self.grass = Grass(self.surface)
        self.lamp = Lamp(self.surface)
        self.dino = Dino(self.surface)
        self.countdown = 60
    def display_time(self):
        """As the name suggests, it will display the remaining time of the game to be completed."""
        mins, secs = divmod(self.countdown, 60)
        timer = "Timer: {:02d}:{:02d}".format(mins, secs)
        font = pygame.font.SysFont('arial',20)
        timer_block = font.render(timer,True,BLACK_COLOR)
        position_of_timer = (850,10)
        self.surface.blit(timer_block,position_of_timer)
        self.countdown -= 1
    def show_game_win_message(self):
        """As the name suggests, it will display a Succes message when you won the game."""
        self.surface.fill(WHITE_COLOR)
        font = pygame.font.SysFont('arial',30)
        line1 = font.render("Congrats! You Won the Game",True,GREEN_COLOR)
        line2 = font.render("Want to Play Again, press Enter",True,BLUE_COLOR)
        position_of_line1 = (300,200)
        position_of_line2 = (300,250)
        self.surface.blit(line1,position_of_line1)
        self.surface.blit(line2,position_of_line2)
        pygame.display.flip()
    def show_game_lost_message(self):
        """As the name suggests, it will display a Failure message when you fail the game or
        hit the lamp.Along with that message, it will also give you an other option to play the
        Game Again.
        """
        self.surface.fill(WHITE_COLOR)
        font = pygame.font.SysFont('arial',30)
        line1 = font.render("Oh! You lost the game",True,RED_COLOR)
        line2 = font.render("Wanna Play Again!, press Enter",True,BLUE_COLOR)
        position_of_line1 = (300,200)
        position_of_line2 = (300,250)
        self.surface.blit(line1,position_of_line1)
        self.surface.blit(line2,position_of_line2)
        pygame.display.flip()
    def play_sound(self,file_path):
        """It will play the sound when the dinosaur hits the lamp."""
        sound = pygame.mixer.Sound(file_path)
        pygame.mixer.Sound.play(sound)
    def play(self):
        """This is a function to be called to render the changes onto the Game Board for every
        second, from the loop(while loop in run() method below.) that runs the Game.
        """
        # If the time for the game is completed, it will throw a TimeUpError Exception.
        # So that we can stop the game.
        if(self.countdown == 0):
            pygame.mixer.music.pause()
            raise TimeUp("Time Completed")
        # Drawing all the objects with changes, onto the Game Board.
        self.grass.draw()
        self.lamp.draw()
        self.dino.draw()
        self.display_time()
        pygame.display.flip()
        # First condition checks if the first lamp is displayed, in the current Lamp Circle.
        # Then only there is a possiblity for the dinosaur to hit the lamp.
        # Only first lamp in the current window can be hit by Dinosaur.
        if self.lamp.positions_to_display[0]:
            # It checks if the dinosaur hits the Lamp.
            if self.dino.is_collision():
                pygame.mixer.music.pause()
                self.play_sound(os.getcwd()+"/resources/crash.mp3")
                raise CollisionError("collision occured.")
        
    def run(self):
        """This method is the Head of this Entire Game.
        It will take all the inputs or actions from the user and then apply the changes
        accordingly and then display them.
        """
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
            except TimeUp:
                self.show_game_win_message()
                pause = True
                self.reset()
            except CollisionError:
                # when the collision occurs, game is in ideal position for 2 seconds.
                time.sleep(2.0)
                self.show_game_lost_message()
                pause = True
                self.reset()
            # It is the delay time between every two adjacent renderings or changes on the Game Board.
            # It decides the speed of the game.
            time.sleep(0.5)

if __name__=="__main__":
    game = Game()
    game.run()
