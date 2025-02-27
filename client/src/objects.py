import pygame

class GameObject:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self, screen):
        """Draw the object on the screen."""
        screen.blit(self.image, (self.x, self.y))

class MainMenuButton(GameObject):
    """Button for the main menu."""
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def is_clicked(self, event):
        """Check if the button is clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button_rect = self.image.get_rect(topleft=(self.x, self.y))
            return button_rect.collidepoint(mouse_x, mouse_y)
        return False