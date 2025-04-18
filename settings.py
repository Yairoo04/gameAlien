import pygame
class Settings:
    def __init__(self):
        # Tự động lấy kích thước màn hình
        pygame.init()
        info = pygame.display.Info()
        screen_w = info.current_w
        screen_h = info.current_h

        # Dùng 90% kích thước màn hình để tránh tràn viền
        self.screen_width = int(screen_w * 0.9)
        self.screen_height = int(screen_h * 0.9)

          # Màu nền
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 3
        # Ship settings
        self.ship_limit = 3
        self.ship_speed_factor = 1.5  # Normal speed for level 1

        # Player bullet settings
        self.bullets_allowed = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_speed_factor = 3  # Normal speed for level 1

        # Alien settings
        self.alien_speed_factor = 0.5  # Normal speed for level 1
        self.fleet_drop_speed = 5
        self.fleet_direction = 1
        self.alien_points = 50  # Fixed points, no scaling
        self.music_volume = 0.5
        self.base_alien_rows = 2  # Fewer rows for level 1
        self.base_aliens_x = 5  # Fewer aliens per row for level 1
        self.alien_scale = 1.1  # Increase aliens by 10% per level

        # Alien bullet settings
        self.alien_bullet_width = 3
        self.alien_bullet_height = 15
        self.alien_bullet_color = (255, 0, 0)  # Red for visibility
        self.alien_bullet_speed_factor = 1.0  # Very slow bullets
        self.alien_bullets_max = 3  # Maximum alien bullets on screen
        self.alien_shoot_probability = 0.0002  # Very low for less frequent shooting

        # Dynamic settings for speed increase
        self.speedup_scale = 1.01  # 1% speed increase per level

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.5
        self.fleet_direction = 1
        self.alien_shoot_probability = 0.0002  # Fixed probability

    def increase_speed(self):
        """Increase speed of game elements for the next level."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        # No scaling for alien_shoot_probability or alien_points