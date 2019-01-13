import random
import sys
import pygame
from pygame.locals import *
from plane import Bkground, Bullet, Enemy, Player

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

bullets=pygame.sprite.Group()				#子弹精灵组
enemys=pygame.sprite.Group()				#敌机精灵组
down_enemys=pygame.sprite.Group()			#死亡的敌机精灵组(方便绘制飞机死亡时的动画)

count=0										#用于控制子弹发射频率

while player.is_kill():
	
	bk.draw_bkimg(screen)				#绘制背景图片
	player.draw(screen)					#绘制玩家飞机
	bullets.draw(screen)				#绘制子弹
	
	for enemy in enemys:
		enemy.draw(screen)				#由于绘制血条 因此自定义draw方法
	for down_enemy in down_enemys:
		down_enemy.draw(screen)


	for event in pygame.event.get():
		if event.type==QUIT:
			pygame.quit()
			sys.exit()

	if count%8==0:
		if player.is_alive():										#设置子弹发射频率(飞机存活时)
			bullets.add(Bullet(player.rect.midtop))
		if len(enemys)<7:										#控制同时出现的敌机数量
			enemys.add(Enemy())

	
	bk.move()
	player.update(pygame.time.get_ticks(),enemys)
	if player.is_alive():
		player.move(pygame.key.get_pressed())					#根据按键控制玩家飞机移动
	bullets.update()											#更新子弹位置
	enemys.update(bullets,down_enemys)							#检测子弹与敌机碰撞 更新位置或加入死亡的飞机精灵组

	if count%3==0:												#控制死亡动画的速度
		for down_enemy in down_enemys:
			down_enemy.down_update()

#	print(len(down_enemys))										#测试剩余多少子弹

	count+=1													#计数器控制频率
	pygame.display.flip()										#更新屏幕画面
	clock.tick(25)


pygame.quit()
print('游戏结束')
sys.exit()
