import pygame

class Button():
    """Nút bấm UI render từ text và mã màu."""
    def __init__(self, x, y, text, font, text_col, bg_col, hover_col, width, height):
        self.text = text
        self.font = font
        self.text_col = text_col
        self.bg_col = bg_col
        self.hover_col = hover_col
        self.rect = pygame.Rect(x, y, width, height)
        self.shadow_rect = pygame.Rect(x + 4, y + 4, width, height)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        current_col = self.bg_col

        if self.rect.collidepoint(pos):
            current_col = self.hover_col
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        pygame.draw.rect(surface, (0, 0, 0), self.shadow_rect)
        pygame.draw.rect(surface, current_col, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 3)

        text_img = self.font.render(self.text, True, self.text_col)
        text_rect = text_img.get_rect(center=self.rect.center)
        surface.blit(text_img, text_rect)

        return action


class ImageButton():
    """Nút bấm UI render từ hình ảnh."""
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action