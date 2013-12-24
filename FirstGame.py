import pygame
import math
import random

random.seed()
clock = pygame.time.Clock()
time = 0
timefactor = .00001
collisiontimefactor = .001
otherfactor = 500
width = 1200
length = 700
menulength = 80
sliderspace = 10
sliderlength = menulength/2 - 2*sliderspace
slidernumber = 4
sliderrows = 2
sliderbarlength = 20
sliderbarwidth = 15
sliderwidth = width/sliderrows - 2*sliderspace
playerrad = 100
numberenemies = 20
enemyrad = 50
enemymass = 10
playermass = 40
speed = 5.0
slowdown = .5
basespeed = 5.0
gravity = 0.0
gravitythresh = 5.0
velocitythresh = 200
minvelocity = .1
collision = 1
gravityon = False
jump = 1
jumpmax = 100
basejump = 1 
airresistance = 0

class Slider:
	def __init__(self,name,pos,min,max):
		self.pos = pos
		self.min = min
		self.max = max
		self.name = name
		self.barpos = 0
		self.temp = 0
		
	def getpos(self):
		return self.pos
	
	def changepos(self,barpos):
		self.barpos = barpos
		
	def getbarpos(self):
		return self.barpos
		
	def getname(self):
		return self.name
		
	def update(self):
		self.temp = self.min + ( self.barpos /( 1.0 * ( sliderwidth - sliderspace ) ) ) * ( self.max - self.min )
		return self.temp
	
class Ball:
	def __init__(self,pos,vel,accel,mass):
		self.pos = pos
		self.vel = vel
		self.accel = accel
		self.mass = mass
		
	def velx(self):
		return self.vel.x
	def vely(self):
		return self.vel.y
	def vel(self):
		return self.vel
	def posx(self):
		return self.pos.x
	def posy(self):
		return self.pos.y
	def accelx(self):
		return self.accel.x
	def accely(self):
		return self.accel.y
	def mass(self):
		return self.mass
		
	def delvelx(self,velx):
		if math.fabs(self.vel.x + velx) < velocitythresh:
			self.vel.delx(velx)
		elif self.vel.x + velx > 0:
			self.vel.setx(velocitythresh)
		else: 
			self.vel.setx(-velocitythresh)
	def delvely(self,vely):
		if math.fabs(self.vel.y + vely) < velocitythresh:
			self.vel.dely(vely)
		elif self.vel.y + vely > 0:
			self.vel.sety(velocitythresh)
		else: 
			self.vel.sety(-velocitythresh)	
		
	def delaccelx(self,accelx):
		if self.accel.x < gravitythresh:
			self.accel.delx(accelx)
	def delaccely(self,accely):
		if self.accel.y < gravitythresh:
			self.accel.dely(accely)
		
	def update(self):
		self.accel.sety(gravity)
		self.vel.delx(self.accel.x)
		self.vel.dely(self.accel.y)
		if self.pos.x+self.vel.x+playerrad > width  and self.vel.x > 0:
			self.vel.setx(-collision*self.vel.x)
		if self.pos.x+self.vel.x < 0 and self.vel.x < 0:
			self.vel.setx(-collision*self.vel.x)
		if self.pos.y+self.vel.y+playerrad > length or self.pos.y+self.vel.y < menulength:
			if gravity > gravitythresh/2 and self.pos.y+self.vel.y + playerrad > length:
				self.vel.sety(0.0)
			else:
				self.vel.dely(-(1+collision)*self.vel.y)
		if math.fabs(self.vel.y) < minvelocity:
			self.vel.sety(0.0)
		if math.fabs(self.vel.x) < minvelocity:
			self.vel.setx(0.0)
		if math.fabs(self.vel.x) > velocitythresh:
			self.vel.delx(-self.vel.x + velocitythresh*self.vel.x/self.vel.x)
		if math.fabs (self.vel.y) > velocitythresh:
			self.vel.dely(-self.vel.y + velocitythresh*self.vel.y/self.vel.y)
		self.pos.delx(self.vel.x)
		self.pos.dely(self.vel.y)
		#if self.vel.x != 0:
		#	if self.vel.x < 0:
		#		self.vel.delx(airresistance*math.fabs(self.vel.x))
		#	else:
		#		self.vel.delx(-airresistance*self.vel.x)
		#if self.vel.y != 0:
		#	if self.vel.y < 0:
		#		self.vel.dely(airresistance*math.fabs(self.vel.y))
		#	else:
		#		self.vel.dely(-airresistance*self.vel.y)
		if self.pos.x + playerrad < 0 or self.pos.x + playerrad > width:
			self.pos.setx(0)
			self.vel.setx(0)
			self.pos.sety(menulength)
			self.vel.sety(0)
		if self.pos.y + playerrad < 0 or self.pos.y + playerrad > length:
			self.pos.setx(0)
			self.vel.setx(0)
			self.pos.sety(menulength)
			self.vel.sety(0)
	def bounce(self):
		self.vel.delx(-2.0*self.vel.x)
		self.vel.dely(-2.0*self.vel.y)
	def collide(self,collidermass,collidervel):
		self.vel.x = 2*collidervel.x*collidermass/(collidermass+self.mass) + self.vel.x*(self.mass - collidermass)/(collidermass + self.mass)
		self.vel.y = 2*collidervel.y*collidermass/(collidermass+self.mass) + self.vel.y*(self.mass - collidermass)/(collidermass + self.mass)
		
class Vector:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def x():
		return self.x
	def y():
		return self.y
	def delx(self,deltax):
		self.x = self.x + deltax
	def dely(self,deltay):
		self.y = self.y + deltay
	def inverse(self):
		self.x = -self.x
		self.y = -self.y
	def setx(self,x):
		self.x = x
	def sety(self,y):
		self.y = y
		
class Enemy:
	def __init__(self,pos,vel,accel,color,mass):
		self.pos = pos
		self.vel = vel
		self.accel = accel
		self.color = color
		self.mass = mass
	def getpos(self):
		return self.pos
	def getvel(self):
		return self.vel
	def getaccel(self):
		return self.accel
	def getcolor(self):
		return self.color
	def mass(self):
		return self.mass
	def bounce(self):
		self.vel.delx(-2.0*self.vel.x)
		self.vel.dely(-2.0*self.vel.y)
	def changepos(self,pos):
		self.pos = pos
	def changeaccel(self,accel):
		self.accel = accel
	def update(self):
		if self.pos.x+self.vel.x + enemyrad > width or self.pos.x+self.vel.x < 0:
			self.vel.delx(-2.0*self.vel.x)
		if self.pos.y+self.vel.y + enemyrad > length or self.pos.y+self.vel.y < menulength:
			self.vel.dely(-2.0*self.vel.y)
		if math.fabs(self.vel.y) < minvelocity:
			self.vel.dely(-self.vel.y)
		if math.fabs(self.vel.x) < minvelocity:
			self.vel.delx(-self.vel.x)
		self.pos.delx(self.vel.x)
		self.pos.dely(self.vel.y)
		self.vel.delx(self.accel.x)
		self.vel.dely(self.accel.y)
	def bounce(self):
		self.vel.delx(-2.0*self.vel.x)
		self.vel.dely(-2.0*self.vel.y)
	def collide(self,collidermass,collidervel):
		self.vel.x = 2*collidervel.x*collidermass/(collidermass+self.mass) + self.vel.x*(self.mass - collidermass)/(collidermass + self.mass)
		self.vel.y = 2*collidervel.y*collidermass/(collidermass+self.mass) + self.vel.y*(self.mass - collidermass)/(collidermass + self.mass)
		
		
class Game:
	
		pygame.init()
		BLACK    = (   0,   0,   0)
		WHITE    = ( 255, 255, 255)
		BLUE     = (   0,   0, 255)
		GREEN    = (   0, 255,   0)
		RED      = ( 255,   0,   0)
		PI = 3.141592653
		
		def RandomColor(x):
			if x == 0:
				return BLACK	
			elif x == 1:
				return WHITE
			elif x == 2:
				return BLUE
			elif x == 3:
				return GREEN
			elif x == 4:
				return RED
			else:
				return (255*random.random(),255*random.random(),255*random.random())


		size = (width, length)
		screen = pygame.display.set_mode(size)
 
		pygame.display.set_caption("Amazing Journey")

		done = False
		
		global gravity
		global collision
		global speed
		global jump

		initpos = Vector(0,menulength)
		initvel = Vector(0,0)
		initaccel = Vector(0,0)
		ball = Ball(initpos,initvel,initaccel,playermass)
		clock.tick(60)
		timeindex = 0
		timeindextwo = 0
		timeindexthree = 0
		index = 0
		anotherindex = 0
		indextwo = 0
		sliderindex = -1
		leftside = 0
		rightside = 0
		topside = 0
		font = pygame.font.Font(None, 25)
		rectone = pygame.Rect(0,0,0,0)
		recttwo = pygame.Rect(0,0,0,0)
		vectone = Vector(0,0)
		vecttwo = Vector(0,0)
		testindex = 5
	
		enemies = []
		index = 0 
		for index in range(0,numberenemies):
			enemyposvect = Vector((width - enemyrad)*random.random(),menulength + (length-menulength-enemyrad)*random.random())
			enemyvelvect = Vector(speed*random.random(),speed*random.random())
			rectone = pygame.Rect(enemyposvect.x,enemyposvect.y,enemyrad,enemyrad)
			anotherindex = 0
			if index > 0:
				while not done: 
					done = True
					rectone = pygame.Rect(enemyposvect.x,enemyposvect.y,enemyrad,enemyrad)
					indextwo = 0
					for anotherindex in range(0,index - 1):
						recttwo = pygame.Rect(enemies[anotherindex].getpos().x,enemies[anotherindex].getpos().y,enemyrad,enemyrad)
						if rectone.colliderect(recttwo):
							enemyposvect = Vector((width - enemyrad)*random.random(),menulength + (length-menulength-enemyrad)*random.random())
							rectone = pygame.Rect(enemyposvect.x,enemyposvect.y,enemyrad,enemyrad)
							done = False
						else:
							indextwo = indextwo + 1
						anotherindex = anotherindex + 1
					recttwo = pygame.Rect(ball.posx(),ball.posy(),playerrad,playerrad)
					if recttwo.colliderect(rectone):
						rectone = pygame.Rect(enemyposvect.x,enemyposvect.y,enemyrad,enemyrad)
						done = False
				done = False
			enemies.append(Enemy(Vector((width - enemyrad)*random.random(),menulength + (length-menulength-enemyrad)*random.random()),Vector(speed*random.random(),speed*random.random()),Vector(0,0),RandomColor(random.random()),enemymass))
			index = index + 1
			
		sliders = []
		sliders.append(Slider(font.render("Gravity",True,RED),Vector(0.0,0.0),0.0,gravitythresh))
		sliders.append(Slider(font.render("Speed",True,RED),Vector(sliderwidth*1.0,0.0),basespeed,velocitythresh))
		sliders.append(Slider(font.render("Collisions",True,RED),Vector(0.0,menulength/2),1.0,0.0))
		sliders.append(Slider(font.render("Jump",True,RED),Vector(sliderwidth,menulength/2),basejump,jumpmax))

		while not done:
	
			screen.fill(WHITE)
		
			for event in pygame.event.get(): # User did something
		
				if event.type == pygame.QUIT: # If user clicked close
					done = True # Flag that we are done so we exit this loop
					
				elif event.type == pygame.KEYDOWN: #Key is pressed
					if event.key == pygame.K_UP:
						if gravity > gravitythresh/2:
							ball.delvely(-jump*speed)
						else:
							ball.delvely(-speed)
					elif event.key == pygame.K_RIGHT:
						ball.delvelx(speed)
					elif event.key == pygame.K_DOWN:
						ball.delvely(speed)
					elif event.key == pygame.K_LEFT:
						ball.delvelx(-speed)
					elif event.key == pygame.K_s:
						ball.delvelx(-slowdown*ball.velx())
						ball.delvely(-slowdown*ball.vely())
						
				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					if pygame.mouse.get_pos()[1] < menulength:
						index=0
						for index in range(0, len(sliders)):
							leftside = sliders[index].getpos().x + sliderspace
							topside =  sliders[index].getpos().y + sliderspace
							rightside = sliders[index].getpos().x + sliderwidth - sliderspace
							sliderrect = pygame.Rect(sliders[index].getbarpos() + leftside - sliderbarwidth/2 + sliderspace, topside + sliderlength/2 - sliderbarlength/2, sliderbarwidth, sliderbarlength)
							if sliderrect.collidepoint(pygame.mouse.get_pos()):
								sliderindex = index
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					if sliderindex > -1:
						pos = pygame.mouse.get_pos()
						if pos[0] > sliders[sliderindex].getpos().x + sliderwidth - sliderspace:
							sliders[sliderindex].changepos(1.0*sliderwidth - 2.0*sliderspace)
						elif pos[0] < sliders[sliderindex].getpos().x + sliderspace:
							sliders[sliderindex].changepos(0.0)
						else:
							sliders[sliderindex].changepos(pos[0] - sliderbarwidth/2 - sliders[sliderindex].getpos().x + sliderspace)
						sliderindex = -1
			
			keys = pygame.key.get_pressed()  #checking pressed keys
    		#if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and keys[pygame.K_g]:
        	#		ball.delaccely(gravity)
    		#if keys[pygame.K_g] and not (keys[pygame.K_RSHIFT or pygame.K_LSHIFT]):
			#		ball.delaccely(-gravity)
			
			index = 0
			for index in range(0, len(sliders)):
				leftside = sliders[index].getpos().x + sliderspace
				topside =  sliders[index].getpos().y + sliderspace
				rightside = sliders[index].getpos().x + sliderwidth - sliderspace
				pygame.draw.rect(screen,BLACK,[leftside,topside, sliderwidth,sliderlength],2)
				pygame.draw.line(screen,BLACK, [leftside + sliderspace, topside + sliderlength/2],[rightside, topside + sliderlength/2],2)
				pygame.draw.rect(screen,BLACK, [sliders[index].getbarpos() + leftside - sliderbarwidth/2 + sliderspace, topside + sliderlength/2 - sliderbarlength/2, sliderbarwidth, sliderbarlength],0)
				screen.blit(sliders[index].getname(),[sliders[index].getpos().x + sliderwidth/2,sliders[index].getpos().y])
						
	
			pygame.draw.ellipse(screen, BLACK, [ball.posx(),ball.posy(),playerrad,playerrad],2)
			pygame.draw.rect(screen, BLACK, [0,0,width,menulength],5)
			clock.tick(60)
			time += clock.get_time()
			
			if time > timeindextwo * collisiontimefactor:
				index = 0
				for index in range(0,numberenemies):
					pygame.draw.ellipse(screen,enemies[index].getcolor(), [enemies[index].getpos().x,enemies[index].getpos().y,enemyrad,enemyrad],0)
					rectone = pygame.Rect(enemies[index].getpos().x,enemies[index].getpos().y,enemyrad,enemyrad)
					andotherindex = 0
					recttwo = pygame.Rect(ball.posx(),ball.posy(),playerrad,playerrad)
					if rectone.colliderect(recttwo):
						temp = enemies[index].getvel()
						temp = Vector(temp.x,temp.y)
						enemies[index].collide(ball.mass,ball.vel)
						ball.collide(enemies[index].mass,temp)
					for anotherindex in range(index + 1,numberenemies):
						recttwo = pygame.Rect(enemies[anotherindex].getpos().x,enemies[anotherindex].getpos().y,enemyrad,enemyrad)
						if rectone.colliderect(recttwo):
							temp = enemies[index].getvel()
							temp = Vector(temp.x,temp.y)
							enemies[index].collide(enemies[anotherindex].mass,enemies[anotherindex].getvel())
							enemies[anotherindex].collide(enemies[index].mass,temp)
						anotherindex = anotherindex + 1
					index = index + 1
				timeindextwo = timeindextwo + 1
			
			if time > timeindexthree * otherfactor:
				if keys[pygame.K_s]:
					ball.delvelx(-slowdown*ball.velx())
					ball.delvely(-slowdown*ball.vely())
				timeindexthree = timeindexthree + 1
					
			if time > timeindex * timefactor:
				ball.update()
				index = 0
				for index in range(0,numberenemies):
					enemies[index].update()
					index = index + 1
				timeindex = timeindex + 1
			jump = sliders[3].update()
			collision = sliders[2].update()
			gravity = sliders[0].update()
			ball.delaccely(gravity-ball.accely())
			speed = sliders[1].update()
			temp = math.sqrt(ball.velx()*ball.velx() + ball.vely()*ball.vely())
			temp = 'Velocity = '.join(['',str(temp)])
			screen.blit(font.render(temp,True,RED),[width - 200,length - 50])
			pygame.display.flip()
		pygame.quit() 