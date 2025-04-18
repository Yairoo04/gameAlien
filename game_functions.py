import sys
from time import sleep
import pygame
from pygame.sprite import groupcollide
from bullet import Bullet, AlienBullet
from alien import Alien
from explosion import Explosion

def check_keydown_events(event, ai_settings, screen, stats, ship, bullets):
    """Xử lý sự kiện nhấn phím"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_ESCAPE:
        stats.game_active = False
        stats.menu_active = True
        pygame.mouse.set_visible(True)

def check_keyup_events(event, ship):
    """Xử lý khi nhả phím"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets):
    """Xử lý các sự kiện trong trò chơi"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)

def check_events_menu(ai_settings, screen, stats, sb, ship, aliens, bullets,
                      play_button, continue_button, start_button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if start_button.rect.collidepoint(mouse_x, mouse_y) and stats.score == 0 and stats.ships_left == ai_settings.ship_limit:
                start_new_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
            elif play_button.rect.collidepoint(mouse_x, mouse_y):
                start_new_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
            elif continue_button.rect.collidepoint(mouse_x, mouse_y):
                resume_game(stats)

def resume_game(stats):
    """Tiếp tục trò chơi đang dở"""
    stats.game_active = True
    stats.menu_active = False
    pygame.mouse.set_visible(False)

def start_new_game(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets=None):
    """Bắt đầu trò chơi mới hoàn toàn"""
    ai_settings.initialize_dynamic_settings()
    stats.reset_stats()
    stats.high_score = 0  # Reset high score for new game
    stats.game_active = True
    stats.menu_active = False
    pygame.mouse.set_visible(False)

    aliens.empty()
    bullets.empty()
    if alien_bullets is not None:
        alien_bullets.empty()

    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

def check_play_button(ai_settings, screen, stats, sb, play_button,
                      ship, aliens, bullets, mouse_x, mouse_y):
    """Xử lý nút Play trong trường hợp không có menu"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_new_game(ai_settings, screen, stats, sb, ship, aliens, bullets)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Bắn đạn nếu chưa quá giới hạn"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, explosions, alien_bullets):
    """Cập nhật màn hình trò chơi"""
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for alien_bullet in alien_bullets.sprites():
        alien_bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    update_explosions(explosions)
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions, alien_bullets):
    """Cập nhật vị trí đạn và xử lý va chạm"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    alien_bullets.update()
    for bullet in alien_bullets.copy():
        if bullet.rect.top >= ai_settings.screen_height:
            bullet.kill()

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions)
    check_alien_bullet_ship_collisions(ai_settings, screen, stats, sb, ship, aliens, alien_bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions):
    """Xử lý va chạm giữa đạn và alien"""
    collisions = groupcollide(bullets, aliens, True, True)
    if collisions:
        for hit_aliens in collisions.values():
            for alien in hit_aliens:
                explosion = Explosion(ai_settings, screen, alien.rect.center)
                explosions.add(explosion)
            stats.score += ai_settings.alien_points * len(hit_aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        stats.level += 1
        sb.prep_level()
        ai_settings.increase_speed()  # Increase speed when level changes
        create_fleet(ai_settings, screen, ship, aliens)

def check_alien_bullet_ship_collisions(ai_settings, screen, stats, sb, ship, aliens, alien_bullets):
    """Xử lý va chạm giữa đạn alien và tàu người chơi"""
    if pygame.sprite.spritecollideany(ship, alien_bullets):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, alien_bullets)

def update_explosions(explosions):
    """Cập nhật hiệu ứng nổ"""
    explosions.update()
    for explosion in explosions:
        explosion.draw()

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Xử lý khi tàu bị va chạm"""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
    else:
        stats.game_active = False
        stats.menu_active = True
        pygame.mouse.set_visible(True)

    aliens.empty()
    bullets.empty()
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    sleep(0.5)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
    """Cập nhật vị trí của tất cả aliens trong hạm đội"""
    check_fleet_edges(ai_settings, aliens)
    # Track front-row aliens by column (using centerx for precision)
    front_row_alien_rows = {}
    for alien in aliens:
        column_key = alien.rect.centerx // 50  # Finer column grouping
        current_row = front_row_alien_rows.get(column_key, float('inf'))
        front_row_alien_rows[column_key] = min(current_row, alien.row)
    
    # Chỉ cập nhật vị trí của aliens
    aliens.update()
    
    # Xử lý riêng việc bắn đạn từ alien
    handle_alien_shooting(ai_settings, screen, aliens, alien_bullets, front_row_alien_rows)

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def handle_alien_shooting(ai_settings, screen, aliens, alien_bullets, front_row_alien_rows):
    """Xử lý việc alien bắn đạn dựa trên front_row_alien_rows"""
    import random
    
    # Giới hạn số lượng đạn alien trên màn hình
    if len(alien_bullets) >= ai_settings.alien_bullets_max:
        return
    
    # Duyệt qua các alien để tìm những alien ở hàng đầu tiên của mỗi cột
    for alien in aliens:
        column_key = alien.rect.centerx // 50
        if alien.row == front_row_alien_rows.get(column_key, float('inf')):
            # Xác suất bắn dựa trên alien_shoot_probability
            if random.random() < ai_settings.alien_shoot_probability:
                new_bullet = AlienBullet(ai_settings, screen, alien)
                alien_bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen, row=row_number)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)