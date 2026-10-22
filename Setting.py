import pygame
import os

pygame.mixer.init()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('The Game')
iconimg = pygame.image.load("img/icons/icongame.png")
pygame.display.set_icon(iconimg)

# Cấu hình khung hình
clock = pygame.time.Clock()
FPS = 60

# Thông số vật lý và bản đồ
GRAVITY = 0.75
SCROLL_THRESH = SCREEN_WIDTH // 2
ROWS = 16
TILE_SIZE = SCREEN_HEIGHT // ROWS
COLS = SCREEN_WIDTH // TILE_SIZE
TILE_TYPES = 7  # 7 loại block (0 đến 6)

# Trạng thái game
screen_scroll = 0
bg_scroll = 0
start_game = False
chse_player = False
start_intro = False
main_Character = 'player'

# Hệ thống điểm số
score = 0
high_score = 0
if os.path.exists('highscore.txt'):
    with open('highscore.txt', 'r') as file:
        try:
            high_score = int(file.read())
        except:
            high_score = 0

# Trạng thái người chơi
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

# Âm thanh
is_playing_msc = True
pygame.mixer.music.load('audio/music2.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)

jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.05)
shot_fx = pygame.mixer.Sound('audio/shot.wav')
shot_fx.set_volume(0.05)
grenade_fx = pygame.mixer.Sound('audio/grenade.wav')
grenade_fx.set_volume(0.05)

# Tải tài nguyên hình ảnh UI
loa_img = pygame.transform.scale(pygame.image.load('img/loa.png').convert_alpha(), (50, 50))
frog_icon = pygame.image.load('img/Character/icon/frog_icon.png').convert_alpha()
guy_icon = pygame.image.load('img/Character/icon/guy_icon.png').convert_alpha()
mask_icon = pygame.image.load('img/Character/icon/mask_icon.png').convert_alpha()
player_icon = pygame.image.load('img/Character/icon/player_icon.png').convert_alpha()

# Tải hình nền cuộn
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

# Tải danh sách block địa hình
img_list = []
for x in range(TILE_TYPES):
    img = pygame.transform.scale(pygame.image.load(f'img/Tile/{x}.png'), (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

# Vũ khí & Vật phẩm
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()

health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
item_boxes = {
    'Health': health_box_img,
    'Ammo': ammo_box_img,
    'Grenade': grenade_box_img
}

# Bảng màu chuẩn
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)


def draw_text(text, font, text_col, x, y):
    """Hàm phụ trợ vẽ văn bản ra màn hình."""
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg():
    """Vẽ phông nền cuộn song song nhiều lớp."""
    screen.fill(BG)
    width = sky_img.get_width()
    for x in range(4):
        screen.blit(sky_img, ((x * width) - (bg_scroll * 0.5) % width, 0))
        screen.blit(mountain_img, ((x * width) - (bg_scroll * 0.6) % width, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - (bg_scroll * 0.7) % width, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - (bg_scroll * 0.8) % width, SCREEN_HEIGHT - pine2_img.get_height()))