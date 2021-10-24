import pygame
from pygame.sprite import Sprite
 
class Alien(Sprite):
    """a class to represent a single alien in the fleet"""

    def __init__(self, ai_game):
        """initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #here, we load the alien image and set its rect attribute below
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #we add a space to the left here so that it's equal to the alien's width and space above it
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #we are concerned about the horizontal speed so we'll track the horizonal position of each alien precisely
        self.x = float(self.rect.x)

    def check_edges(self):
        """return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        #we know it's at the left edge if its value is less than or equal to 0
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """move the alien right or left"""
        #we change the update() method to allow motion to the left or right by multiplying the alien's speed by the value of the fleet direction
        self.x += (self.settings.alien_speed *
                        self.settings.fleet_direction)
        self.rect.x = self.x