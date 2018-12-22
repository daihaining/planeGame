import pygame
import sys
from pygame.locals import *
from plane import Bkground,Player,Bullet,Enemy
import random


SCREEN_WIDTH=450
SCREEN_HEIGHT=680

bk_y1=0												#背景图片坐标
bk_y2=SCREEN_HEIGHT			

pygame.init()

pygame.display.set_caption('飞机大战')
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock=pygame.time.Clock()

bk=Bkground()
player=Player((200,500))

bullets=pygame.sprite.Group()				#子弹组
enemys=pygame.sprite.Group()

count=0

while player.is_alive():
	
	screen.fill((0,0,0))
	bk.draw_bkimg(screen)				#绘制背景图片
	player.draw(screen)					#绘制玩家飞机
	bullets.draw(screen)				#绘制子弹
	
	for enemy in enemys:
		enemy.draw(screen)


	for event in pygame.event.get():
		if event.type==QUIT:
			pygame.quit()
			sys.exit()

	if count%8==0:
		if player.num<2:										#设置子弹发射频率(飞机存活时)
			bullets.add(Bullet(player.rect.midtop))
		if len(enemys)<9:										#控制同时出现的敌机数量
			enemys.add(Enemy())

	
	bk.move()
	player.update(pygame.time.get_ticks(),enemys)
	player.move(pygame.key.get_pressed())
	bullets.update()							#更新子弹位置
	enemys.update(bullets)

	#print(len(enemys))							#测试剩余多少子弹

	count+=1									#计数器控制频率
	pygame.display.update()
	clock.tick(25)


pygame.quit()
print('游戏结束')
sys.exit()

