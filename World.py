import random
import pygame
from Decoration import Decoration
from HealthBar import HealthBar
from ItemBox import ItemBox
from Setting import TILE_SIZE, img_list, ROWS, COLS, SCREEN_WIDTH
from Soldier import Soldier
from Water import Water
from Patterns import ALL_PATTERNS


class World():
    """Trình tạo thế giới Endless sử dụng cơ chế Auto-tiling ngẫu nhiên."""
    def __init__(self):
        self.obstacle_list = []
        self.generated_columns = 0
        self.ground_level = ROWS - 5

    def create_start_zone(self, water_group, decoration_group, enemy_group, item_box_group, main_Character):
        # Render đoạn đường an toàn ban đầu
        for x in range(COLS + 2):
            world_x = x * TILE_SIZE
            for y in range(self.ground_level, ROWS):
                if y == self.ground_level:
                    self._add_tile(0, world_x, y * TILE_SIZE)
                    if random.randint(1, 10) <= 3:
                        dec_img = img_list[random.choice([4, 5, 6])]
                        decoration = Decoration(dec_img, world_x, (y - 1) * TILE_SIZE)
                        decoration_group.add(decoration)
                else:
                    self._add_tile(1, world_x, y * TILE_SIZE)
            self.generated_columns += 1

        start_x = 100
        start_y = (self.ground_level - 2) * TILE_SIZE
        player = Soldier(main_Character, start_x, start_y, 1.65, 6, 20, 5)
        health_bar = HealthBar(10, 10, player.health, player.health)

        return player, health_bar

    def spawn_pattern(self, pattern, water_group, decoration_group, enemy_group, item_box_group, bg_scroll):
        pattern_width = len(pattern[0])

        for col in range(pattern_width):
            world_x = self.generated_columns * TILE_SIZE
            screen_x = world_x - bg_scroll

            for row in range(ROWS):
                char = pattern[row][col]
                y = row * TILE_SIZE

                if char == 'G':
                    if row > 0 and pattern[row - 1][col] not in ['G', 'W']:
                        self._add_tile(0, screen_x, y)
                        if random.randint(1, 10) <= 2:
                            dec_img = img_list[random.choice([4, 5, 6])]
                            decoration = Decoration(dec_img, screen_x, y - TILE_SIZE)
                            decoration_group.add(decoration)
                    else:
                        self._add_tile(1, screen_x, y)

                elif char == 'W':
                    if row > 0 and pattern[row - 1][col] != 'W':
                        water = Water(img_list[2], screen_x, y)
                    else:
                        water = Water(img_list[3], screen_x, y)
                    water_group.add(water)

                elif char == 'P':
                    dec_img = img_list[random.choice([4, 5, 6])]
                    decoration = Decoration(dec_img, screen_x, y)
                    decoration_group.add(decoration)
                elif char == 'E':
                    enemy = Soldier('enemy', screen_x, y, 1.65, 2, 20, 0)
                    enemy_group.add(enemy)
                elif char == 'A':
                    item_box = ItemBox('Ammo', screen_x, y)
                    item_box_group.add(item_box)
                elif char == 'H':
                    item_box = ItemBox('Health', screen_x, y)
                    item_box_group.add(item_box)
                elif char == 'B':
                    item_box = ItemBox('Grenade', screen_x, y)
                    item_box_group.add(item_box)

            self.generated_columns += 1

    def _add_tile(self, tile_index, x, y):
        try:
            img = img_list[tile_index]
            img_rect = img.get_rect(topleft=(x, y))
            self.obstacle_list.append([img, img_rect])
        except IndexError:
            pass

    def update_endless(self, bg_scroll, water_group, decoration_group, enemy_group, item_box_group):
        right_edge_world_x = bg_scroll + SCREEN_WIDTH + TILE_SIZE * 2

        # Liên tục sinh địa hình nếu nhân vật tiến về phía trước
        while (self.generated_columns * TILE_SIZE) < right_edge_world_x:
            chosen_pattern = random.choice(ALL_PATTERNS)
            self.spawn_pattern(chosen_pattern, water_group, decoration_group,
                               enemy_group, item_box_group, bg_scroll)

    def draw(self, screen, screen_scroll):
        for tile in self.obstacle_list[:]:
            tile[1][0] += screen_scroll
            if tile[1].right < 0:
                self.obstacle_list.remove(tile)
            else:
                screen.blit(tile[0], tile[1])