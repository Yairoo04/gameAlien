import pygame
from pygame.sprite import Sprite
import os

class Explosion(Sprite):
    """A class to manage explosion animation when an alien is hit."""

    def __init__(self, ai_settings, screen, position):
        """Initialize the explosion at the given position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the explosion image
        base_path = os.path.dirname(os.path.abspath(__file__))
        explosion_path = os.path.join(base_path, 'images', 'explode.png')
        self.image = pygame.image.load(explosion_path)
        self.rect = self.image.get_rect()

        # Set position of the explosion (center at the alien's position)
        self.rect.center = position

        # Load and play the explosion sound
        sound_path = os.path.join(base_path, 'sounds', 'explosion.mp3')
        self.explosion_sound = pygame.mixer.Sound(sound_path)
        self.explosion_sound.play()

        # Timer to control how long the explosion is displayed (in milliseconds)
        self.duration = 500  # Explosion lasts for 0.5 seconds
        self.start_time = pygame.time.get_ticks()

    def update(self):
        """Update the explosion state."""
        # Check if the explosion duration has passed
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            self.kill()  # Remove the explosion sprite after duration

    def draw(self):
        """Draw the explosion to the screen."""
        self.screen.blit(self.image, self.rect)