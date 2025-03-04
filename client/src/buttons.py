import pygame

class Button:
    def __init__(self, pos, width, height, text, action=None):
        self.rect = pygame.Rect(pos, (width, height))
        self.color = (140, 50, 0)  # Button color
        self.text = text
        self.font = pygame.font.Font(None, 36)  # Default font, size 36
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.action = action  # Action to be performed when clicked

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)  # Draw the button
        surface.blit(self.text_surface, self.text_rect)  # Draw the text

    def is_clicked(self, mouse_pos):
        print("CLICK! from buttons.py") # debug
        return self.rect.collidepoint(mouse_pos)  # Check if mouse clicks inside the button

    def click(self):
        if self.action:
            print(f"Button '{self.text}' clicked from buttons.py") # debug 
            self.action()  # Call the button's action if defined