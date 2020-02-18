import pygame
import sys
import random
import math
import time

pygame.font.init()

# fonts
fonts = pygame.font.Font('freesansbold.ttf',45)
overfonts = pygame.font.Font('freesansbold.ttf',50)
font = pygame.font.Font(None, 40)

# messages
success = "Completed Round!"
hit = "Crash!"
pl2win = "Player 2 WINS!!"
pl1win = "Player 1 WINS!!"
bothwin = "Both Players WIN!!"

# colors
river = (59, 179, 208)
sand = (238, 214, 175)
bank = (194, 178, 128)

class Player(object):
    height = 0
    width = 0
    def __init__(self, icon, posx, posy, score, sc, lev, key, surf):
        self.icon = icon
        self.posx = posx
        self.posy = posy
        #self.rect = pygame.Rect(self.posx, self.posy, 64, 64)
        self.score = score
        self.sc = sc
        self.lev = lev
        self.key1 = key
        self.surf = surf
        global height 
        height = surf.get_height()
        global width 
        width = surf.get_width()

    def addPlayer(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.surf.blit(self.icon, (posx, posy))
        if posx <= 0:
            self.posx = 1
        elif posx >= width-64:
            self.posx = width-65
        if posy <= 0:
            self.posy = 0
        elif posy >= height-64:
            self.posy = height-65
        self.rect = pygame.Rect(self.posx, self.posy, 64, 64)

    def updatepos(self):
        
        if self.key1[0]:
            self.posy -= 1
        elif self.key1[1]:
            self.posy += 1
        elif self.key1[2]:
            self.posx += 2
        elif self.key1[3]:
            self.posx -= 2
        self.rect = pygame.Rect(self.posx, self.posy, 64, 64)

    #def switch_player(self, turn_no, level):
class MovingObs:
    def __init__(self, icon, posx, posy, changex, surf):
        self.icon = icon
        self.posx = posx
        self.posy = posy
        self.surf = surf
        self.chngx = changex
#       global height 
#       height = surf.get_height()
#       global width 
#       width = surf.get_width()

    def addMovingObs(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.surf.blit(self.icon, (posx, posy))
        # if they hit the edge of screen
        if self.posx <= 0:
            self.chngx = -self.chngx
        elif self.posx >= self.surf.get_width()-64:
            self.chngx = -self.chngx    

class StationaryObs:
    def __init__(self, icon, posx, posy, surf):
        self.icon = icon
        self.posx = posx
        self.posy = posy
        self.surf = surf
    
    def addStationaryObs(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.surf.blit(self.icon, (posx, posy))