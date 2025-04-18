class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Bắt đầu ở trạng thái menu
        self.game_active = False
        self.menu_active = True

        # High score không bị reset
        self.high_score = 0

    def reset_stats(self):
        """Đặt lại các chỉ số có thể thay đổi khi chơi."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
