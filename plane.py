import pygame
import random

WIDTH=450
HEIGHT=680

#背景类 实现背景移动
class Bkground:
	
	def __init__(self):
		self.pos=[0,HEIGHT]																		#背景图片位置
		self.bk_img=pygame.image.load('img/background.png').convert_alpha()				#背景图片

	#绘制背景图片
	def draw_bkimg(self,screen):
		screen.blit(self.bk_img,(0,self.pos[0]))
		screen.blit(self.bk_img,(0,self.pos[1]))

	#图片移动
	def move(self):
		for i in range(0,2):
			self.pos[i]-=2;
			if(self.pos[i]<-HEIGHT):
				self.pos[i]=HEIGHT

#玩家类
class Player(pygame.sprite.Sprite):
	
	#玩家飞机图片
	player_imgs=['img/hero1.png','img/hero2.png','img/hero_blow1.png','img/hero_blow2.png','img/hero_blow3.png','img/hero_blow4.png']
	for i in range(0,len(player_imgs)):
		player_imgs[i]=pygame.image.load(player_imgs[i])		#加载所需要的图片文件
	
	#初始化玩家位置
	def __init__(self,init_pos):
		super().__init__()

		self.image=Player.player_imgs[0]
		self.rect=self.image.get_rect()
		self.rect.topleft=init_pos
		self.num=0								#图片编号(同时记录状态)
		self.update_time=0						#更新时间
		self.radius=min(self.rect.size)/2*0.8	#设置半径属性(方便碰撞检测)
		self.speed=10							#飞机移动时的速度

	def update(self,current_time,enemys):

		if self.num<2 and self.__is_collision(enemys):
			self.num=2

		if(current_time>self.update_time):
			
			if self.num<2:
				self.num=(self.num+1)%2
			else:
				self.num+=1
			if self.num<len(Player.player_imgs):
				self.image=Player.player_imgs[self.num]

			self.update_time=current_time+60

	def move(self,key_pressed):
		if key_pressed[pygame.K_a] and self.rect.x>0:
			self.rect.x-=self.speed
		if key_pressed[pygame.K_d] and self.rect.x<WIDTH-self.rect.width:
			self.rect.x+=self.speed
		if key_pressed[pygame.K_w] and self.rect.y>0:
			self.rect.y-=self.speed
		if key_pressed[pygame.K_s] and self.rect.y<HEIGHT-self.rect.height:
			self.rect.y+=self.speed

	def draw(self,screen):
		screen.blit(self.image,self.rect)

	#判断是否与敌机碰撞
	def __is_collision(self,enemys):
		for enemy in enemys:
			if pygame.sprite.collide_circle(self,enemy):
				return True		
		return False

	#返回玩家是否存活
	def is_alive(self):
		return self.num<len(Player.player_imgs)


class Bullet(pygame.sprite.Sprite):
	
	#初始化子弹
	def __init__(self,pos):
		super().__init__()
		self.image=pygame.image.load('img/bullet1.png').convert_alpha()
		self.rect=self.image.get_rect()
		self.speed=20												#子弹速度
		self.rect.midbottom=pos 									#设置坐标


	def update(self):
		self.rect.y-=self.speed
		if self.rect.bottom<=0:
			self.kill()												#删除子弹(子弹越界时)

#敌机类
class Enemy(pygame.sprite.Sprite):
	
	enemy_imgs=[['img/enemy0.png','img/enemy0_down1.png','img/enemy0_down2.png','img/enemy0_down3.png','img/enemy0_down4.png'],
				['img/enemy1.png','img/enemy1_down1.png','img/enemy1_down2.png','img/enemy1_down3.png','img/enemy1_down4.png'],
				['img/enemy2.png','img/enemy2_down1.png','img/enemy2_down2.png','img/enemy2_down3.png','img/enemy2_down4.png',
				'img/enemy2_down5.png','img/enemy2_down6.png']];
	for i in range(0,len(enemy_imgs)):
		for j in range(0,len(enemy_imgs[i])):
			enemy_imgs[i][j]=pygame.image.load(enemy_imgs[i][j])	#加载图片

	#初始化敌机
	def __init__(self):
		super().__init__()
		self.id=Enemy.__init_enemy_id()						#不同飞机编号
		self.state=0										#状态(方便绘制不同图片)
		self.image=Enemy.enemy_imgs[self.id][self.state]
		self.rect=self.image.get_rect()
		self.speed=random.randint(5,10)						#速度
		self.rect.topleft=(random.uniform(0,WIDTH-self.rect.w),-self.rect.height) 	#设置坐标
		self.radius=min(self.rect.size)/2*0.9					#设置半径(方便碰撞检测)
		self.blood=self.id*2+1									#敌机血量(根据飞机类型不同血量不同)
		self.sum_blood=self.blood 								#敌机总血量方便绘制血条

	def update(self,bullets):

		if self.blood>0:						#敌机血量大于零时
			self.rect.y+=self.speed
			self.__is_collision(bullets)

		if self.blood==0:
			self.state+=1
			if self.state<len(Enemy.enemy_imgs[self.id]):
				self.image=Enemy.enemy_imgs[self.id][self.state]			#更新图片

		if self.rect.top>=HEIGHT or self.state>len(Enemy.enemy_imgs[self.id]):
			self.kill()												#删除敌机(敌机越界时或者)

	#判断是否与子弹碰撞
	def __is_collision(self,bullets):
		for bullet in bullets:
			if pygame.sprite.collide_rect(self,bullet):
				self.blood-=1										#敌机血量减少
				bullet.kill()										#消灭敌机后子弹销毁

	def draw(self,screen):
		screen.blit(self.image,self.rect)
		#绘制血条
		if self.id>0:
			scale=self.blood/self.sum_blood
			pygame.draw.rect(screen,(0,255,0),(self.rect.x,self.rect.y-12,self.rect.w*scale,2))
			pygame.draw.rect(screen,(255,0,0),(self.rect.x+self.rect.w*scale,self.rect.y-12,self.rect.w*(1-scale),2))


	#产生不同飞机
	@staticmethod
	def __init_enemy_id():
		num=random.random()
		if num<=0.6:
			return 0
		elif num>0.96:
			return 2
		else:
			return 1
