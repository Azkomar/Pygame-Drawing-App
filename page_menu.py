import pygame

class MenuPage:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        w, h = self.screen.get_width(), self.screen.get_height()

        self.button = pygame.Rect(w/3, h/4, w/3, h/6)
        self.btn_color = 'black'
        self.font = pygame.font.SysFont('Arial', 35)
        self.text = self.font.render('50', True, 'white')

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button.collidepoint(pygame.mouse.get_pos()):
                    self.game.gridValue = 50
                    self.game.current_page = self.game.pages["draw"]
                    self.game.pages["draw"].on_enter()

    def update(self):
        pass

    def draw(self):
        self.screen.fill("white")
        pygame.draw.rect(self.screen, self.btn_color, self.button)
        text_rect = self.text.get_rect(center=self.button.center)
        self.screen.blit(self.text, text_rect)
        pygame.display.flip()