import pygame.font
from pygame.sprite import Group
 
from ship import Ship

class Scoreboard:
    """a class to report scoring information"""

    #we give the init method this parameter so that it can access the settings, screen, and stats objects which will report the values to our tracking
    def __init__(self, ai_game):
        """initialize scorekeeping attributes"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        #here we set a text color
        self.text_color = (30, 30, 30)
        #below, we instantiate a font object
        self.font = pygame.font.SysFont(None, 48)

        #the code below allows us to turn the text into an image when displayed; we prepare the initial score images
        self.prep_score()
        #the high score is to be displayed separately from the other score so this method does that (below)
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """turn the score into a rendered image"""
        #this code tells python to round the value of stats.s-core to the nearest 10 and store it in rounded_score
        rounded_score = round(self.stats.score, -1)
        #a string formatting directive tells python to insert commas into numbers when converting a numerical value to a string
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                self.text_color, self.settings.bg_color)
        
        #this code tells the program to display the score in the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """turn the high score into a rendered image"""
        #we round the high score to the nearest 10 and format it with commas
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        #we then generate an image from the high score using the code below
        self.high_score_image = self.font.render(high_score_str, True,
                self.text_color, self.settings.bg_color)
            
        #center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        #center the high score horizontally
        self.high_score_rect.centerx = self.screen_rect.centerx
        #set its top attribute to match the top of the score image
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """turn the level into a rendered image"""
        level_str = str(self.stats.level)
        #this method creates an image from the value stored in stats.level
        self.level_image = self.font.render(level_str, True,
                self.text_color, self.settings.bg_color)
    
        #position the level below the score
        self.level_rect = self.level_image.get_rect()
        #this sets the image's right attribute to match the score's right attribute
        self.level_rect.right = self.score_rect.right
        #it then sets the top attribute 10 pixels below the bottom of the score image to leave space between
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """show how many ships are left"""
        #to fill this group, we use the code below as a loop that runs once for every ship the player has left
        self.ships = Group()
        #below, inside the loop, we create a new ship and set each ship's x-coodinate value so that the ships appear next to each other
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            #below, we set the y-coordinate value 10 pixels down from the top so that the ships appear in the upper left corner
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            #we add each new ship to the group of ships
            self.ships.add(ship)

    def check_high_score(self):
        """check to see if there's a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """draw scores, level, and ships to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)