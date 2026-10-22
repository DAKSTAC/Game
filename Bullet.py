import pygame
from Setting import SCREEN_WIDTH, bullet_img

class Bullet(pygame.sprite.Sprite):
    """Quản lý thực thể đạn và va chạm."""
    def __init__(self, x, y, direction):
        super().__init__()
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction

    def update(self, world, player, bullet_group, enemy_group, screen_scroll):
        self.rect.x += (self.direction * self.speed) + screen_scroll

        # Hủy đạn nếu bay ra khỏi màn hình
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        # Va chạm với địa hình
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        # Va chạm với người chơi
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()

        # Va chạm với kẻ địch
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()