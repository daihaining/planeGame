import pygame
import sys
from pygame.locals import *
from plane import Bkground,Player


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

while True:
	
	screen.fill((0,0,0))
	bk.draw_bkimg(screen)				#绘制背景图片
	screen.blit(player.image,player.rect)

	for event in pygame.event.get():
		if event.type==QUIT:
			pygame.quit()
			sys.exit()
	bk.move()
	player.update(pygame.time.get_ticks())
	player.move(pygame.key.get_pressed())

	pygame.display.update()
	clock.tick(20)
