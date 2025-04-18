# -*- coding: utf-8 -*-
import pygame.font
import os

class Button:
    def __init__(self, ai_settings, screen, msg, width=200, height=50, y_offset=0):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings

        # Button dimensions and colors
        self.width, self.height = width, height
        self.button_color = (100, 149, 237)         # Normal color
        self.hover_color = (65, 105, 225)           # Hover color
        self.text_color = (255, 255, 255)
        self.shadow_color = (50, 50, 50, 100)       # Semi-transparent dark shadow
        # Load custom TTF font to support Vietnamese characters
        base_path = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(base_path, 'fonts', 'Roboto-Regular.ttf')
        self.font = pygame.font.Font(font_path, 32)  # Reduced font size for proportionality

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (
            self.screen_rect.centerx,
            self.screen_rect.centery + y_offset
        )
        # Shadow rect (slightly offset)
        self.shadow_rect = self.rect.copy()
        self.shadow_rect.move_ip(5, 5)

        self.msg = msg
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn msg into a rendered image, and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw button with shadow, rounded corners, and hover effect."""
        mouse_pos = pygame.mouse.get_pos()

        # Draw shadow
        shadow_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, self.shadow_color, (0, 0, self.width, self.height), border_radius=12)
        self.screen.blit(shadow_surface, self.shadow_rect)

        # Draw button with hover effect
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen, current_color, self.rect, border_radius=12)

        # Draw message text
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def is_clicked(self, mouse_pos):
        """Return True if button is clicked."""
        return self.rect.collidepoint(mouse_pos)