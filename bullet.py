import pygame
from pygame.sprite import Sprite
 
#when you use sprite, you can group related elements in your game and act on all of the grouped elements at the same time
class Bullet(Sprite):
    """a class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """create a bullet object at the ship's current position"""
        #let's create a bullet object at the ship's current position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #now let's create a bullet rect at (0,0) and then set the correct position
        #we create the bullet's rect attribute, it's not based on an image so we have to create it from scratch using pygame.Rect() class
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        #we set the bullet's midtop attribute below to match the ship's midtop attribute so that the bullet can emerge from the top of the ship
        self.rect.midtop = ai_game.ship.rect.midtop
        
        #now let's store all of the bullet's positions as a decimal value, adjustments to the bullet's speed
        self.y = float(self.rect.y)

    def update(self):
        """move the bullet up the screen"""
        #we subtract the amount stored in the settings.bullet_speed from self.y to update the position
        self.y -= self.settings.bullet_speed
        #we then use the value of self.y to set the value of self.rect.y; this updates the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """draw the bullet to the screen"""
        #when we want to draw a bullet, we call the code below so that it fills the part of the screen defined by the bullet's rect with the color we stored and chose
        pygame.draw.rect(self.screen, self.color, self.rect)