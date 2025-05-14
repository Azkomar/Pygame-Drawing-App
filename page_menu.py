import pygame

class MenuPage:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        w, h = self.screen.get_width(), self.screen.get_height()

        self.inputField = pygame.Rect(w/2-w/6, h/2-h/12, w/3, h/6)
        self.active = False
        self.input = ''
        self.font = pygame.font.SysFont('Arial', 35)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.inputField.collidepoint(mouse_pos):
                    self.active = True
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.input = self.input[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.game.gridValue = int(self.input)
                        self.game.current_page = self.game.pages["draw"]
                        self.game.pages["draw"].on_enter()
                    else:
                        self.input += event.unicode
                    


    def draw(self):
        self.screen.fill("black")
        if self.active:
            pygame.draw.rect(self.screen, 'red', self.inputField, 1)
            self.textInput = self.font.render(self.input, True, 'white')
            inputText = self.textInput.get_rect(center=self.inputField.center)
            self.screen.blit(self.textInput, inputText)
        else:
            pygame.draw.rect(self.screen, "white", self.inputField)

        pygame.display.flip()