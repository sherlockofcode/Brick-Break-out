import pygame
import sys
import time
#initialisation
pygame.init()
screen=pygame.display.set_mode((640,480))
clock=pygame.time.Clock()
brick_w = 60
brick_h= 15
paddle_w = 80
paddle_h = 12
ball_dia= 16
ball_rad = 8

max_paddle_x= 640 - 60 
max_ball_x = 640 - 16
max_ball_y = 480 -16
paddle_y= 480-20

#color constants
blue=(0,0,255)
white=(255,255,255)


# create the brick class
class bricks:
	def __init__(self):
		y=35
		self.bricks=[]
		for i in range(7):
			x=35
			for j in range(8):
				self.bricks.append(pygame.Rect(x,y,brick_w,brick_h))
				x=x+brick_w +10
			y = y+ brick_h + 5

	def drawbricks(self):
		for brick in self.bricks:
			pygame.draw.rect(screen,white,brick)

class user1:
	def __init__(self):
		self.ball_velx=5
		self.ball_vely=-5
		self.paddle=pygame.Rect(300,paddle_y,paddle_w,paddle_h)
		self.ball=pygame.Rect(300,paddle_y-ball_dia,ball_dia,ball_dia)
		
	def drawballandpaddle(self):
		pygame.draw.rect(screen,white,self.paddle)
		pygame.draw.circle(screen,white, (self.ball.left+ ball_rad,self.ball.top+ball_rad),ball_rad)
	def moveball(self):
		self.ball.left  = self.ball.left +self.ball_velx;
		self.ball.top  = self.ball.top +self.ball_vely;
#		print  self.ball.left, self.ball.top
		if self.ball.left <=0:
			self.ball.left=0
			self.ball_velx-=2*self.ball_velx
		if self.ball.left >=max_ball_x:
			self.ball.left=max_ball_x
			self.ball_velx-=2*self.ball_velx

		if self.ball.top <=0:
			self.ball.top=0
			self.ball_vely-=2*self.ball_vely
		if self.ball.top >=max_ball_y:
			self.ball.top=max_ball_y
			self.ball_vely-=2*self.ball_vely 

score=0
lives=3
state=0
block=bricks()
user=user1()
def run(a,b):
	global score,lives,state
	keys= pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		pygame.quit()
		sys.exit()
	screen.fill(blue)
	a.drawbricks()
	b.drawballandpaddle()
	screen.blit(pygame.font.Font(None,30).render("score:" +str(score) +"lives:" +str(lives),False,white),(205,5))
	if(state==0):
		b.ball.left=b.paddle.left+b.paddle.width/2
		b.ball.top=b.paddle.top - b.ball.height
		screen.blit(pygame.font.Font(None,30).render("Press space to launch ball",False,white),(300,300))
		if keys[pygame.K_SPACE]:
			state=1
#			print state
	if(state==1):
		b.moveball()
		if keys[pygame.K_LEFT]:
			if(b.paddle.left >=0):
				b.paddle.left -= 5
		if keys[pygame.K_RIGHT]:
			if(b.paddle.left <max_paddle_x):
				b.paddle.left +=5
		for brick in a.bricks:
			if b.ball.colliderect(brick):
				score+=3
				b.ball_vely-=2*b.ball_vely
				a.bricks.remove(brick)
				break
		if(len(a.bricks)==0):
		  	state=2
		if b.ball.colliderect(b.paddle):
			b.ball.top=paddle_y-ball_dia
			b.ball_vely-=2*b.ball_vely
		if(b.ball.top >b.paddle.top):
			lives-=1
			if(lives>0):
				state=0
			else:
			 	state=3
	if(state==2):
		screen.blit(pygame.font.Font(None,30).render("Game won: press esc to quit",False,white),(20,300))
	if(state==3):
		screen.blit(pygame.font.Font(None,30).render("Game lost: press esc to quit",False,white),(20,300))
		time.sleep(5)
	#Make event listener:
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
	clock.tick(50)
	pygame.display.flip()
while 1:
	run(block,user)

