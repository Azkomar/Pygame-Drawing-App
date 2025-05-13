import pygame
from page_menu import MenuPage
from page_draw import DrawPage

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.gridValue = 0

        # Pages
        self.pages = {
            "menu": MenuPage(self),
            "draw": DrawPage(self)
        }
        self.current_page = self.pages["menu"]
        
    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.current_page.handle_events(events)
            self.current_page.update()
            self.current_page.draw()
            self.clock.tick(30)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    game = Game(screen)
    game.run()
    pygame.quit()