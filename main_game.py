import pygame
import sys
from pygame.locals import *
from plane import Bkground,Player,Bullet


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

count=0

while True:
	
	screen.fill((0,0,0))
	bk.draw_bkimg(screen)				#绘制背景图片
	player.draw(screen)
	bullets.draw(screen)

	for event in pygame.event.get():
		if event.type==QUIT:
			pygame.quit()
			sys.exit()

	if count%8==0:																#设置子弹发射频率
		bullets.add(Bullet(player.rect.midtop))
	
	bk.move()
	player.update(pygame.time.get_ticks())
	player.move(pygame.key.get_pressed())
	bullets.update()												#更新子弹位置

	if len(bullets)>0 and bullets.sprites()[0].rect.bottom<0:
		bullets.remove(bullets.sprites()[0])						#删除越界的子弹

	count+=1
	pygame.display.update()
	clock.tick(20)
