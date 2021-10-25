# PygameProject

alien_invasion.py
    This is the main file, it has the alien_invasion class and the main loop of the game that also contains the while loop. The while loop calls _check_events(), _update_screen(), and ship.update() methods.

ship.py
    This file contains the ship class and all of the details about the ship that we use in the game. The ship class has the init, update(), and blitme() methods. The update() method manage's the ship's position while the blitme() method draws the ship onto the screen.

settings.py
    This file contains all of the settings details within the Settings class. The settings for the ship, alien, screen etc is all stored in this file.

alien.py
    This file contains all of the alien and fleet details within the Alien class. It also contains the update() and check_edges methods to direct the direction of the fleet of aliens.

bullet.py
    This file contains all of the bullet details within the Bullet class. It also has the method to draw the bullets onto the actual screen and the update method to update the positions of the bullets on the screen.

button.py
    This file is pretty simple and basically draws the green play button we see in the middle of the screen when we first run the game. Pushing this button is what allows the player to begin playing the game. 

scoreboard.py
    This file is responsible for keeping track of the score while the player is playing the game and earning points. It also remembers the high score during the rounds the player is playing; it also compares the current score to the highest score and updates the high score accordingly.

game_stats.py
    This file creates the GameStats class which contains all of the details about how the scoring is done for the game. It keeps track of the game levels and the score; it also resets all of the elements (certain ones) that are suppose to reset when the game/round starts again.
