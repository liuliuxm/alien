# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 10:49:59 2020

@author: 18142
"""

import pygame
from settings import Settings 
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

#from alien import Alien

def run_game():
    '''初始化游戏并创建一个屏幕对象'''
    #初始化背景设置
    pygame.init()
    ai_settings = Settings()
    
    #创建一个名为screen的显示窗口，这个游戏的所有图形元素都将在其中绘制。
    #对象screen是一个surface。在Pygame中，surface是屏幕的一部分，用于显示游戏元素。
    #在这个游戏中，每个元素（如外星人或飞船）都是一个surface。
    #display.set_mode()返回的surface表示整个游戏窗口
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    #设置窗口标题
    pygame.display.set_caption('Alien Invasion')
    
    #创建play按钮
    play_button = Button(ai_settings,screen,'Play')
    
    #创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    
    #创建记分牌
    sb = Scoreboard(ai_settings,screen,stats)
    
    #创建一艘飞船
    ship = Ship(ai_settings,screen) 
    
    #创建一个用于存储子弹的编组和一个外星人编组
    bullets = Group()
    aliens = Group()
    
    #创建外星人群
    gf.create_fleet(ai_settings,screen,aliens,ship)
    
    #开始游戏的主循环
    while True:
        #监视键盘和鼠标事件
        gf.check_events(ai_settings,screen,ship,bullets,stats,play_button,aliens,sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,aliens,bullets,screen,ship,stats,sb)
            gf.update_aliens(ai_settings,stats,screen,aliens,ship,bullets,sb)
        gf.update_screen(ai_settings,screen,ship,aliens,bullets,stats,play_button,sb)
        
run_game()