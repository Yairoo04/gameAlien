# -*- coding: utf-8 -*-
import pygame
from pygame.sprite import Group
import os

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf

def run_game():
    pygame.init()
    pygame.mixer.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    base_path = os.path.dirname(os.path.abspath(__file__))
    music_path = os.path.join(base_path, 'sounds', 'nhacNen.mp3')
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(ai_settings.music_volume)
    pygame.mixer.music.play(-1)  # Loop music indefinitely

    bg_image_path = os.path.join(base_path, 'images', 'manHinhCho.bmp')
    bg_image = pygame.image.load(bg_image_path).convert()
    
    # Get original image dimensions
    orig_width, orig_height = bg_image.get_size()
    # Calculate scaling factor to match screen width
    scale_factor = ai_settings.screen_width / orig_width
    # Calculate new height to maintain aspect ratio
    new_height = int(orig_height * scale_factor)
    # Smoothly scale image to match screen width
    bg_image = pygame.transform.smoothscale(bg_image, (ai_settings.screen_width, new_height))
    
    # Calculate vertical position to center image
    bg_rect = bg_image.get_rect()
    if new_height >= ai_settings.screen_height:
        # If image is taller than screen, align top or crop
        bg_rect.top = 0
    else:
        # If image is shorter, center vertically
        bg_rect.centery = ai_settings.screen_height // 2

    # Create buttons with adjusted spacing
    play_button = Button(ai_settings, screen, "Chơi mới", y_offset=-30) 
    continue_button = Button(ai_settings, screen, "Chơi tiếp", y_offset=40)
    start_button = Button(ai_settings, screen, "Chơi game")

    stats = GameStats(ai_settings)
    # Start with waiting screen
    stats.game_active = False
    stats.menu_active = True
    pygame.mouse.set_visible(True)
    sb = Scoreboard(ai_settings, screen, stats)

    ship = Ship(ai_settings, screen)
    bullets = Group()
    alien_bullets = Group()
    aliens = Group()
    explosions = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:
        if stats.menu_active:
            gf.check_events_menu(ai_settings, screen, stats, sb, ship, aliens, bullets,
                                 play_button, continue_button, start_button)
            # Draw waiting screen with background color for empty areas
            screen.fill((50, 50, 50))  # Dark gray for contrast
            screen.blit(bg_image, bg_rect)
            # Optional: Add semi-transparent overlay for readability
            overlay = pygame.Surface((ai_settings.screen_width, ai_settings.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 50))  # Semi-transparent black
            screen.blit(overlay, (0, 0))
            if stats.score == 0 and stats.ships_left == ai_settings.ship_limit and stats.level == 1:
                # Show "Chơi game" button on initial menu
                start_button.draw_button()
            else:
                # Show "Chơi mới" and "Chơi tiếp" after ESC or game over
                play_button.draw_button()
                continue_button.draw_button()
            pygame.display.flip()
            continue

        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions, alien_bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, explosions, alien_bullets)

run_game()