import pygame
from settings import WIDTH, HEIGHT, NAV_HEIGHT
from state_manager import StateManager

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT + NAV_HEIGHT))
pygame.display.set_caption("NEON PAC-MAN ARCADE")

class Main:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.state_manager = StateManager(self.screen)

    def main(self):
        while True:
            events = pygame.event.get()
            self.state_manager.handle_events(events)
            self.state_manager.update()
            self.state_manager.draw()
            
            pygame.display.update()
            self.clock.tick(30)

if __name__ == "__main__":
    game = Main(screen)
    game.main()