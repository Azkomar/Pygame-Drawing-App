import pygame
import tkinter as tk
from tkinter import colorchooser

class DrawPage:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        w, h = self.screen.get_width(), self.screen.get_height()
        self.w = w
        self.h = h
        self.listRect = []

        #Back Button
        self.menuWidth = w/8
        self.menuHeight = h/10
        self.button = pygame.Rect(0, 0, self.menuWidth, self.menuHeight)
        self.btn_color = 'black'
        self.font = pygame.font.SysFont('Arial', 35)
        self.text = self.font.render('Retour', True, 'white')

        #Grid
        self.grid = pygame.Rect(self.menuWidth, 0, w-self.menuWidth, h)
        self.gridBaseColor = 'gray'

        #Color selection
        self.blockSize = self.menuWidth/2
        self.selected_color = 'blue'
        self.custom_color_btn = pygame.Rect(0, self.menuHeight, self.menuWidth, self.menuHeight)
        self.custom_color_txt = self.font.render("Choose Color", True, "white")

    def on_enter(self):
        # Appelée quand on arrive sur la page
        self.drawGrid(self.game.gridValue)

    def choose_custom_color(self):
        # Crée une fenêtre Tkinter (cachée)
        root = tk.Tk()
        root.withdraw()

        # Ouvre la palette système
        color_code = colorchooser.askcolor(title="Choisir une couleur")

        # Récupère la couleur hex (ex: '#ff0000') si valide
        if color_code[1] is not None:
            self.selected_color = color_code[1]  # Hex string compatible avec pygame

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button.collidepoint(pygame.mouse.get_pos()):
                    self.game.current_page = self.game.pages["menu"]
                elif self.custom_color_btn.collidepoint(pygame.mouse.get_pos()):
                    self.choose_custom_color()
                    

        if pygame.mouse.get_pressed(3)[0] is True:
            mouse_pos = pygame.mouse.get_pos()
            for cell in self.listRect:
                if cell["rect"].collidepoint(mouse_pos):
                    cell["color"] = self.selected_color
            

    def update(self):
        pass

    def draw(self):
        self.screen.fill("white")
        pygame.draw.rect(self.screen, self.btn_color, self.button)
        text_rect = self.text.get_rect(center=self.button.center)
        self.screen.blit(self.text, text_rect)
        
        #for i in range(2):
        #   for j in range(int(self.menuHeight), self.h, int(self.blockSize)):
        #       rect = pygame.Rect(i*self.blockSize, j, self.blockSize, self.blockSize)
         #       pygame.draw.rect(self.screen, 'red', rect, 1)

        self.drawGridHover()

        pygame.draw.rect(self.screen, "gray", self.custom_color_btn)
        text_rect = self.custom_color_txt.get_rect(center=self.custom_color_btn.center)
        self.screen.blit(self.custom_color_txt, text_rect)

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