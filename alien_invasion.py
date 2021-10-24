#the import sys line imports the module who's tools we will use when a player wants to quit and exit the game
import sys
from time import sleep

#the import pygame line imports the module that has the functions we need in order to create the game
import pygame

#here, we are creating an instance to use the settings we created
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

#here, we import the ship
from ship import Ship

#here, we import the bullets
from bullet import Bullet
from alien import Alien

#create an overall class to manage all game assets and behaviors below
class AlienInvasion:
    """overall class to manage game assets and behavior"""

#now, initialize the game and create your game resources, this function will initialize the background settings that the game needs in order to function properly
#the display.set_mode function will allow us to create a display window where we can draw the game's graphical elements
#the tuple arguments of 1200 and 800 define the dimensions of the game window in terms of pixels
#we want to assign this all to the attribute self.screen so that it can be available to all of the methods in the class, the object assigned is called a surface
#a surface in pygame is a part of the screen where any game element can be portrayed, each element (alien/ship) is its own surface
#the surface returned by the display.set_mode() accounts for the entire game window
#when we activate the game's loop, the surfaces will be re-drawn and updated with any inputs/changes from the player's input
#let's change the background color of the display from black to something else, that's the last line in the init method
    #colors in pygame are a mix of RGB (red,green,blue) and range from 0-255
    #(255,0,0) is red
    #(0,255,0) is green
    #(0,0,255) is blue
    #(230,230,230) does an even mix of RGB which produces a light gray background and we assigned it to self.big_color
#under pygame.init() we are going to add our settings
#initially, the self.screen was this: self.screen=pygame.display.set_mode((1200,800))
    #but now we are going to change it since we created our settings file, we don't have to hardcode it
#for self.ship, we called it and it requires one argument and is an instance, the self argument refers to the current instance of Iman's Alien Invasion
    def __init__(self):
        """initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()

        #the code line below tells pygame to figure out a window size that will fit the screen because the dimensions are unknown to us
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        #here we use the width and the height attriubutes of the screen'srect to update the settings object
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        #replacing the code below with the code above for full screen purposes
        #self.screen=pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Iman's Alien Invasion")

        #here, we create an instance to store the game stats
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")

#now, start the main loop for the alien invasion game
#create a while loop that watches for keyboard and mouse strokes/events
#the entire game is controlled by the run_game method because it contains the while loop that will continously run
#this while loop contains an event loop and an event is an action that the player activates/does while playing our game
    #an example of an event could be pressing a key or moving their mouse
#the last line in this def method will redraw the screen during each pass through the while loop
#we fill the screen with the background color from above ^ in the fill() method that only takes one argument: the color
#same deal with self.screen.fill, originally self.screen.fill(self.bg_color)
#now we don't need to hardcode it and we can change it to what it is now below
#after filling in the background, we draw the ship on the screen by calling ship.blitme()

    def run_game(self):
        """start the main loop for the game"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                #the group automatically calls update() for each sprite in the group
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            #we check here if the key pressed is the right arrow key
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            #we add a new elif block which responds to keyup events  
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            #below, we allow the pygame to detect when a player clicks anywhere on the screen and we want to restrict our game to respond to clicks only on the play button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #we accomplish this because the code beloow returns a tuple containing the  mouse cursor and when the button is clickeed
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """start a new game when the player clicks play"""
        #the flag will store a true or false value
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        #the game will only restartr if play is clicked and the game is not currently active
        if button_clicked and not self.stats.game_active:
            #here, we reset the game settings
            self.settings.initialize_dynamic_settings()

            #here we reset the game stats which gives the player 3 new ships
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #here we empty the bullets and alien groups
            self.aliens.empty()
            self.bullets.empty()
            
            #and then here we create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #here, we hide the mouse cousur
            pygame.mouse.set_visible(False)

    #we created a new helper method here
    #both need a self parameter and an event one because the bodies of these 2 helper methods are copied from the _check_events()
    def _check_keydown_events(self, event):
        """respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            #here we modify how the game responds when the player presses the right arrow key
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        #here we create an easier way for the player to quit the game instead of having to press the x button everytime
        elif event.key == pygame.K_q:
            sys.exit()
        #below, we make an instance of the bullet and call it new bullet
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    #we created a new helper method here
    #both need a self parameter and an event one because the bodies of these 2 helper methods are copied from the _check_events()
    def _check_keyup_events(self, event):
        """respond to key releases"""
        #the right arrow key is pressed
        if event.key == pygame.K_RIGHT:
            #here we modify how the game responds when the player presses the right arrow key
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            #here we add it to the group of bullets using the add() method
            new_bullet = Bullet(self)
             #the add method is similar to the append method but it's a method that is specifically for Pygame groups
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """update position of bullets and get rid of old bullets"""
        #here, we update the bullet's positions
        self.bullets.update()

        #here, we get rid of the bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                 self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """respond to bullet-alien collisions"""
        #here, we remove any collided bullets and aliens
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            #here, we destroy the existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #here we increase the level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """check if the fleet is at an edge, then update the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        #here, we look for any collisions; if no collisions occur, this method returns none and the if block won't execute
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #here we look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            #an alien reaches the bottom of the screen when its rect.bottom value is greater than or equal to the screen's rect.bottom attribute
            if alien.rect.bottom >= screen_rect.bottom:
                #here we treat it the same as if the ship got hit
                self._ship_hit()
                break

    def _ship_hit(self):
        """respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            #the number of ships left is reduced by 1 and update the scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            
            #we empty the groups aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            
            #we create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            
            #we add a pause after all of the updates have been made so that the player can see that their ship has been hit
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """create the fleet of aliens"""
        #we create an alien here below so that we know the alien's width and height for placement purposes; 
            #create an alien and find the number of aliens in a row; spacing between each alien is equal to one alien width
        alien = Alien(self)
        #below, we use the attribute size which contains a tuple with the width and height of a rect object
        alien_width, alien_height = alien.rect.size
        #here we calculate the horizonal space available for aliens and the # of aliens that can fit in that space
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        ship_height = self.ship.rect.height
        #the code below calculates the number of rows we can fit on our screen
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        #we use two nested loops (an outter and inner one) to create multiple rows; create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """create an alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        #here we change the alien's coordinate value when it's not in the first row
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """respond appropriately if any aliens have reached an edge"""
        #we loop through the fleet and call check_edges() on each alien
        for alien in self.aliens.sprites():
            if alien.check_edges():
                #if it returns true, then we know an alien is at the edge and the fleet needs to change direction so we call this method to break out of the loop
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        """drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            #here we loop thru all of the aliens and drop each one using this settings and then we change the value of the direction by multiplyi8ng the value by -1
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
         #to draw all fired bullets to the screen, we loop through the sprites in the bullets and call draw_bullet() on each one
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #here we draw the score info
        self.sb.show_score()

        #here, if the game is inactive, we draw the play button
        if not self.stats.game_active:
            self.play_button.draw_button()

    #now, display the most recently drawn/created screen visible
    #for this specific case, it just draws an empty screen on each pass through the loop
    #it erases the old screen so that only the new screen is visible
    #this function below is responsible for the smooth movement of the game elements because it continually updates the display to show new positions and erases the old positions
        pygame.display.flip()

#now, you can create/make a game instance and run the game!!
#we put this in an if function so that it only runs if the file is directly called
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

#refactor code: simplifies the structure of the code which makes it easier to build on
#we are going to break the run_game() method into 2 helper methods which work inside of a class but isn't meant to be called thru an instance
# a single leading underscore represets a helper method ex: (_iman)