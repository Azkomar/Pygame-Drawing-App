import pygame

class DrawPage:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        w, h = self.screen.get_width(), self.screen.get_height()
        self.w = w
        self.h = h
        self.listRect = []

        #Back Button
        self.btnWidth = w/8
        self.btnHeight = h/10
        self.button = pygame.Rect(0, 0, self.btnWidth, self.btnHeight)
        self.btn_color = 'black'
        self.font = pygame.font.SysFont('Arial', 35)
        self.text = self.font.render('Retour', True, 'white')

        #Grid
        self.grid = pygame.Rect(self.btnWidth, 0, w-self.btnWidth, h)
        self.gridBaseColor = 'gray'

    def on_enter(self):
        # Appelée quand on arrive sur la page
        self.drawGrid(self.game.gridValue)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button.collidepoint(pygame.mouse.get_pos()):
                    self.game.current_page = self.game.pages["menu"]
                else:
                    mouse_pos = pygame.mouse.get_pos()
                    for cell in self.listRect:
                        if cell["rect"].collidepoint(mouse_pos):
                            cell["color"] = "blue"

    def update(self):
        pass

    def draw(self):
        self.screen.fill("white")
        pygame.draw.rect(self.screen, self.btn_color, self.button)
        text_rect = self.text.get_rect(center=self.button.center)
        self.screen.blit(self.text, text_rect)
        self.drawGridHover()
        pygame.display.flip()
    
    def drawGrid(self, size):
        self.listRect.clear()
        pygame.draw.rect(self.screen, self.btn_color, self.grid, 1)
        for x in range(self.grid.left, int(self.w-self.w/8), size):
            for y in range(0, self.h, size):
                rect = pygame.Rect(x, y, size, size)
                pygame.draw.rect(self.screen, self.gridBaseColor, rect, 1)
                self.listRect.append({"rect": rect, "color": "white"})

    def drawGridHover(self):
        mouse_pos = pygame.mouse.get_pos()
        for cell in self.listRect:
            rect = cell["rect"]
            color = cell["color"]
            pygame.draw.rect(self.screen, color, rect)

            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, 'red', rect, 2)
            else:
                pygame.draw.rect(self.screen, self.gridBaseColor, rect, 1)