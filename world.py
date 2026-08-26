import pygame
import time

from settings import HEIGHT, WIDTH, NAV_HEIGHT, CHAR_SIZE, PLAYER_SPEED
from pac import Pac
from cell import Cell
from berry import Berry
from ghost import Ghost
from display import Display
from map_loader import MapLoader
from particle import ParticleSystem

class World:
    def __init__(self, screen):
        self.screen = screen

        self.player = pygame.sprite.GroupSingle()
        self.ghosts = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.berries = pygame.sprite.Group()

        self.display = Display(self.screen)
        self.particles = ParticleSystem()

        self.game_over = False
        self.reset_pos = False
        self.player_score = 0
        self.game_level = 1

        self.map_grid = MapLoader.load_map(f"maps/level{self.game_level}.txt")
        self._generate_world()

    def _generate_world(self):
        self.walls.empty()
        self.berries.empty()
        self.ghosts.empty()
        self.player.empty()

        for y_index, col in enumerate(self.map_grid):
            for x_index, char in enumerate(col):
                if char == "1":
                    self.walls.add(Cell(x_index, y_index, CHAR_SIZE, CHAR_SIZE))
                elif char == " ":
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 4))
                elif char == "B":
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 2, is_power_up=True))

                elif char == "s":
                    self.ghosts.add(Ghost(x_index, y_index, "skyblue"))
                elif char == "p": 
                    self.ghosts.add(Ghost(x_index, y_index, "pink"))
                elif char == "o":
                    self.ghosts.add(Ghost(x_index, y_index, "orange"))
                elif char == "r":
                    self.ghosts.add(Ghost(x_index, y_index, "red"))

                elif char == "P":
                    self.player.add(Pac(x_index, y_index))

        self.walls_collide_list = [wall.rect for wall in self.walls.sprites()]

    def generate_new_level(self):
        self.map_grid = MapLoader.load_map(f"maps/level{((self.game_level - 1) % 2) + 1}.txt")
        self._generate_world()

    def restart_level(self):
        self.game_level = 1
        self.game_over = False
        self.map_grid = MapLoader.load_map("maps/level1.txt")
        self._generate_world()

    def _dashboard(self):
        nav = pygame.Rect(0, HEIGHT, WIDTH, NAV_HEIGHT)
        pygame.draw.rect(self.screen, (20, 20, 35), nav)
        pygame.draw.line(self.screen, (0, 255, 255), (0, HEIGHT), (WIDTH, HEIGHT), 2)
        
        if self.player.sprite:
            self.display.show_life(self.player.sprite.life)
            self.display.show_level(self.game_level)
            self.display.show_score(self.player.sprite.pac_score)

    def _check_game_state(self):
        if self.player.sprite and self.player.sprite.life == 0:
            self.game_over = True

        if len(self.berries) == 0 and self.player.sprite and self.player.sprite.life > 0:
            self.game_level += 1
            self.generate_new_level()

    def draw(self):
        [wall.update(self.screen) for wall in self.walls.sprites()]
        [berry.update(self.screen) for berry in self.berries.sprites()]
        self.ghosts.draw(self.screen)

        if self.player.sprite:
            self.player.draw(self.screen)

        self.particles.draw(self.screen)
        self._dashboard()

    def update(self):
        if not self.game_over and self.player.sprite:
            pressed_key = pygame.key.get_pressed()
            self.player.sprite.animate(pressed_key, self.walls_collide_list)

            # Teleport wrap-around
            if self.player.sprite.rect.right <= 0:
                self.player.sprite.rect.x = WIDTH
            elif self.player.sprite.rect.left >= WIDTH:
                self.player.sprite.rect.x = 0

            # Eat berries
            for berry in self.berries.sprites():
                if self.player.sprite.rect.colliderect(berry.rect):
                    if berry.power_up:
                        self.player.sprite.immune_time = 150
                        self.player.sprite.pac_score += 50
                        self.particles.emit(berry.rect.centerx, berry.rect.centery, (0, 255, 255), 15)
                        for ghost in self.ghosts.sprites():
                            ghost.set_frightened(150)
                    else:
                        self.player.sprite.pac_score += 10
                        self.particles.emit(berry.rect.centerx, berry.rect.centery, (255, 255, 180), 5)
                    berry.kill()

            # Find Red ghost for Inky targeting calculations
            red_ghost = next((g for g in self.ghosts.sprites() if g.color_name == "red"), None)
            red_rect = red_ghost.rect if red_ghost else None

            # Ghost interactions & AI updates
            for ghost in self.ghosts.sprites():
                ghost.update(
                    self.walls_collide_list,
                    pac_rect=self.player.sprite.rect,
                    pac_dir=self.player.sprite.direction,
                    red_ghost_rect=red_rect
                )

                if self.player.sprite.rect.colliderect(ghost.rect):
                    if not ghost.is_frightened and not self.player.sprite.immune:
                        self.particles.emit(self.player.sprite.rect.centerx, self.player.sprite.rect.centery, (255, 50, 50), 20)
                        self.player.sprite.life -= 1
                        self.reset_pos = True
                        break
                    elif ghost.is_frightened:
                        self.player.sprite.ghost_combo += 1
                        points = 200 * (2 ** (self.player.sprite.ghost_combo - 1))
                        self.player.sprite.pac_score += points
                        self.particles.emit(ghost.rect.centerx, ghost.rect.centery, (0, 255, 100), 25)
                        ghost.move_to_start_pos()

            self.player.update()

        self._check_game_state()

        # Update particle effects
        self.particles.update()

        if self.reset_pos and not self.game_over:
            [ghost.move_to_start_pos() for ghost in self.ghosts.sprites()]
            if self.player.sprite:
                self.player.sprite.move_to_start_pos()
            self.reset_pos = False