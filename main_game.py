import pygame
import sys
from pygame.locals import *


SCREEN_WIDTH=450
SCREEN_HEIGHT=680

bk_y1=0												#背景图片坐标
bk_y2=SCREEN_HEIGHT									#背景图片坐标

pygame.init()

pygame.display.set_caption('飞机大战')
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock=pygame.time.Clock()

bk_img=pygame.image.load('img/background.png').convert_alpha()

while True:
	
	screen.fill((0,0,0))
	screen.blit(bk_img,(0,bk_y1))
	screen.blit(bk_img,(0,bk_y2))

	for event in pygame.event.get():
		if event.type==QUIT:
			pygame.quit()
			sys.exit()
	
	bk_y1-=8
	bk_y2-=8

	if bk_y1<=-SCREEN_HEIGHT:
		bk_y1=SCREEN_HEIGHT
	if bk_y2<=-SCREEN_HEIGHT:
		bk_y2=SCREEN_HEIGHT

	pygame.display.update()
	clock.tick(20)
