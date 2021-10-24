import pygame.font
 
class Button:
 
    #it takes these parameters because it contains the button's text
    def __init__(self, ai_game, msg):
        """initialize button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        #button dimensions and properties are set below
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        #we prepare a font attribute for rendering text, the none argument tells pygame to use the default font and 48 specifies the size of the text
        self.font = pygame.font.SysFont(None, 48)
        
        #this builds(sets) the button's center attribute to match that of the screen
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        #the code below handles this rendering; the button message needs to e prepped only one time
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """turn msg into a rendered image and center text on the button"""
        #this turns the text stored into an image
        self.msg_image = self.font.render(msg, True, self.text_color,
                self.button_color)
        #we center the text image on the button by reacting a rect from the image and setting its center attribute to match the button
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #here we draw the blank button and then the blank message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)