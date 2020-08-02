# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 17:04:10 2020

@author: 18142
"""

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_settings,screen):
        '''初始化飞船并设置其初始化位置'''
        super().__init__()
        self.screen = screen
        self.ai_settings =ai_settings
        
        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('E:\\大三下\\python练习\\项目\\项目1外星人入侵\\images\\ship.bmp')
        self.rect = self.image.get_rect()#使用get_rect()获取相应surface的属性rect
        self.screen_rect = screen.get_rect()
        
        #将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        #self.rect.centery = self.screen_rect.centery
        
        self.rect.bottom = self.screen_rect.bottom
        
        #在飞船的属性ceter中存储小数值
        self.centerx = float(self.rect.centerx)
        #self.centery = float(self.rect.centery)
        self.bottom = float(self.rect.bottom)
        
        #移动标志
        self.moving_right = False 
        self.moving_left = False
        self.moving_up =False
        self.moving_down = False
        
        
    def update(self):
        '''根据移动标志调整飞船的位置，并限制飞船范围'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
            
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
    
        if self.moving_up and self.rect.top > 0:
            self.bottom  -= self.ai_settings.ship_speed_factor
            
        if self.moving_down and self.rect.bottom <self.screen_rect.bottom:
            self.bottom  += self.ai_settings.ship_speed_factor
            
        self.rect.centerx =self.centerx
        #self.rect.centery = self.centery
        self.rect.bottom = self.bottom
        
        
    def center_ship(self):
        '''让飞船在屏幕上居中'''
        self.center = self.screen_rect.centerx
        
    
    def blitme(self):
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image,self.rect)#根据self.rect指定的位置将图像绘制到屏幕上。
        
    
            