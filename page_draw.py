import pygame
import tkinter as tk
from tkinter import colorchooser

class DrawPage:

##### INIT function #####
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.w, self.h = self.screen.get_width(), self.screen.get_height()
        self.game.gridSize = int(0.95*self.h)
        self.listRect = []
        self.listColor = []
        self.index = 0
        self.saveImage = pygame.image.load("./diskette.png")
        self.selected = 0

        #Back Button
        self.menuWidth = int(0.5*(self.w-self.game.gridSize))
        self.menuHeight = self.h/10
        self.backButton = pygame.Rect(0, 0, self.menuWidth, self.menuHeight)
        self.btn_color = 'white'
        self.textColor = 'black'
        self.font = pygame.font.SysFont('Arial', 35)

        #Border
        self.border = pygame.Rect(0, 0, self.menuWidth, self.menuHeight)

        #Grid
        self.grid = pygame.Rect(self.menuWidth, 0, self.game.gridSize, self.game.gridSize)
        self.gridBaseColor = 'gray'

        #Color selection
        self.colorSquare = pygame.Rect(0, int(4 * self.menuHeight), self.menuWidth, int((self.h - 4 * self.menuHeight)- 1))
        self.blockSizeX = self.menuWidth / 3
        self.selected_color = 'white'

        #OffSet buttons
        self.offset = -1
        self.plusBtn = pygame.Rect(self.grid.right, 0, int(self.menuWidth/2), self.menuHeight)

    def on_enter(self):
        # Appelée quand on arrive sur la page
        self.drawGrid(self.game.gridValue)

##### RESIZE screen function #####
    def checkResize(self):
        newW, newH = self.screen.get_width(), self.screen.get_height()
        if newH != self.h or newW != self.w:
            scaleY = newH/self.h
            scaleX = newW/self.w
            self.screenSize()
            self.resizeColorBlock(scaleX, scaleY)

    def screenSize(self):
        self.w, self.h = self.screen.get_width(), self.screen.get_height()
        self.game.gridSize = round(0.95*self.h)
        self.menuWidth = round(0.5*(self.w-self.game.gridSize))
        self.menuHeight = round(self.h/10)

        self.backButton = pygame.Rect(0, 0, self.menuWidth, self.menuHeight)
        self.border = pygame.Rect(0, 0, self.menuWidth, self.menuHeight)
        self.grid = pygame.Rect(self.menuWidth, 0, self.game.gridSize, self.game.gridSize)
        self.blockSizeX = self.menuWidth / 3
        self.colorSquare = pygame.Rect(0, 4 * self.menuHeight, self.menuWidth, (self.h - 4 * self.menuHeight)- 1)
        self.selected = 0
        self.drawGrid(self.game.gridValue)

    def resizeColorBlock(self, scaleX, scaleY):
        for rectColor in self.listColor:
            x = round(scaleX * rectColor["pos"][0])
            y =  round(scaleY * rectColor["pos"][1])
            rectColor["rect"].update(x, y, self.blockSizeX, self.menuHeight)
            rectColor["pos"][0] = x
            rectColor["pos"][1] = y


##### COLOR Tkinter function #####
    def choose_custom_color(self):
        # Crée une fenêtre Tkinter (cachée)
        root = tk.Tk()
        root.withdraw()

        # Ouvre la palette système
        color_code = colorchooser.askcolor(title="Choisir une couleur")

        # Récupère la couleur hex (ex: '#ff0000') si valide
        if color_code[1] is not None:
            self.selected_color = color_code[1]  # Hex string compatible avec pygame
            self.colorSquarePos()

    def colorSquarePos(self):
        # Calcule la position pour l'affichage dans la palette
        # Nombre de cellules verticales max
        max_rows = int((self.h - 4 * self.menuHeight) // self.menuHeight) - 1

        # Calcul position en colonne et ligne
        row = self.index % max_rows
        col = (self.index // max_rows) % 3

        x = col * self.blockSizeX
        y = int(4 * self.menuHeight + row * self.menuHeight)

        color_rect = pygame.Rect(x, y, self.blockSizeX, self.menuHeight)

        self.listColor.append({
            "pos": [x, y],
            "color": self.selected_color,
            "rect": color_rect
        })

        self.index += 1

##### EVENT function #####
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.backButton.collidepoint(mouse_pos):
                    self.game.current_page = self.game.pages["menu"]
                elif self.customColorBtn.collidepoint(mouse_pos):
                    self.choose_custom_color()
                elif self.clearBtn.collidepoint(mouse_pos):
                    self.on_enter()
                elif self.colorSquare.collidepoint(mouse_pos):
                    self.chooseSquareEffect(mouse_pos)
                elif self.saveBtn.collidepoint(mouse_pos):
                    self.saveDraw()
                elif self.plusBtn.collidepoint(mouse_pos):
                    self.offset +=1

        if pygame.mouse.get_pressed(3)[0] is True:
            if self.grid.collidepoint(mouse_pos):
                self.colorGrid(mouse_pos)
    
    def colorGrid(self, mouse_pos):
        cols = rows = self.game.gridValue
        for i, cell in enumerate(self.listRect):
                if cell["rect"].collidepoint(mouse_pos):
                    # Coordonnées de la case dans la grille
                    col = i % cols
                    row = i // cols
                    if self.offset >= 0:
                    # Parcours du carré x*x
                        for dy in range(-self.offset + (-1), self.offset + 2):
                            for dx in range(-self.offset + (-1), self.offset + 2):
                                new_col = col + dx
                                new_row = row + dy

                                if 0 <= new_col < cols and 0 <= new_row < rows:
                                    index = new_row * cols + new_col
                                    self.listRect[index]["color"] = self.selected_color
                        break
                    else:
                        cell["color"] = self.selected_color
                    

    def chooseSquareEffect(self, mouse_pos):
        for color in self.listColor:
            if color["rect"].collidepoint(mouse_pos):
                self.selected_color = color["color"]
                self.selected = pygame.Rect(color["rect"].x, color["rect"].y, self.blockSizeX, self.menuHeight)
                break

    def saveDraw(self):
        self.game.pixelArt = pygame.Surface((self.game.gridSize, self.game.gridSize), pygame.SRCALPHA)
        self.game.pixelArt.fill((0, 0, 0, 0))
        for pixel in self.listRect:
            rect = pixel["rect"]
            color = pixel["color"]
            pygame.draw.rect(self.game.pixelArt, color, pygame.Rect(rect.x - self.grid.left, rect.y, rect.width, rect.height))

        self.game.current_page = self.game.pages["save"]

##### DRAW function #####
    def draw(self):
        self.screen.fill("black")

        #Draw first button to go back to the menu
        self.btnText = 'Back'
        self.text = self.font.render(self.btnText, True, self.textColor)
        pygame.draw.rect(self.screen, self.btn_color, self.backButton)
        pygame.draw.rect(self.screen, self.textColor, self.border, 1)
        text_rect = self.text.get_rect(center=self.backButton.center)
        self.screen.blit(self.text, text_rect)

        self.drawGridHover()
        self.drawButtons()

        for colorNewBtn in self.listColor:
            pygame.draw.rect(self.screen, colorNewBtn["color"], colorNewBtn["rect"])
        if self.selected != 0:
            pygame.draw.rect(self.screen, 'red', self.selected, 3)

        pygame.draw.rect(self.screen, self.btn_color, self.plusBtn)

        pygame.display.flip()

    def drawButtons(self):
        button_labels = ["Choose Color", "Clear", "Save"]
        current_rect = self.backButton
        current_border = self.border

        for label in button_labels:
            # Déplacement vertical pour positionner le bouton
            current_rect = current_rect.move(0, self.menuHeight)
            current_border = current_border.move(0, self.menuHeight)

            # Rendu du texte
            self.text = self.font.render(label, True, self.textColor)

            # Dessin du bouton
            pygame.draw.rect(self.screen, self.btn_color, current_rect)
            pygame.draw.rect(self.screen, self.textColor, current_border, 1)

            # Placement du texte centré sur le bouton
            text_rect = self.text.get_rect(center=current_rect.center)
            self.screen.blit(self.text, text_rect)

            # Sauvegarde des boutons pour usage ultérieur
            if label == "Choose Color":
                self.customColorBtn = current_rect
            elif label == "Clear":
                self.clearBtn = current_rect
            elif label == "Save":
                self.saveBtn = current_rect

##### GRID Interaction function #####
    def drawGrid(self, maxIteration):
        self.listRect.clear()
        size = int(self.game.gridSize / maxIteration)

        for i in range(maxIteration):
            x = self.grid.left + i * size
            for j in range(maxIteration):
                y = j * size
                rect = pygame.Rect(x, y, size, size)
                self.listRect.append({"rect": rect, "color": (0, 0, 0, 0)})

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
