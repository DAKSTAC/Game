import pygame
from Setting import TILE_SIZE

class Water(pygame.sprite.Sprite):
    """Block môi trường lava, kết liễu khi va chạm"""
    def __init__(self, img, x, y):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self, screen_scroll):
        self.rect.x += screen_scroll