import os
import random
import pygame
from Bullet import Bullet
from Setting import GRAVITY, SCREEN_HEIGHT, SCREEN_WIDTH, SCROLL_THRESH, TILE_SIZE, shot_fx


class Soldier(pygame.sprite.Sprite):
    """Lớp cốt lõi quản lý thông số, vật lý và AI của Player/Enemy."""

    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        super().__init__()
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.shoot_cooldown = 0
        self.grenades = grenades
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # Biến cấu hình AI
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

        # Nạp hoạt ảnh
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'img/Character/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/Character/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right, world, water_group, bg_scroll, enemy_group=None):
        screen_scroll = 0
        dx = 0
        dy = 0

        # Áp dụng gia tốc
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # Nhảy
        if self.jump and not self.in_air:
            self.vel_y = -14
            self.jump = False
            self.in_air = True

        # Trọng lực
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Va chạm địa hình
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # Rớt xuống nước / Vực
        if pygame.sprite.spritecollide(self, water_group, False) or self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        level_complete = False

        # Bức tường vô hình chặn người chơi ở mép màn hình
        if self.char_type != 'enemy':
            if self.rect.left + dx < 0:
                dx = -self.rect.left
            if self.rect.right + dx > SCREEN_WIDTH:
                dx = SCREEN_WIDTH - self.rect.right

        self.rect.x += dx
        self.rect.y += dy

        # Cuộn camera khi vượt ngưỡng màn hình
        if self.char_type != 'enemy':
            if self.rect.right > SCREEN_WIDTH - SCROLL_THRESH:
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def shoot(self, bullet_group):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery,
                            self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1
            shot_fx.play()

    def ai(self, player, world, water_group, screen_scroll, bg_scroll, bullet_group):
        if self.alive and player.alive:
            # Ngẫu nhiên dừng lại để Idle
            if not self.idling and random.randint(1, 200) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50

            # AI phát hiện người chơi
            if self.vision.colliderect(player.rect):
                self.update_action(0)
                self.shoot(bullet_group)
            else:
                if not self.idling:
                    ai_moving_right = (self.direction == 1)
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right, world, water_group, bg_scroll)
                    self.update_action(1)
                    self.move_counter += 1

                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        self.rect.x += screen_scroll

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:  # Nếu là animation Death thì xóa nhân vật
                self.frame_index = len(self.animation_list[self.action]) - 1
                self.kill()
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw_hp_ai(self, screen):
        dx = self.rect.x - 10
        dy = self.rect.y - 20
        pygame.draw.rect(screen, (0, 0, 0), (dx, dy, 70, 15), 2)
        pygame.draw.rect(screen, (255, 0, 0), (dx, dy, 70 * self.health // 100, 15))

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        if self.char_type == 'enemy':
            self.draw_hp_ai(screen)