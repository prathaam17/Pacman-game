import pygame
import random
from collections import deque
from settings import WIDTH, CHAR_SIZE, GHOST_SPEED
from asset_manager import AssetManager

class Ghost(pygame.sprite.Sprite):
    def __init__(self, row, col, color_name):
        super().__init__()
        self.abs_x = (row * CHAR_SIZE)
        self.abs_y = (col * CHAR_SIZE)
        self.color_name = color_name

        self.rect = pygame.Rect(self.abs_x, self.abs_y, CHAR_SIZE, CHAR_SIZE)
        self.move_speed = GHOST_SPEED
        self.moving_dir = "up"
        self.direction = (0, -1)

        self.img_path = f'assets/ghosts/{color_name}/'
        self.image = AssetManager.get_image(f'{self.img_path}up.png', (CHAR_SIZE, CHAR_SIZE))
        self.rect = self.image.get_rect(topleft=(self.abs_x, self.abs_y))

        self.is_frightened = False
        self.frightened_timer = 0

        self.directions = {
            'left': (-self.move_speed, 0),
            'right': (self.move_speed, 0),
            'up': (0, -self.move_speed),
            'down': (0, self.move_speed)
        }
        self.dir_names = {
            (-self.move_speed, 0): 'left',
            (self.move_speed, 0): 'right',
            (0, -self.move_speed): 'up',
            (0, self.move_speed): 'down'
        }

    def move_to_start_pos(self):
        self.rect.x = self.abs_x
        self.rect.y = self.abs_y
        self.direction = (0, -1)
        self.moving_dir = "up"
        self.is_frightened = False

    def is_collide(self, dx, dy, walls_collide_list):
        tmp_rect = self.rect.move(dx, dy)
        return tmp_rect.collidelist(walls_collide_list) != -1

    def set_frightened(self, duration=150):
        self.is_frightened = True
        self.frightened_timer = duration

    def _animate(self):
        if self.is_frightened:
            # Render scared ghost blue/white
            surf = pygame.Surface((CHAR_SIZE, CHAR_SIZE))
            color = (0, 0, 255) if (self.frightened_timer > 30 or self.frightened_timer % 6 < 3) else (255, 255, 255)
            surf.fill(color)
            pygame.draw.circle(surf, (255, 255, 255), (10, 12), 4)
            pygame.draw.circle(surf, (255, 255, 255), (22, 12), 4)
            pygame.draw.circle(surf, (0, 0, 0), (10, 12), 2)
            pygame.draw.circle(surf, (0, 0, 0), (22, 12), 2)
            self.image = surf
        else:
            img = AssetManager.get_image(f'{self.img_path}{self.moving_dir}.png', (CHAR_SIZE, CHAR_SIZE))
            self.image = img

    def _calculate_target(self, pac_rect, pac_dir, red_ghost_rect):
        pac_x, pac_y = pac_rect.x, pac_rect.y
        p_dx, p_dy = pac_dir

        if self.color_name == "red":
            # Blinky: Directly targets Pac-Man
            return (pac_x, pac_y)

        elif self.color_name == "pink":
            # Pinky: Targets 4 tiles ahead of Pac-Man
            return (pac_x + p_dx * 4 * CHAR_SIZE, pac_y + p_dy * 4 * CHAR_SIZE)

        elif self.color_name == "skyblue":
            # Inky: Flank vector based on Blinky & Pac-Man
            rx = red_ghost_rect.x if red_ghost_rect else pac_x
            ry = red_ghost_rect.y if red_ghost_rect else pac_y
            target_x = pac_x + (pac_x - rx)
            target_y = pac_y + (pac_y - ry)
            return (target_x, target_y)

        elif self.color_name == "orange":
            # Clyde: Chases if far (>8 tiles), otherwise retreats to corner
            dist_sq = (self.rect.x - pac_x)**2 + (self.rect.y - pac_y)**2
            if dist_sq > (8 * CHAR_SIZE)**2:
                return (pac_x, pac_y)
            else:
                return (0, 600)

        return (pac_x, pac_y)

    def _select_best_move(self, available_keys, target_pos, walls_collide_list):
        tx, ty = target_pos
        best_key = None
        min_dist = float('inf')

        opposite = {
            'left': 'right', 'right': 'left',
            'up': 'down', 'down': 'up'
        }
        current_opp = opposite.get(self.moving_dir, '')

        # Filter out 180-degree turn unless it's the only option
        valid_keys = [k for k in available_keys if k != current_opp]
        if not valid_keys:
            valid_keys = available_keys

        for key in valid_keys:
            dx, dy = self.directions[key]
            next_x = self.rect.x + dx
            next_y = self.rect.y + dy
            dist = (next_x - tx)**2 + (next_y - ty)**2
            if dist < min_dist:
                min_dist = dist
                best_key = key

        return best_key if best_key else random.choice(available_keys)

    def update(self, walls_collide_list, pac_rect=None, pac_dir=(0,0), red_ghost_rect=None):
        if self.is_frightened:
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.is_frightened = False

        available_moves = []
        for key, move in self.directions.items():
            if not self.is_collide(*move, walls_collide_list):
                available_moves.append(key)

        if available_moves:
            # Alignment check to only change direction when snapped near tile grid
            if self.rect.x % CHAR_SIZE == 0 and self.rect.y % CHAR_SIZE == 0:
                if self.is_frightened:
                    self.moving_dir = random.choice(available_moves)
                elif pac_rect:
                    target_pos = self.calculate_target_pos(pac_rect, pac_dir, red_ghost_rect)
                    self.moving_dir = self._select_best_move(available_moves, target_pos, walls_collide_list)
                else:
                    self.moving_dir = random.choice(available_moves)

                self.direction = self.directions[self.moving_dir]

        speed_factor = 0.5 if self.is_frightened else 1.0
        actual_move = (int(self.direction[0] * speed_factor), int(self.direction[1] * speed_factor))

        if not self.is_collide(*actual_move, walls_collide_list):
            self.rect.move_ip(actual_move)

        # Teleport sides
        if self.rect.right <= 0:
            self.rect.x = WIDTH
        elif self.rect.left >= WIDTH:
            self.rect.x = 0

        self._animate()

    def calculate_target_pos(self, pac_rect, pac_dir, red_ghost_rect):
        return self._calculate_target(pac_rect, pac_dir, red_ghost_rect)
