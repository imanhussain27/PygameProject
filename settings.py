#this  class is going to store all of the settings for our alien invasion game
class Settings:
    """a class to store all settings for Alien Invasion"""

#initialize the game settings
# define the screen settings
# now that we've defined our game settings, we need to go back to our alien_invasion.py and make an instance in the project to access our settings   

    def __init__(self):
        """initialize the game's static settings"""
        #here are the screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #here are the ship settings
        self.ship_limit = 3

        #here are the bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        #here are the alien settings
        self.fleet_drop_speed = 10

        #this shows how quicly the game speeds up
        #we add this setting control below to control how quickly the game speeds up
        self.speedup_scale = 1.1
        #how quickly the alien point values increase & we define a rate at which points increase below
        self.score_scale = 1.5
        #here we call this method to initialize the values for the attributes that need to change during the entire game
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """initialize settings that change throughout the game"""
        #we adjust the ships speed below, the position will be adjusted by 1.5 pixels rather than just 1 throughout the loop
        #we are using decimal so that we can have finer control over the ship's speed
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        #here is the scoring
        self.alien_points = 50

    def increase_speed(self):
        """increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        #we want to increase the game's speed so we increase the point value of each hit
        self.alien_points = int(self.alien_points * self.score_scale)