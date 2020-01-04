#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:

import sys
import pygame as pg
import numpy as np



def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def button(msg,surface,x,y,w,h,initcolor,actcolor,textcolor,fontsize,action):
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pg.draw.rect(surface, actcolor, (x,y,w,h))
        
        if click[0] == 1 and action != None:
            action()
    else:
        pg.draw.rect(surface, initcolor, (x,y,w,h))

    buttonfont = pg.font.SysFont(None,fontsize)
    textSurf, textRect = text_objects(msg, buttonfont, textcolor)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    surface.blit(textSurf, textRect)

def quit():
    pg.quit()
    sys.exit()
    
    
class Player(pg.sprite.Sprite):
    
    def __init__(self,player,player2,player3,zoom,initrect):
        super().__init__()
        self.prev_action = None
        
        image = pg.image.load(player)
        image = pg.transform.rotozoom(image,0.0,zoom)
        image.convert()
        self.image = image
        self.rect = image.get_rect(topleft=initrect)
        
        image2 = pg.image.load(player2)
        image2 = pg.transform.rotozoom(image2,0.0,zoom)
        image2.convert()
        self.image2 = image2
        
        image3 = pg.image.load(player3)
        image3 = pg.transform.rotozoom(image3,0.0,zoom)
        image3.convert()
        self.image3 = image3
        
        self.initrect = image.get_rect(topleft=initrect)

    def up(self):
        self.prev_action = pg.K_UP
        self.rect.move_ip(0, -2)

    def down(self):
        self.prev_action = pg.K_DOWN
        self.rect.move_ip(0, 2)

    def right(self):
        self.prev_action = pg.K_RIGHT
        self.rect.move_ip(2, 0)

    def left(self):
        self.prev_action = pg.K_LEFT
        self.rect.move_ip(-2, 0)

    def stepback(self):
        if self.prev_action == pg.K_UP:
            self.rect.move_ip(0, 2)
        elif self.prev_action == pg.K_DOWN:
            self.rect.move_ip(0, -2)
        elif self.prev_action == pg.K_RIGHT:
            self.rect.move_ip(-2, 0)
        elif self.prev_action == pg.K_LEFT:
            self.rect.move_ip(2, 0)
    
    
    
    def ups(self):
        self.prev_action = pg.K_UP
        self.rect.move_ip(0, -1)

    def downs(self):
        self.prev_action = pg.K_DOWN
        self.rect.move_ip(0, 1)

    def rights(self):
        self.prev_action = pg.K_RIGHT
        self.rect.move_ip(1, 0)

    def lefts(self):
        self.prev_action = pg.K_LEFT
        self.rect.move_ip(-1, 0)

    def stepbacks(self):
        if self.prev_action == pg.K_UP:
            self.rect.move_ip(0, 1)
        elif self.prev_action == pg.K_DOWN:
            self.rect.move_ip(0, -1)
        elif self.prev_action == pg.K_RIGHT:
            self.rect.move_ip(-1, 0)
        elif self.prev_action == pg.K_LEFT:
            self.rect.move_ip(1, 0)

        
            
            
class Potion(pg.sprite.Sprite):
    
    def __init__(self, map_path, unit, screen):
        super().__init__()
        self.redpotions = []
        self.bluepotions = []
        
        with open(map_path, "r") as f:
            lines = f.read().strip('\n').split('\n')

            for row, line in enumerate(lines):
                for col, symbol in enumerate(line):
                    if symbol == 'R':
                        redpotion = RedPotion((col*unit, row*unit))
                        self.redpotions.append(redpotion)
                    
                    elif symbol == 'B':
                        bluepotion = BluePotion((col*unit, row*unit))
                        self.bluepotions.append(bluepotion)
                        
                    else:
                        pass
        
        self.redpotion_group = pg.sprite.Group(self.redpotions)
        self.bluepotion_group = pg.sprite.Group(self.bluepotions)
        
        
class RedPotion(pg.sprite.Sprite):

    def __init__(self, initrect):
        super().__init__()
        
        image = pg.image.load("pictures/redpotion.png")
        image = pg.transform.rotozoom(image,0.0,1/5)
        image.convert()
        self.image = image
        self.rect = image.get_rect(topleft=initrect)
                        

class BluePotion(pg.sprite.Sprite):

    def __init__(self, initrect):
        super().__init__()
        
        image = pg.image.load("pictures/bluepotion.png")
        image = pg.transform.rotozoom(image,0.0,3/62)
        image.convert()
        self.image = image
        self.rect = image.get_rect(topleft=initrect)
        
            
class MapObstacle(pg.sprite.Sprite):

    def __init__(self, position, texture):
        super().__init__()
        self.texture = texture
        self.image = pg.surfarray.make_surface(np.transpose(texture ,(1, 0, 2)))
        self.rect = pg.Rect(position, self.texture.shape[:2])
        

class Map(pg.sprite.Sprite):

    def __init__(self, position, texture):
        super().__init__()
        self.texture = texture
        self.image = pg.surfarray.make_surface(np.transpose(texture ,(1, 0, 2)))
        self.rect = pg.Rect(position, self.texture.shape[:2])


class Game:

    def __init__(self, map_path, unit):
        self.map_path = map_path
        self.unit = unit

        # The following attributes will be initialized later
        self.map = None
        self.obstacles = []
        self.blocks = []
        self.exit_point = None

        # Build Map
        with open(map_path, "r") as f:
            # Reserve space for map
            lines = f.read().strip('\n').split('\n') # Read the map
            mapunit = np.zeros((len(lines)*unit, len(lines[0])*unit, 3)) # (height, width, depth)

            # Initialize map row by row
            for row, line in enumerate(lines):
                for col, symbol in enumerate(line):
                    if symbol == '@':   # white road
                        # Set the color on this position to white in map
                        mapunit[row*unit:row*unit+unit, col*unit:col*unit+unit, :] = 255

                        
                    elif symbol == '#':   # black obstacle
                        # Set the color on this position to black in map
                        mapunit[row*unit:row*unit+unit, col*unit:col*unit+unit, :] = 0
                        
                        # Create obstacle
                        obstacle = MapObstacle(
                                        (col*unit, row*unit),
                                        mapunit[row*unit:row*unit+unit, col*unit:col*unit+unit, :].copy())
                        self.obstacles.append(obstacle)
                    
                    
                    elif symbol == '=': #upper plate
                        # Set to light green
                        mapunit[row*unit:row*unit+unit, col*unit:col*unit+unit, 0] = 51
                        mapunit[row*unit:row*unit+unit, col*unit:col*unit+unit, 1] = 255
                        mapunit[row*unit:row*unit+unit, col*unit:col*unit+unit, 2] = 51
                        
                        obstacle = MapObstacle(
                                        (col*unit, row*unit),
                                        mapunit[row*unit:row*unit+unit, col*unit:col*unit+unit, :].copy())
                        self.obstacles.append(obstacle)
                    
                    elif symbol == 'A':
                        mapunit[row*unit:row*unit+unit, col*unit:col*unit+unit, :] = 255
                        
                        andyfig = "pictures/andy-1.png"
                        andyfig2 = "pictures/andy-2.png"
                        andyfig3 = "pictures/andy-3.png"
                        self.andy = Player(andyfig,andyfig2,andyfig3,27/169,(col*unit,row*unit))
                        
                    elif symbol == 'C':
                        mapunit[row*unit:row*unit+unit, col*unit:col*unit+unit, :] = 255
                        
                        chuckyfig = "pictures/chucky-1.png"
                        chuckyfig2 = "pictures/chucky-2.png"
                        chuckyfig3 = "pictures/chucky-3.png"
                        self.chucky = Player(chuckyfig,chuckyfig2,chuckyfig3,0.05,(col*unit,row*unit))
                        
                    elif symbol == 'B':
                        mapunit[row*unit:row*unit+unit, col*unit:col*unit+unit, :] = 255
                        
                    elif symbol == 'R':
                        mapunit[row*unit:row*unit+unit, col*unit:col*unit+unit, :] = 255
                    
                    else:
                        raise Exception("Invalid symbol in maze '%s'" % symbol)

        # Save map
        self.map = Map((0, 0), mapunit.copy())
        
        
        # Create groups
        self.chucky_group = pg.sprite.Group(self.chucky)
        self.obstacle_group = pg.sprite.Group(self.obstacles)
        self.block_group = pg.sprite.Group(self.blocks)
        

