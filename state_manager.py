import pygame
import sys
from settings import WIDTH, HEIGHT, NAV_HEIGHT
from world import World
from high_score_manager import HighScoreManager
from asset_manager import AssetManager

class StateManager:
    def __init__(self, screen):
        self.screen = screen
        self.high_score_mgr = HighScoreManager()
        self.world = World(self.screen)
        self.state = "MENU" # MENU, PLAY, PAUSE, GAMEOVER

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.state == "MENU":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.world.restart_level()
                        self.state = "PLAY"

                elif self.state == "PLAY":
                    if event.key in (pygame.K_p, pygame.K_ESCAPE):
                        self.state = "PAUSE"

                elif self.state == "PAUSE":
                    if event.key in (pygame.K_p, pygame.K_ESCAPE):
                        self.state = "PLAY"
                    elif event.key == pygame.K_m:
                        self.state = "MENU"

                elif self.state == "GAMEOVER":
                    if event.key == pygame.K_r:
                        self.world.restart_level()
                        self.state = "PLAY"
                    elif event.key == pygame.K_m:
                        self.state = "MENU"

    def update(self):
        if self.state == "PLAY":
            self.world.update()
            if self.world.player.sprite:
                self.high_score_mgr.update_high_score(self.world.player.sprite.pac_score)
            if self.world.game_over:
                self.state = "GAMEOVER"

    def draw(self):
        self.screen.fill("black")

        if self.state == "MENU":
            self._draw_menu()
        elif self.state == "PLAY":
            self.world.draw()
        elif self.state == "PAUSE":
            self.world.draw()
            self._draw_pause()
        elif self.state == "GAMEOVER":
            self.world.draw()
            self._draw_game_over()

    def _draw_menu(self):
        title_font = AssetManager.get_font(42)
        sub_font = AssetManager.get_font(24)
        small_font = AssetManager.get_font(18)

        title_surf = title_font.render("PAC-MAN ARCADE", True, (255, 255, 0))
        start_surf = sub_font.render("Press ENTER or SPACE to Play", True, (0, 255, 255))
        score_surf = sub_font.render(f"HIGH SCORE: {self.high_score_mgr.high_score}", True, (255, 184, 255))
        
        controls_surf = small_font.render("Controls: Arrow Keys / WASD | P: Pause | R: Restart", True, (200, 200, 200))

        self.screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 3)))
        self.screen.blit(score_surf, score_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        self.screen.blit(start_surf, start_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60)))
        self.screen.blit(controls_surf, controls_surf.get_rect(center=(WIDTH // 2, HEIGHT - 40)))

    def _draw_pause(self):
        overlay = pygame.Surface((WIDTH, HEIGHT + NAV_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        font = AssetManager.get_font(40)
        sub_font = AssetManager.get_font(22)

        pause_surf = font.render("GAME PAUSED", True, (255, 255, 255))
        resume_surf = sub_font.render("Press P to Resume | M for Main Menu", True, (200, 200, 200))

        self.screen.blit(pause_surf, pause_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        self.screen.blit(resume_surf, resume_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

    def _draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT + NAV_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        self.screen.blit(overlay, (0, 0))

        font = AssetManager.get_font(46)
        sub_font = AssetManager.get_font(24)

        go_surf = font.render("GAME OVER", True, (255, 50, 50))
        score_surf = sub_font.render(f"Final Score: {self.world.player.sprite.pac_score if self.world.player.sprite else 0}", True, (255, 255, 255))
        high_surf = sub_font.render(f"High Score: {self.high_score_mgr.high_score}", True, (255, 255, 0))
        restart_surf = sub_font.render("Press R to Restart | M for Main Menu", True, (0, 255, 255))

        self.screen.blit(go_surf, go_surf.get_rect(center=(WIDTH // 2, HEIGHT // 3)))
        self.screen.blit(score_surf, score_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        self.screen.blit(high_surf, high_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
        self.screen.blit(restart_surf, restart_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70)))
