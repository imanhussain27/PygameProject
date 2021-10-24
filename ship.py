#now we will create a ship module that will contain the ship class
#this class will manage the behavior of the player's ship
#pygame is efficient because it lets you treat all game elements like rectangles even if that's not their exact shape
#this is efficient because they are simple geometric shapes which allows pygame to figure out game elements easier
#we will treat the ship and screen as rectangles for this purpose

import pygame
 
from pygame.sprite import Sprite
 
#creating a class ship to manage the ship
#the init will initialize the ship and set its starting position
#init method takes 2 parameters: the self reference and the reference to the current instance of the AlienInvasion class
#this will give the ship access to all of the game resources defiend in the AlienInvasion file
#below, we import sprite to make sure the ship inherits sprite
class Ship(Sprite):
    """a class to manage the ship"""
 
    def __init__(self, ai_game):
        """initialize the ship and set its starting position"""
        #here, we call super() at the beginning of __init__
        super().__init__()
        #below, we assign the screen to an attribute of the ship so we can easily access all the methods in this class
        self.screen = ai_game.screen
        #below, we need to assign the position to a variable that can store a decimal value so that we can adjust the ship's position
        self.settings = ai_game.settings
        #below, we access the screen's rect attribute using the get_rect() method and assign it to self.screen_rect(), doing this allows the correct placement 
        # of the ship on the screen
        self.screen_rect = ai_game.screen.get_rect()

        #now load the ship image and get its rect
        #this also gives it the location of our ship image
        #this function returns a surface representing a ship which is what we assign to self.image
        #once the image is loaded, we call get_rect() to access the ship's surface's attribute so that we can use it later
 
        #here we load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #here we tell the game to start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #store a decimal value for the ship's horizontal position
        #use the float function to convert the value of self.rect.x to a dcimal and assign the value to self.x
        self.x = float(self.rect.x)

        #here are the movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        #update the ship's position based on the movement flag below
        #will be called thru an instance of the ship so it's not considered a helper
        #now the value of self.x is adjusted by the amount stroed in settings.ship_speed
        #if the value of the left side of the rect is greater than 0 then the ship hasn't reached the left edge of the screen
        #this also ensures that the ship is within these bounds before adjusting the value of self x
        """update the ship's position based on movement flags"""
        #here we want to update the ship's x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        #here we update rect object from self.x
        self.rect.x = self.x

    #now draw the ship at its current location
    #here we define this method which draws the image to the screen at the specified location
    def blitme(self):
        """draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)