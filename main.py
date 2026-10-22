import pygame
from pygame import mixer
import Button
import os
from Setting import *
from Bullet import Bullet
from Decoration import Decoration
from Explosion import Explosion
from Grenade import Grenade
from HealthBar import HealthBar
from ItemBox import ItemBox
from ScreenFade import ScreenFade
from Soldier import Soldier
from Water import Water
from World import World

mixer.init()
pygame.init()


def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()


# ==========================================
# BẢNG MÀU UI (RETRO ARCADE THEME)
# ==========================================
PANEL_BG = (25, 35, 50)
CARD_BG = (35, 50, 70)
PANEL_BORDER = (255, 204, 0)
BTN_NORMAL = (45, 70, 100)
BTN_HOVER = (230, 95, 45)
GOLD_TEXT = (255, 215, 0)

# ==========================================
# KHỞI TẠO ĐỒNG BỘ FONT
# ==========================================
FONT_PATH = 'PressStart2P-Regular.ttf'
title_font = pygame.font.Font(FONT_PATH, 26)
pixel_font = pygame.font.Font(FONT_PATH, 16)
hud_font = pygame.font.Font(FONT_PATH, 14)
small_pixel_font = pygame.font.Font(FONT_PATH, 11)


def draw_text_centered_at(text, font_use, text_col, center_x, center_y):
    shadow_img = font_use.render(text, True, BLACK)
    shadow_rect = shadow_img.get_rect(center=(center_x + 2, center_y + 2))
    screen.blit(shadow_img, shadow_rect)
    img = font_use.render(text, True, text_col)
    rect = img.get_rect(center=(center_x, center_y))
    screen.blit(img, rect)


def draw_text_center(text, font_use, text_col, y):
    draw_text_centered_at(text, font_use, text_col, SCREEN_WIDTH // 2, y)


def draw_panel(x, y, width, height, bg_color=PANEL_BG, border_color=PANEL_BORDER):
    shadow_rect = pygame.Rect(x + 6, y + 6, width, height)
    panel_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, (0, 0, 0), shadow_rect)
    pygame.draw.rect(screen, bg_color, panel_rect)
    pygame.draw.rect(screen, border_color, panel_rect, 4)


intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)

# ==========================================
# KHỞI TẠO CÁC NÚT BẤM UI
# ==========================================
BTN_MAIN_W = 300
BTN_MAIN_H = 55
start_button = Button.Button(SCREEN_WIDTH // 2 - BTN_MAIN_W // 2, SCREEN_HEIGHT // 2 - 100, "START GAME", pixel_font, WHITE, BTN_NORMAL, BTN_HOVER, BTN_MAIN_W, BTN_MAIN_H)
choose_player = Button.Button(SCREEN_WIDTH // 2 - BTN_MAIN_W // 2, SCREEN_HEIGHT // 2 - 30, "CHOOSE PLAYER", pixel_font, WHITE, BTN_NORMAL, BTN_HOVER, BTN_MAIN_W, BTN_MAIN_H)
tutorial_button = Button.Button(SCREEN_WIDTH // 2 - BTN_MAIN_W // 2, SCREEN_HEIGHT // 2 + 40, "TUTORIAL", pixel_font, WHITE, BTN_NORMAL, BTN_HOVER, BTN_MAIN_W, BTN_MAIN_H)
exit_button = Button.Button(SCREEN_WIDTH // 2 - BTN_MAIN_W // 2, SCREEN_HEIGHT // 2 + 110, "EXIT", pixel_font, WHITE, BTN_NORMAL, BTN_HOVER, BTN_MAIN_W, BTN_MAIN_H)

loa_menu_btn = Button.ImageButton(SCREEN_WIDTH - 70, 20, loa_img, 1)

PAUSE_W, PAUSE_H = 380, 340
PAUSE_X = SCREEN_WIDTH // 2 - PAUSE_W // 2
PAUSE_Y = SCREEN_HEIGHT // 2 - PAUSE_H // 2
BTN_SUB_W = 250
BTN_SUB_H = 50

resume_button = Button.Button(SCREEN_WIDTH // 2 - BTN_SUB_W // 2, PAUSE_Y + 95, "RESUME", pixel_font, WHITE, BTN_NORMAL, BTN_HOVER, BTN_SUB_W, BTN_SUB_H)
restart_button = Button.Button(SCREEN_WIDTH // 2 - BTN_SUB_W // 2, PAUSE_Y + 165, "RESTART", pixel_font, WHITE, BTN_NORMAL, BTN_HOVER, BTN_SUB_W, BTN_SUB_H)
menu_button = Button.Button(SCREEN_WIDTH // 2 - BTN_SUB_W // 2, PAUSE_Y + 235, "MAIN MENU", pixel_font, WHITE, BTN_NORMAL, BTN_HOVER, BTN_SUB_W, BTN_SUB_H)

loa_pause_btn = Button.ImageButton(PAUSE_X + PAUSE_W - 55, PAUSE_Y + 15, loa_img, 0.8)

GO_W, GO_H = 420, 360
GO_X = SCREEN_WIDTH // 2 - GO_W // 2
GO_Y = SCREEN_HEIGHT // 2 - GO_H // 2

go_restart_btn = Button.Button(SCREEN_WIDTH // 2 - BTN_SUB_W // 2, GO_Y + 200, "PLAY AGAIN", pixel_font, WHITE, BTN_NORMAL, BTN_HOVER, BTN_SUB_W, BTN_SUB_H)
go_menu_btn = Button.Button(SCREEN_WIDTH // 2 - BTN_SUB_W // 2, GO_Y + 270, "MAIN MENU", pixel_font, WHITE, BTN_NORMAL, BTN_HOVER, BTN_SUB_W, BTN_SUB_H)

COL1_X = SCREEN_WIDTH // 2 - 165
COL2_X = SCREEN_WIDTH // 2 + 165
ROW1_Y = SCREEN_HEIGHT // 2 - 75
ROW2_Y = SCREEN_HEIGHT // 2 + 105

back_btn = Button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 65, "BACK", pixel_font, WHITE, BTN_NORMAL, BTN_HOVER, 200, 45)

show_tutorial = False
kill_score = 0
game_paused = False

enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()

world = World()
player, health_bar = world.create_start_zone(water_group, decoration_group, enemy_group, item_box_group, main_Character)


def choose_maincr():
    global chse_player, player, main_Character, world, health_bar, bg_scroll, kill_score
    draw_bg()

    draw_panel(SCREEN_WIDTH // 2 - 350, 35, 700, SCREEN_HEIGHT - 70)
    draw_text_center("CHOOSE CHARACTER", title_font, GOLD_TEXT, 80)
    pygame.draw.line(screen, PANEL_BORDER, (SCREEN_WIDTH // 2 - 280, 110), (SCREEN_WIDTH // 2 + 280, 110), 3)

    CARD_W, CARD_H = 290, 150
    cards = [
        (COL1_X, ROW1_Y, 'player', "SIEU NHAN CUONG PHONG", player_icon),
        (COL2_X, ROW1_Y, 'VirtualGuy', "SHIN CAU BE BUT CHI", guy_icon),
        (COL1_X, ROW2_Y, 'NinjaFrog', "CHU ECH NHI NHANH", frog_icon),
        (COL2_X, ROW2_Y, 'MaskDude', "THO DAN THAN THIEN", mask_icon)
    ]

    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]
    selected = False

    for cx, cy, char_code, char_name, icon_img in cards:
        card_rect = pygame.Rect(cx - CARD_W // 2, cy - CARD_H // 2, CARD_W, CARD_H)
        is_hovered = card_rect.collidepoint(mouse_pos)

        if main_Character == char_code or is_hovered:
            border_col = GREEN
            text_col = GOLD_TEXT
        else:
            border_col = WHITE
            text_col = WHITE

        pygame.draw.rect(screen, CARD_BG, card_rect)
        pygame.draw.rect(screen, border_col, card_rect, 3)

        scaled_icon = pygame.transform.scale(icon_img, (int(icon_img.get_width() * 2), int(icon_img.get_height() * 2)))
        icon_rect = scaled_icon.get_rect(center=(cx, cy - 15))
        screen.blit(scaled_icon, icon_rect)
        draw_text_centered_at(char_name, small_pixel_font, text_col, cx, cy + 48)

        if is_hovered and mouse_clicked:
            main_Character = char_code
            selected = True

    if back_btn.draw(screen):
        pygame.time.delay(200)
        pygame.event.clear()
        chse_player = False

    if selected:
        pygame.time.delay(200)
        pygame.event.clear()
        reset_level()
        bg_scroll = 0
        kill_score = 0
        world = World()
        player, health_bar = world.create_start_zone(water_group, decoration_group, enemy_group, item_box_group, main_Character)
        chse_player = False


def show_tutorial_screen():
    global show_tutorial
    draw_bg()

    draw_panel(SCREEN_WIDTH // 2 - 350, 40, 700, SCREEN_HEIGHT - 80)
    draw_text_center("HOW TO PLAY", title_font, GOLD_TEXT, 90)
    pygame.draw.line(screen, PANEL_BORDER, (SCREEN_WIDTH // 2 - 280, 125), (SCREEN_WIDTH // 2 + 280, 125), 3)

    draw_text_centered_at("--- CONTROLS ---", pixel_font, RED, SCREEN_WIDTH // 2, 170)
    draw_text_centered_at("A/D or LEFT/RIGHT: Move", hud_font, WHITE, SCREEN_WIDTH // 2, 215)
    draw_text_centered_at("W or UP: Jump", hud_font, WHITE, SCREEN_WIDTH // 2, 250)
    draw_text_centered_at("SPACE: Shoot", hud_font, WHITE, SCREEN_WIDTH // 2, 285)
    draw_text_centered_at("S or DOWN: Throw Grenade", hud_font, WHITE, SCREEN_WIDTH // 2, 320)

    draw_text_centered_at("--- OBJECTIVES ---", pixel_font, RED, SCREEN_WIDTH // 2, 380)
    draw_text_centered_at("Run forward to survive and gain points.", hud_font, GOLD_TEXT, SCREEN_WIDTH // 2, 425)
    draw_text_centered_at("Kill enemies to get Extra Points!", hud_font, GREEN, SCREEN_WIDTH // 2, 460)

    if back_btn.draw(screen):
        pygame.time.delay(200)
        pygame.event.clear()
        show_tutorial = False


overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
overlay.set_alpha(150)
overlay.fill((0, 0, 0))

run = True
while run:
    clock.tick(FPS)

    if chse_player:
        choose_maincr()

    elif show_tutorial:
        show_tutorial_screen()

    elif not start_game:
        draw_bg()
        draw_panel(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 210, 400, 420)
        draw_text_center("THE GAME", title_font, GOLD_TEXT, SCREEN_HEIGHT // 2 - 160)

        if start_button.draw(screen):
            pygame.time.delay(150)
            pygame.event.clear()
            start_game = True
            start_intro = True
            game_paused = False
            kill_score = 0
        if choose_player.draw(screen):
            pygame.time.delay(200)
            pygame.event.clear()
            chse_player = True
        if tutorial_button.draw(screen):
            pygame.time.delay(200)
            pygame.event.clear()
            show_tutorial = True
        if exit_button.draw(screen):
            run = False

        if loa_menu_btn.draw(screen):
            if is_playing_msc:
                pygame.mixer.music.stop()
                is_playing_msc = False
            else:
                pygame.mixer.music.play(-1, 0.0, 5000)
                is_playing_msc = True
        if not is_playing_msc:
            pygame.draw.line(screen, RED, (loa_menu_btn.rect.left, loa_menu_btn.rect.top), (loa_menu_btn.rect.right, loa_menu_btn.rect.bottom), 4)

    else:
        if game_paused:
            screen_scroll = 0

        draw_bg()
        world.draw(screen, screen_scroll)
        health_bar.draw(screen, player.health)

        screen.blit(pygame.transform.scale(bullet_img, (20, 20)), (10, 35))
        draw_text(f'AMMO:{player.ammo}', hud_font, BLACK, 37, 39)
        draw_text(f'AMMO:{player.ammo}', hud_font, WHITE, 35, 37)

        screen.blit(pygame.transform.scale(grenade_img, (20, 20)), (10, 65))
        draw_text(f'GRENADES:{player.grenades}', hud_font, BLACK, 37, 69)
        draw_text(f'GRENADES:{player.grenades}', hud_font, WHITE, 35, 67)

        distance_score = bg_scroll // 10
        current_score = max(0, distance_score + kill_score)

        draw_text(f'SCORE:{current_score}', hud_font, BLACK, SCREEN_WIDTH - 228, 17)
        draw_text(f'SCORE:{current_score}', hud_font, WHITE, SCREEN_WIDTH - 230, 15)

        draw_text(f'HIGH:{high_score}', hud_font, BLACK, SCREEN_WIDTH - 228, 42)
        draw_text(f'HIGH:{high_score}', hud_font, GOLD_TEXT, SCREEN_WIDTH - 230, 40)

        player.draw(screen)
        for enemy in enemy_group:
            enemy.draw(screen)

        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)

        if start_intro:
            if intro_fade.fade(screen):
                start_intro = False
                intro_fade.fade_counter = 0

        # MENU TẠM DỪNG (ESC)
        if game_paused:
            screen.blit(overlay, (0, 0))
            draw_panel(PAUSE_X, PAUSE_Y, PAUSE_W, PAUSE_H)
            draw_text_center('PAUSED', title_font, GOLD_TEXT, PAUSE_Y + 45)

            if loa_pause_btn.draw(screen):
                if is_playing_msc:
                    pygame.mixer.music.stop()
                    is_playing_msc = False
                else:
                    pygame.mixer.music.play(-1, 0.0, 5000)
                    is_playing_msc = True
            if not is_playing_msc:
                pygame.draw.line(screen, RED, (loa_pause_btn.rect.left, loa_pause_btn.rect.top), (loa_pause_btn.rect.right, loa_pause_btn.rect.bottom), 4)

            if resume_button.draw(screen):
                game_paused = False
            if restart_button.draw(screen):
                pygame.time.delay(150)
                pygame.event.clear()
                bg_scroll = 0
                screen_scroll = 0
                kill_score = 0
                reset_level()
                world = World()
                player, health_bar = world.create_start_zone(water_group, decoration_group, enemy_group, item_box_group, main_Character)
                game_paused = False
                start_intro = True
            if menu_button.draw(screen):
                pygame.time.delay(200)
                pygame.event.clear()
                start_game = False
                game_paused = False
                bg_scroll = 0
                screen_scroll = 0
                kill_score = 0
                reset_level()
                world = World()
                player, health_bar = world.create_start_zone(water_group, decoration_group, enemy_group, item_box_group, main_Character)

        # GAME CHẠY BÌNH THƯỜNG
        elif player.alive:
            world.update_endless(bg_scroll, water_group, decoration_group, enemy_group, item_box_group)
            player.update()

            for enemy in enemy_group:
                enemy.ai(player, world, water_group, screen_scroll, bg_scroll, bullet_group)
                enemy.update()

                # Bảo vệ điểm khi quái rớt vực / Phạt điểm khi chạy trốn
                if enemy.health <= 0 and not getattr(enemy, 'scored', False):
                    enemy.scored = True
                    if not (enemy.rect.bottom >= SCREEN_HEIGHT or pygame.sprite.spritecollideany(enemy, water_group)):
                        kill_score += 50
                if enemy.rect.right < 0:
                    kill_score -= 30
                    enemy.kill()

            bullet_group.update(world, player, bullet_group, enemy_group, screen_scroll)
            grenade_group.update(world, explosion_group, player, enemy_group, screen_scroll)
            explosion_group.update(screen_scroll)
            item_box_group.update(player, screen_scroll)
            decoration_group.update(screen_scroll)
            water_group.update(screen_scroll)

            if shoot:
                player.shoot(bullet_group)
            elif grenade and not grenade_thrown and player.grenades > 0:
                grenade_instance = Grenade(
                    player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),
                    player.rect.top,
                    player.direction
                )
                grenade_group.add(grenade_instance)
                player.grenades -= 1
                grenade_thrown = True

            if player.in_air:
                player.update_action(2)
            elif moving_left or moving_right:
                player.update_action(1)
            else:
                player.update_action(0)

            screen_scroll, _ = player.move(moving_left, moving_right, world, water_group, bg_scroll, enemy_group)
            bg_scroll -= screen_scroll

        # GIAO DIỆN GAME OVER
        else:
            screen_scroll = 0
            if death_fade.fade(screen):
                screen.blit(overlay, (0, 0))

                if current_score > high_score:
                    high_score = current_score
                    with open('highscore.txt', 'w') as file:
                        file.write(str(high_score))

                draw_panel(GO_X, GO_Y, GO_W, GO_H)
                draw_text_center('GAME OVER', title_font, RED, GO_Y + 45)
                pygame.draw.line(screen, PANEL_BORDER, (GO_X + 40, GO_Y + 80), (GO_X + GO_W - 40, GO_Y + 80), 3)
                draw_text_center(f'YOUR SCORE: {current_score}', pixel_font, WHITE, GO_Y + 115)
                draw_text_center(f'HIGH SCORE: {high_score}', pixel_font, GOLD_TEXT, GO_Y + 155)

                if go_restart_btn.draw(screen):
                    pygame.time.delay(150)
                    pygame.event.clear()
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    screen_scroll = 0
                    kill_score = 0
                    reset_level()
                    world = World()
                    player, health_bar = world.create_start_zone(water_group, decoration_group, enemy_group, item_box_group, main_Character)

                if go_menu_btn.draw(screen):
                    pygame.time.delay(200)
                    pygame.event.clear()
                    death_fade.fade_counter = 0
                    start_game = False
                    bg_scroll = 0
                    screen_scroll = 0
                    kill_score = 0
                    reset_level()
                    world = World()
                    player, health_bar = world.create_start_zone(water_group, decoration_group, enemy_group, item_box_group, main_Character)

    # SỰ KIỆN BÀN PHÍM
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if not game_paused:
                if event.key in (pygame.K_LEFT, pygame.K_a): moving_left = True
                if event.key in (pygame.K_RIGHT, pygame.K_d): moving_right = True
                if event.key == pygame.K_SPACE: shoot = True
                if event.key in (pygame.K_DOWN, pygame.K_s): grenade = True
                if event.key in (pygame.K_UP, pygame.K_w) and player.alive:
                    player.jump = True
                    jump_fx.play()

            if event.key == pygame.K_ESCAPE:
                if start_game and player.alive:
                    game_paused = not game_paused
                    if game_paused:
                        moving_left = moving_right = shoot = grenade = False
                        screen_scroll = 0

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_a): moving_left = False
            if event.key in (pygame.K_RIGHT, pygame.K_d): moving_right = False
            if event.key == pygame.K_SPACE: shoot = False
            if event.key in (pygame.K_DOWN, pygame.K_s):
                grenade = False
                grenade_thrown = False

    pygame.display.update()

pygame.quit()