import pygame

class MenuPage:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        w, h = self.screen.get_width(), self.screen.get_height()

        self.button50 = pygame.Rect(w/3, h/4, w/3, h/6)
        self.btn_color = 'black'
        self.font = pygame.font.SysFont('Arial', 35)
        self.text = self.font.render('50 px', True, 'white')

        self.button10 = pygame.Rect(w/3, self.button50.bottom + h/4, w/3, h/6)
        self.text10 = self.font.render('10 px', True, 'white')

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button50.collidepoint(pygame.mouse.get_pos()):
                    self.game.gridValue = 50
                    self.game.current_page = self.game.pages["draw"]
                    self.game.pages["draw"].on_enter()

                if self.button10.collidepoint(pygame.mouse.get_pos()):
                    self.game.gridValue = 10
                    self.game.current_page = self.game.pages["draw"]
                    self.game.pages["draw"].on_enter()

    def draw(self):
        self.screen.fill("white")
        pygame.draw.rect(self.screen, self.btn_color, self.button50)
        text_rect = self.text.get_rect(center=self.button50.center)
        self.screen.blit(self.text, text_rect)

        pygame.draw.rect(self.screen, self.btn_color, self.button10)
        text_rect = self.text10.get_rect(center=self.button10.center)
        self.screen.blit(self.text10, text_rect)

        pygame.display.flip()