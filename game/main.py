#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import sys
import json
import argparse
import pygame as pg
import random



from setting import text_objects, button, quit, Game, Potion, RedPotion, BluePotion

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", default="config.json", help="game configuration file")
parser.add_argument("-a", "--auto", default=False ,action='store_true', help="play map automatically")

        

def maingame(config_path, autoplay,roomnumber):

    # Load game configuration file
    with open(config_path, "r") as f:
        config = json.loads(f.read())

    # Setup game environment
    game = Game(config['map']['path']["{}".format(roomnumber)], config['map']['unit'])
    potion = Potion(config['map']['path']["{}".format(roomnumber)], config['map']['unit'], screen)
    #block = MapBlock(config['map']['path']["{}".format(roomnumber)], config['map']['unit'], screen)
    screen_rect = screen.get_rect()
    andy = game.andy
    chucky = game.chucky
    chucky_group = game.chucky_group
    obstacle_group = game.obstacle_group
    #block_group = block.block_group
    redpotion_group = potion.redpotion_group
    bluepotion_group = potion.bluepotion_group
    code1 = True
    code2 = True
    code11 = True
    code22 = True
    start1 = -5000
    start2 = -5000
    start11 = -5000
    start22 = -5000
    
    quit_flag = False
    
    # player collision detect
    def finish():
        if len(pg.sprite.spritecollide(andy, chucky_group, False)) != 0 :
            return True
        else:
            return False
        
    start_time = pg.time.get_ticks()
        
    while not finish() and not quit_flag:
        # Event checking
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            #if event.type == pg.KEYDOWN:
            #    if event.key == pg.K_ESCAPE:
            #        quit_flag = True
        
        keys = pg.key.get_pressed()    
        if keys[pg.K_UP]:
            if code11 == True:
                chucky.up()
            else:
                chucky.ups()
        elif keys[pg.K_DOWN]:
            if code11 == True:
                chucky.down()
            else:
                chucky.downs()
        elif keys[pg.K_RIGHT]:
            if code11 == True:
                chucky.right()
            else:
                chucky.rights()
        elif keys[pg.K_LEFT]:
            if code11 == True:
                chucky.left()
            else:
                chucky.lefts()
        else:
            pass
            
        if keys[pg.K_w]:
            if code22 == True:
                andy.up()
            else:
                andy.ups()
        elif keys[pg.K_s]:
            if code22 == True:
                andy.down()
            else:
                andy.downs()
        elif keys[pg.K_a]:
            if code22 == True:
                andy.left()
            else:
                andy.lefts()
        elif keys[pg.K_d]:
            if code22 == True:
                andy.right()
            else:
                andy.rights()
        else:
            pass
    

            
        # Check collision
        if len(pg.sprite.spritecollide(andy, obstacle_group, False)) != 0 :
            if (code1 == True) and (code22 == True):
                andy.stepback()
            elif (code1 == True) and (code22 == False):
                andy.stepbacks()
            else:
                pass
        if len(pg.sprite.spritecollide(chucky, obstacle_group, False)) != 0 :
            if (code2 == True) and (code11 == True):
                chucky.stepback()
            elif (code2 == True) and (code11 == False):
                chucky.stepbacks()
            else:
                pass
        
        if len(pg.sprite.spritecollide(andy, redpotion_group, True)) != 0 :
            andy.stepback()
            code1 = False
            start1 = pg.time.get_ticks()
        if len(pg.sprite.spritecollide(chucky, redpotion_group, True)) != 0 :
            chucky.stepback()
            code2 = False
            start2 = pg.time.get_ticks()
        if len(pg.sprite.spritecollide(andy, bluepotion_group, True)) != 0 :
            andy.stepback()
            code11 = False
            start11 = pg.time.get_ticks()
        if len(pg.sprite.spritecollide(chucky, bluepotion_group, True)) != 0 :
            chucky.stepback()
            code22 = False
            start22 = pg.time.get_ticks()
        
        #限制角色移動範圍在地圖之內
        andy.rect.clamp_ip(screen_rect)
        chucky.rect.clamp_ip(screen_rect)
        

        # Update screen
        screen.blit(game.map.image, game.map.rect)
        
        if code1 == False:
            screen.blit(andy.image2, andy.rect)
        else:
            screen.blit(andy.image, andy.rect)
        
        if code2 == False:
            screen.blit(chucky.image2, chucky.rect)
        else:
            screen.blit(chucky.image, chucky.rect)
        
        if code22 == False:
            screen.blit(andy.image3, andy.rect)
        else:
            screen.blit(andy.image, andy.rect)
        
        if code11 == False:
            screen.blit(chucky.image3, chucky.rect)
        else:
            screen.blit(chucky.image, chucky.rect)
        
        redpotion_group.draw(screen)
        bluepotion_group.draw(screen)
        
        # potion times up
        if (pg.time.get_ticks() - start1) >= 3000:
            code1 = True
        if (pg.time.get_ticks() - start2) >= 3000:
            code2 = True
        if (pg.time.get_ticks() - start11) >= 3000:
            code11 = True
        if (pg.time.get_ticks() - start22) >= 3000:
            code22 = True
        
        # Check game times remain
        if (pg.time.get_ticks() - start_time) >= 40000:
            quit_flag = True
            global survive
            survive = True
        
        # potion pop up
        if (pg.time.get_ticks() - start_time) >= 5000 and (pg.time.get_ticks() - start_time) <= 5010:
            redpotion = RedPotion((random.randint(1,38)*30, random.randint(2,24)*30))
            redpotion_group.add(redpotion)
            bluepotion = BluePotion((random.randint(1,38)*30, random.randint(2,24)*30))
            bluepotion_group.add(bluepotion)
        
        if (pg.time.get_ticks() - start_time) >= 15000 and (pg.time.get_ticks() - start_time) <= 15010:
            redpotion = RedPotion((random.randint(1,38)*30, random.randint(2,24)*30))
            redpotion_group.add(redpotion)
            bluepotion = BluePotion((random.randint(1,38)*30, random.randint(2,24)*30))
            bluepotion_group.add(bluepotion)
                
        if (pg.time.get_ticks() - start_time) >= 25000 and (pg.time.get_ticks() - start_time) <= 25010:
            redpotion = RedPotion((random.randint(1,38)*30, random.randint(2,24)*30))
            redpotion_group.add(redpotion)
            bluepotion = BluePotion((random.randint(1,38)*30, random.randint(2,24)*30))
            bluepotion_group.add(bluepotion)
                
        if (pg.time.get_ticks() - start_time) >= 35000 and (pg.time.get_ticks() - start_time) <= 35010:
            redpotion = RedPotion((random.randint(1,38)*30, random.randint(2,24)*30))
            redpotion_group.add(redpotion)
            bluepotion = BluePotion((random.randint(1,38)*30, random.randint(2,24)*30))
            bluepotion_group.add(bluepotion)
        
        
        pg.time.delay(5)
        pg.display.update()


def menu():
    
    #menu_pic
    image = pg.image.load("C:/Users/User/Desktop/game/pictures/menu_pic.jpg")
    image = pg.transform.rotozoom(image,0.0,5/6)
    image.convert()
    
    musicfile = "C:/Users/User/Desktop/game/gamemusic/childs_play_theme.mp3"
    pg.mixer.music.load(musicfile)
    pg.mixer.music.play(-1)
    pg.mixer.music.set_volume(0.4)
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
        
        screen.blit(image, (0,0))
        
        # 宣告 font 文字物件
        headfont = pg.font.SysFont(None, 140)
        
        
        TextSurf, TextRect = text_objects("Child\'s Play", headfont, (255,255,255))
        TextRect.center = ((400,160))
        screen.blit(TextSurf, TextRect)
    
        # 畫按鈕
        button('PLAY!',screen,340,280,180,80,(255,255,255),(255,153,153),(0,0,0),75,start)
        button('Option',screen,340,440,180,80,(255,255,255),(255,153,153),(0,0,0),75,None)
        button('Quit',screen,340,600,180,80,(255,255,255),(255,153,153),(0,0,0),75,quit)
    
    
        pg.display.update()
    

    
    
def start():    
    args = vars(parser.parse_args())
    andywin = 0
    
    musicfile = "C:/Users/User/Desktop/game/gamemusic/zed_mart_massacre.mp3"
    pg.mixer.music.load(musicfile)
    pg.mixer.music.play(-1,30)
    pg.mixer.music.set_volume(0.4)
    
    for room in range(1,6):
        global survive
        survive = False
        maingame(args['config'], args['auto'],room)
        score(survive)
        if survive == True:
            andywin += 1
        else:
            andywin -= 1
    endpage(andywin)
    
    
def endpage(andywin):
    image = pg.image.load("C:/Users/User/Desktop/game/pictures/menu_pic.jpg") # andy survive
    image = pg.transform.rotozoom(image,0.0,5/6)
    image.convert()
        
    musicfile = "C:/Users/User/Desktop/game/gamemusic/friends_until_the_end.mp3"
    pg.mixer.music.load(musicfile)
    pg.mixer.music.play(-1,10)
    pg.mixer.music.set_volume(0.4)
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            
        screen.blit(image, (0,0))
        
        if andywin > 0:
            win = 'Andy'
        else:
            win = 'Chucky'
        
        headfont = pg.font.SysFont(None, 140)
        
        TextSurf, TextRect = text_objects("{} Win!!".format(win), headfont, (255,255,255))
        TextRect.center = ((400,160))
        screen.blit(TextSurf, TextRect)
            
        
        button('MENU',screen,340,440,180,80,(255,255,255),(255,153,153),(0,0,0),75,menu)

        pg.display.update()
            
def gonext():
    global stop
    stop = False
            
def score(survive):
    global stop
    stop = True
    if survive == True:
        image = pg.image.load("C:/Users/User/Desktop/game/pictures/andywin.png")
        image = pg.transform.rotozoom(image,0.0,1200/1435)
        image.convert()
        
        while stop:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
            
            screen.blit(image, (0,0))
            
            button('Next>>',screen,140,280,180,80,(255,255,255),(255,153,153),(0,0,0),75,gonext)
            button('MENU',screen,140,440,180,80,(255,255,255),(255,153,153),(0,0,0),75,menu)
            
            pg.display.update()
    else: # survive = False
        image = pg.image.load("C:/Users/User/Desktop/game/pictures/chuckywin.png") # chucky win
        image = pg.transform.rotozoom(image,0.0,1200/1066)
        image.convert()
        
        while stop:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
            
            screen.blit(image, (0,0))
            
            button('Next>>',screen,140,280,180,80,(255,255,255),(255,153,153),(0,0,0),75,gonext)
            button('MENU',screen,140,440,180,80,(255,255,255),(255,153,153),(0,0,0),75,menu)
            
            pg.display.update()
            
      
            
if __name__ == "__main__":
    
    pg.init()
    # 建立 window 視窗畫布，大小為 1200x750
    screen = pg.display.set_mode((1200, 750))
    # 設置視窗標題為 Child's Play
    pg.display.set_caption('Child\'s Play')
    
    menu()

    

# In[ ]:




