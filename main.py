import pygame
from page_menu import MenuPage
from page_draw import DrawPage
from page_save import SavePage

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.gridValue = 0
        self.pixelArt = 0
        self.gridSize = 0

        # Pages
        self.pages = {
            "menu": MenuPage(self),
            "draw": DrawPage(self),
            "save": SavePage(self)
        }
        self.current_page = self.pages["menu"]
        
    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.current_page.handle_events(events)
            self.current_page.checkResize()
            self.current_page.draw()
            self.clock.tick(120)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1600, 1000), pygame.RESIZABLE)
    game = Game(screen)
    game.run()
    pygame.quit()