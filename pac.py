import pygame
from settings import CHAR_SIZE, PLAYER_SPEED
from animation import import_sprite

class Pac(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__()

        self.abs_x = (row * CHAR_SIZE)
        self.abs_y = (col * CHAR_SIZE)

        self._import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.5

        if self.animations["idle"]:
            self.image = self.animations["idle"][0]
        else:
            self.image = self._create_fallback_surface()

        self.rect = self.image.get_rect(topleft=(self.abs_x, self.abs_y))
        self.mask = pygame.mask.from_surface(self.image)

        self.pac_speed = PLAYER_SPEED
        self.immune_time = 0
        self.immune = False
        self.ghost_combo = 0

        self.directions = {
            'left': (-PLAYER_SPEED, 0),
            'right': (PLAYER_SPEED, 0),
            'up': (0, -PLAYER_SPEED),
            'down': (0, PLAYER_SPEED)
        }
        self.keys = {
            'left': [pygame.K_LEFT, pygame.K_a],
            'right': [pygame.K_RIGHT, pygame.K_d],
            'up': [pygame.K_UP, pygame.K_w],
            'down': [pygame.K_DOWN, pygame.K_s]
        }
        self.direction = (0, 0)
        self.status = "idle"
        self.life = 3
        self.pac_score = 0
        self.walls_collide_list = []

    def _create_fallback_surface(self, color=(255, 255, 0)):
        surf = pygame.Surface((CHAR_SIZE, CHAR_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (CHAR_SIZE // 2, CHAR_SIZE // 2), CHAR_SIZE // 2 - 2)
        return surf

    def _import_character_assets(self):
        character_path = "assets/pac/"
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "idle": [],
            "power_up": []
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            try:
                self.animations[animation] = import_sprite(full_path)
            except Exception:
                self.animations[animation] = []

    def _is_collide(self, x, y):
        tmp_rect = self.rect.move(x, y)
        if tmp_rect.collidelist(self.walls_collide_list) == -1:
            return False
        return True

    def move_to_start_pos(self):
        self.rect.x = self.abs_x
        self.rect.y = self.abs_y
        self.direction = (0, 0)
        self.status = "idle"

    def animate(self, pressed_key, walls_collide_list):
        self.walls_collide_list = walls_collide_list

        for key, key_codes in self.keys.items():
            if any(pressed_key[code] for code in key_codes):
                if not self._is_collide(*self.directions[key]):
                    self.direction = self.directions[key]
                    self.status = key if not self.immune else "power_up"
                    break

        if not self._is_collide(*self.direction):
            self.rect.move_ip(self.direction)
            self.status = self.status if not self.immune else "power_up"
        else:
            self.status = "idle" if not self.immune else "power_up"

        animation = self.animations.get(self.status, [])
        if animation:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0
            image = animation[int(self.frame_index)]
            self.image = pygame.transform.scale(image, (CHAR_SIZE, CHAR_SIZE))
        else:
            color = (255, 255, 0) if not self.immune else (0, 255, 255)
            self.image = self._create_fallback_surface(color)

    def update(self):
        if self.immune_time > 0:
            self.immune = True
            self.immune_time -= 1
        else:
            self.immune = False
            self.ghost_combo = 0

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))