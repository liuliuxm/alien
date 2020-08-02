# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 21:08:09 2020

@author: 18142
"""

import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep 

def check_keydown_events(event,ai_settings,screen,ship,bullets,stats,aliens,sb):
    '''响应按键'''
    #向右移动飞船
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    #向左移动飞船
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    #向上移动飞船
    elif event.key == pygame.K_UP:
        ship.moving_up =True
    #向下移动飞船
    elif event.key ==pygame.K_DOWN:
        ship.moving_down = True
     #按空格键发射子弹
    elif event.key == pygame.K_SPACE: 
        fire_bullet(ai_settings,screen,ship,bullets)
    #按q退出游戏界面
    elif event.key == pygame.K_q:
        pygame.quit()
        sys.exit()
    #按P开始游戏
    elif event.key == pygame.K_p: 
        if stats.game_active == False:
            start_game(stats,aliens,bullets,ship,ai_settings,screen,sb)
    
         
def check_keyup_events(event,ship):
    '''响应松开'''
    if event.key ==pygame.K_RIGHT:
         ship.moving_right = False 
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key ==pygame.K_DOWN:
        ship.moving_down = False
    
           
        
def check_events(ai_settings,screen,ship,bullets,stats,play_button,aliens,sb):
    '''响应按键和鼠标事件'''
     #监视键盘和鼠标事件
    for event in pygame.event.get():#为访问Pygame检测到的事件      
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()   
# 玩家单击游戏窗口的关闭按钮时，将检测到pygame.QUIT事件，而我们调用sys.exit()来退出游戏.           
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets,stats,aliens,sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)   
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()#返回一个元组，其中包含玩家单击时鼠标的x和y坐标
            check_play_button(stats,play_button,mouse_x,mouse_y,aliens,bullets,ai_settings,screen,ship,sb)#检查鼠标单击位置是否在Play按钮的rect内
       
        
def get_number_aliens_x(ai_settings,alien_width):
    '''计算一行可容纳多少个外星人'''
     #外星人间距为外星人宽度
    available_space_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x /(2*alien_width))
    return number_aliens_x


def get_number_rows(ai_settings,ship_height,alien_height):
    '''计算屏幕可容纳多少行外星人'''
    availabel_space_y = (ai_settings.screen_height - (3*alien_height) - ship_height)
    number_rows = int(availabel_space_y /(2*alien_height))
    return number_rows


def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    '''创建一个外星人，并将其放在当前行'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width *alien_number
    alien.rect.x = alien.x 
    alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
    aliens.add(alien)
    
    
def create_fleet(ai_settings,screen,aliens,ship):
    '''创建外星人群'''
    #创建一个外星人，并计算一行可容纳多少个外星人
    alien = Alien(ai_settings,screen)
    number_aliens_x =get_number_aliens_x(ai_settings,alien.rect.width) 
    number_rows =get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    
    #创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)
        
        
def check_fleet_edges(ai_settings,aliens):
    '''有外星人到达边缘时采取相应的措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
        
        
def change_fleet_direction(ai_settings,aliens):
    '''将整群外星人下移，并改变他们的方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1



def fire_bullet(ai_settings,screen,ship,bullets):
    '''如果还没有达到限制，就发射一颗子弹'''
    #创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)
           
        
def update_bullets(ai_settings,aliens,bullets,screen,ship,stats,sb):
    '''更新子弹的位置，并删除已消失的子弹'''
    #更新子弹的位置
    bullets.update()
    #删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #print(len(bullets))
    check_bullet_alien_collision(ai_settings,screen,ship,aliens,bullets,stats,sb)
    
    
def check_bullet_alien_collision(ai_settings,screen,ship,aliens,bullets,stats,sb): 
    '''相应子弹和外星人的碰撞'''
     #检查是否有子弹击中了外星人
    #如果是，就删除相应的子弹和外星
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
                                #遍历编组bullets中的每颗子弹，再遍历编组aliens中的每个外星人。
                                #每当有子弹和外星人的rect重叠时，groupcollide()就在它返回的字典中添加一个键-值对。
                                #两个实参True告诉Pygame删除发生碰撞的子弹和外星人。返回一个字典
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
        
    if len(aliens) ==0:
        #删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        #提高等级
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings,screen,aliens,ship)
    
    
def ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb):
    '''响应被外星人撞到的飞船'''
    if stats.ships_left > 0:
        #将ships_left减1
        stats.ships_left -= 1
        #更新飞船数
        sb.prep_ships()
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings,screen,aliens,ship)
        ship.center_ship()
        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        #游戏结束后重新显示光标
        pygame.mouse.set_visible(True)
    
    
def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets,sb):
    '''检查是否有外星人到达屏幕底部'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞到一样进行处理
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb)
            break
    
    
def update_aliens(ai_settings,stats,screen,aliens,ship,bullets,sb):
    '''检查是否有外星人位于屏幕边缘，更新外星人群中所有外星人的位置'''
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #检测外星人和飞船之间的碰撞
    #方法spritecollideany()接受两个实参：一个精灵和一个编组。
    #它检查编组是否有成员与精灵发生了碰撞，并在找到与精灵发生了碰撞的成员后就停止遍历编组.
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb)
        
    #检查是否有外星人到达屏幕底部
    check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets,sb)
      
    
def start_game(stats,aliens,bullets,ship,ai_settings,screen,sb):
    '''开始游戏的设置'''
    #隐藏光标
    pygame.mouse.set_visible(False) 
    #重置游戏统计信息
    stats.reset_stats()
    stats.game_active  = True
    #重置记分牌图像
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    #清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
    #创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings,screen,aliens,ship)
    ship.center_ship()
        

def check_play_button(stats,play_button,mouse_x,mouse_y,aliens,bullets,ai_settings,screen,ship,sb):
    '''在玩家单机play按钮时开始游戏'''
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    #print(button_clicked) 
    #输出结果为1，当玩家单击了Play按钮且游戏当前处于非活动状态时，游戏才重新开始
    if button_clicked and (stats.game_active == False):
        #玩家重新开始游戏时，重置游戏设置
        ai_settings.initialize_dynamic_settings()
        start_game(stats,aliens,bullets,ship,ai_settings,screen,sb)
        
    
def check_high_score(stats,sb):
    '''检查是否诞生了新的最高分'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
    
    
def update_screen(ai_settings,screen,ship,aliens,bullets,stats,play_button,sb):
    '''更新屏幕上的图像，并切换到新屏幕'''
    #每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    
    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():#返回一个列表，其中包含编组bullets中的所有精灵
        bullet.draw_bullet()
        
    ship.blitme()
    aliens.draw(screen)
    #显示得分
    sb.show_score()
    #如果游戏处于非活动状态，就显示play按钮
    if stats.game_active == False:
        play_button.draw_button()
        
    #让最近绘制的屏幕可见
    pygame.display.flip()
    '''
    在我们移动游戏元素时，pygame.display.flip()将不断更新屏幕，
    以显示元素的新位置，并在原来的位置隐藏元素，从而营造平滑移动的效果。
    '''