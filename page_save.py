import pygame
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename

class SavePage:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.w, self.h = self.screen.get_width(), self.screen.get_height()

        self.menuWidth = int(0.5*(self.w-self.game.gridSize))
        self.menuHeight = self.h/10
        self.border = pygame.Rect(0, 0, self.menuWidth, self.menuHeight)
        self.backButton = pygame.Rect(0, 0, self.menuWidth, self.menuHeight)
        self.btn_color = 'white'
        self.textColor = 'black'
        self.font = pygame.font.SysFont('Arial', 35)

        self.viewRect = pygame.Rect(self.menuWidth, 0, self.game.gridSize, self.game.gridSize)

    def checkResize(self):
        newW, newH = self.screen.get_width(), self.screen.get_height()
        if newH != self.h or newW != self.w:
            scaleY = newH/self.h
            scaleX = newW/self.w
            self.screenSize()

    def screenSize(self):
        self.w, self.h = self.screen.get_width(), self.screen.get_height()
        self.game.gridSize = round(0.95*self.h)
        self.menuWidth = round(0.5*(self.w-self.game.gridSize))
        self.menuHeight = round(self.h/10)

        self.backButton = pygame.Rect(0, 0, self.menuWidth, self.menuHeight)
        self.border = pygame.Rect(0, 0, self.menuWidth, self.menuHeight)
        self.viewRect = pygame.Rect(self.menuWidth, 0, self.game.gridSize, self.game.gridSize)

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.backButton.collidepoint(mouse_pos):
                    self.game.current_page = self.game.pages["draw"]
                elif self.saveBtn.collidepoint(mouse_pos):
                    Tk().withdraw()
                    f = asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
                    if f is None:
                        return
                    else:
                        pygame.image.save(self.game.pixelArt, f)

    def draw(self):
        self.screen.fill("black")

        #Draw first button to go back to the menu
        self.btnText = 'Back'
        self.text = self.font.render(self.btnText, True, self.textColor)
        pygame.draw.rect(self.screen, self.btn_color, self.backButton)
        pygame.draw.rect(self.screen, self.textColor, self.border, 1)
        text_rect = self.text.get_rect(center=self.backButton.center)
        self.screen.blit(self.text, text_rect)

        self.saveBtn = self.backButton.move(0, self.menuHeight)
        self.borderBis = self.border.move(0, self.menuHeight)

        pygame.draw.rect(self.screen, self.btn_color, self.saveBtn)
        self.text = self.font.render("Save", True, self.textColor)
        text_rect = self.text.get_rect(center=self.saveBtn.center)
        self.screen.blit(self.text, text_rect)

        self.screen.blit(self.game.pixelArt, self.viewRect)
        pygame.display.flip()