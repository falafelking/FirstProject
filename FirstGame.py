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
sliderspace = 5
sliderlength = menulength/3 - 2*sliderspace
slidernumber = 5
sliderrows = 2
sliderbarlength = 10
sliderbarwidth = 10
sliderwidth = width/sliderrows - 2*sliderspace
buttonwidth = 20
buttonlength = sliderlength
buttonspace = 30
playerrad = 100
numberenemies = 0
enemymax = 20
enemyrad = 50
enemymass = 10
playermass = 40
speed = 5.0
slowdown = .5
basespeed = 5.0
gravity = 0.0
gravitythresh = 5.0
velocitythresh = 50
minvelocity = .1
friction = .5
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
		self.temp = self.min + ( self.barpos /( 1.0 * ( sliderwidth - 2*sliderspace ) ) ) * ( self.max - self.min )
		return self.temp
		
class Button: 
	def __init__(self,name,pos,bool):
		self.pos = pos
		self.bool = bool
		self.name = name
	
	def pos(self):
		return self.pos
	def bool(self):
		return self.bool
	def name(self):
		return self.name
		
	def clicked(self):
		if self.bool:
			self.bool = False
		else:
			self.bool = True
	
class Ball:
	def __init__(self,pos,vel,accel,color,mass,rad):
		self.pos = pos
		self.vel = vel
		self.accel = accel
		self.mass = mass
		self.color = color
		self.rad = rad
		
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
	def pos(self):
		return self.pos
	def accelx(self):
		return self.accel.x
	def accely(self):
		return self.accel.y
	def mass(self):
		return self.mass
	def color(self):
		return self.color
	def rad(self):
		return self.rad
		
	def againstwall(self):
		if self.pos.x + self.rad > width or self.pos.x < 0:
			return True
		elif self.pos.y + self.rad > length or self.pos.y < menulength:
			return True
		else:
			return False
			
	def setvelx(self,velx):
		self.vel.setx(velx)
	def setvely(self,vely):
		self.vel.sety(vely)
		
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
		
	def forcex(self,forcex):
		if self.accel.x < gravitythresh:
			self.accel.delx(forcex/self.mass)
	def forcey(self,forcey):
		if self.accel.y < gravitythresh:
			self.accel.dely(forcey/self.mass)
		
	def update(self):
		self.accel.sety(gravity)
		self.vel.delx(self.accel.x)
		self.vel.dely(self.accel.y)
		if self.pos.x+self.vel.x + self.rad > width  and self.vel.x > 0:
			self.vel.setx(-collision*self.vel.x)
		if self.pos.x+self.vel.x < 0 and self.vel.x < 0:
			self.vel.setx(-collision*self.vel.x)
		if self.pos.y+self.vel.y+self.rad > length or self.pos.y+self.vel.y < menulength:
			if gravity > gravitythresh/2 and self.pos.y+self.vel.y + self.rad > length:
				self.vel.sety(0.0)
			else:
				self.vel.dely(-(1+collision)*self.vel.y)
		if math.fabs(self.vel.y) < minvelocity:
			self.vel.sety(0.0)
		if math.fabs(self.vel.x) < minvelocity:
			self.vel.setx(0.0)
		if math.fabs(self.vel.x) > velocitythresh:
			self.vel.setx(velocitythresh*self.vel.x/(math.fabs(self.vel.x)))
		if math.fabs(self.vel.y) > velocitythresh:
			self.vel.sety(velocitythresh*self.vel.y/math.fabs(self.vel.y))
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
		if self.pos.x < 0 or self.pos.x + self.rad > width:
			self.pos.setx(0)
			self.vel.setx(0)
			self.pos.sety(menulength)
			self.vel.sety(0)
		if self.pos.y < menulength or self.pos.y + self.rad > length:
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
		if self.pos.x + self.vel.x < 0 or self.pos.x + self.vel.x + self.rad > width:
			self.vel.setx(0)
		if self.pos.y + self.vel.y < menulength or self.pos.y + self.vel.y + self.rad > length:
			self.vel.sety(0)
			
	def collidewall(self,collidermass,collidervel):
		if self.pos.x < 0 or self.pos.x + self.rad > width:
			return self.pos
		 	
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
		
		global numberenemeies
		global gravity
		global collision
		global speed
		global jump

		initpos = Vector(0,menulength)
		initvel = Vector(0,0)
		initaccel = Vector(0,0)
		ball = Ball(initpos,initvel,initaccel,BLACK,playermass,playerrad)
		clock.tick(60)
		timeindex = 0
		timeindextwo = 0
		timeindexthree = 0
		index = 0
		anotherindex = 0
		indextwo = 0
		sliderindex = -1
		buttonindex = -1
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
		
		buttons = []
		buttons.append(Button("Kick",Vector(sliderwidth,menulength*2/3),False))
			
		sliders = []
		sliders.append(Slider(font.render("Gravity",True,RED),Vector(0.0,0.0),0.0,gravitythresh))
		sliders.append(Slider(font.render("Speed",True,RED),Vector(sliderwidth*1.0,0.0),basespeed,velocitythresh))
		sliders.append(Slider(font.render("Collisions",True,RED),Vector(0.0,menulength/3),1.0,0.0))
		sliders.append(Slider(font.render("Jump",True,RED),Vector(sliderwidth,menulength/3),basejump,jumpmax))
		sliders.append(Slider(font.render("Number of Enemies",True,RED),Vector(0.0,menulength*2/3),0,enemymax))
		
		def checkforcollisions(enemies,ball):
			index = 0
			for index in range(0,len(enemies)):
				rectone = pygame.Rect(enemies[index].pos.x,enemies[index].pos.y,enemyrad,enemyrad)
				andotherindex = 0
				recttwo = pygame.Rect(ball.posx(),ball.posy(),playerrad,playerrad)
				if rectone.colliderect(recttwo):
					if not ball.againstwall():
						temp = enemies[index].vel
						temp = Vector(temp.x,temp.y)
						enemies[index].collide(ball.mass,ball.vel)
						ball.collide(enemies[index].mass,temp)
					else:
						enemies[index].bounce()
				for anotherindex in range(index + 1,len(enemies)):
					recttwo = pygame.Rect(enemies[anotherindex].pos.x,enemies[anotherindex].pos.y,enemyrad,enemyrad)
					if rectone.colliderect(recttwo):
						if not enemies[anotherindex].againstwall():
							temp = enemies[index].vel
							temp = Vector(temp.x,temp.y)
							enemies[index].collide(enemies[anotherindex].mass,enemies[anotherindex].vel)
							enemies[anotherindex].collide(enemies[index].mass,temp)
						else: 
							enemies[index].bounce()
					anotherindex = anotherindex + 1
				index = index + 1
				
		def checkenemynumber(enemies,ball,update):
			done = False
			numberenemies = int(round(update))
			index = len(enemies)
			while len(enemies) < numberenemies:
				index = len(enemies)
				for index in range(0,numberenemies):
					enemyposvect = Vector((width - enemyrad)*random.random(),menulength + (length-menulength-enemyrad)*random.random())
					enemyvelvect = Vector(speed*random.random(),speed*random.random())
					rectone = pygame.Rect(enemyposvect.x,enemyposvect.y,enemyrad,enemyrad)
					anotherindex = 0
					if index > 0:
						while done == False: 
							done = True
							for anotherindex in range(0,len(enemies)):
								recttwo = pygame.Rect(enemies[anotherindex].pos.x - sliderspace,enemies[anotherindex].pos.y - sliderspace,enemyrad + 2*sliderspace,enemyrad + 2*sliderspace)
								if rectone.colliderect(recttwo):
									enemyposvect = Vector((width - enemyrad)*random.random(),menulength + (length-menulength-enemyrad)*random.random())
									rectone = pygame.Rect(enemyposvect.x,enemyposvect.y,enemyrad,enemyrad)
									done = False
								anotherindex = anotherindex + 1
							recttwo = pygame.Rect(ball.posx() - sliderspace,ball.posy() + sliderspace,playerrad + 2*sliderspace,playerrad + 2*sliderspace)
							if recttwo.colliderect(rectone):
								enemyposvect = Vector((width - enemyrad)*random.random(),menulength + (length-menulength-enemyrad)*random.random())
								rectone = pygame.Rect(enemyposvect.x,enemyposvect.y,enemyrad,enemyrad)
								done = False
					enemies.append(Ball(enemyposvect,Vector(speed*random.random(),speed*random.random()),Vector(0,0),(255*random.random(),255*random.random(),255*random.random()),enemymass,enemyrad))
					index = index + 1
			while len(enemies) > numberenemies:
				enemies.pop(len(enemies) - 1)
			

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
							sliderbarrect = pygame.Rect(sliders[index].getbarpos() + leftside - sliderbarwidth/2 + sliderspace, topside + sliderlength/2 - sliderbarlength/2, sliderbarwidth, sliderbarlength)
							sliderrect = pygame.Rect(leftside,topside, sliderwidth,sliderlength)
							if sliderbarrect.collidepoint(pygame.mouse.get_pos()):
								sliderindex = index
							elif sliderrect.collidepoint(pygame.mouse.get_pos()):
								pos = pygame.mouse.get_pos()
								if pos[0] > sliders[index].getpos().x + sliderwidth - 2*sliderspace:
									sliders[index].changepos(sliderwidth - 2*sliderspace)
								elif pos[0] < sliders[index].getpos().x + 2*sliderspace:
									sliders[index].changepos(0.0)
								else:
									sliders[index].changepos(pos[0] - sliderbarwidth/2 - sliders[index].getpos().x - sliderspace)
									
						index = 0
						for index in range(0,len(buttons)):
							namewidth, nameheight = font.size(buttons[index].name)
							leftside = buttons[index].pos.x + sliderspace + namewidth + buttonspace
							topside = buttons[index].pos.y + sliderspace
							buttonrect = pygame.Rect(leftside,topside,buttonwidth,buttonlength)
							if buttonrect.collidepoint(pygame.mouse.get_pos()):
								buttonindex = index
								
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					if sliderindex > -1:
						pos = pygame.mouse.get_pos()
						if pos[0] > sliders[sliderindex].getpos().x + sliderwidth - 2*sliderspace:
							sliders[sliderindex].changepos(sliderwidth - 2*sliderspace)
						elif pos[0] < sliders[sliderindex].getpos().x + 2*sliderspace:
							sliders[sliderindex].changepos(0.0)
						else:
							sliders[sliderindex].changepos(pos[0] - sliderbarwidth/2 - sliders[sliderindex].getpos().x - sliderspace)
						sliderindex = -1
					
					if buttonindex > -1:
						namewidth, nameheight = font.size(buttons[buttonindex].name)
						leftside = buttons[buttonindex].pos.x + sliderspace + namewidth + buttonspace
						topside = buttons[buttonindex].pos.y + sliderspace
						buttonrect = pygame.Rect(leftside,topside,buttonwidth,buttonlength)
						if buttonrect.collidepoint(pygame.mouse.get_pos()):
							buttons[buttonindex].clicked()
						buttonindex = -1
			
			keys = pygame.key.get_pressed()  #checking pressed keys
    		#if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and keys[pygame.K_g]:
        	#		ball.forcey(gravity)
    		#if keys[pygame.K_g] and not (keys[pygame.K_RSHIFT or pygame.K_LSHIFT]):
			#		ball.forcey(-gravity)
			
			index = 0
			for index in range(0, len(sliders)):
				leftside = sliders[index].getpos().x + sliderspace
				topside =  sliders[index].getpos().y + sliderspace
				rightside = sliders[index].getpos().x + sliderwidth - sliderspace
				pygame.draw.rect(screen,BLACK,[leftside,topside, sliderwidth,sliderlength],2)
				pygame.draw.line(screen,BLACK, [leftside + sliderspace, topside + sliderlength/2],[rightside + sliderspace, topside + sliderlength/2],2)
				pygame.draw.rect(screen,BLACK, [sliders[index].getbarpos() + leftside - sliderbarwidth/2 + sliderspace, topside + sliderlength/2 - sliderbarlength/2, sliderbarwidth, sliderbarlength],0)
				screen.blit(sliders[index].getname(),[sliders[index].getpos().x + sliderwidth/2,sliders[index].getpos().y])
			
			index = 0
			for index in range(0, len(buttons)):
				namewidth, nameheight = font.size(buttons[index].name)
				leftside = buttons[index].pos.x + sliderspace + namewidth + buttonspace
				topside = buttons[index].pos.y + sliderspace
				pygame.draw.rect(screen,BLACK,[leftside,topside,buttonwidth,buttonlength],2)
				screen.blit(font.render(buttons[index].name,True,RED),[leftside - namewidth,topside])
				
			if sliderindex > -1:
				pos = pygame.mouse.get_pos()
				if pos[0] > sliders[sliderindex].getpos().x + sliderwidth - 2*sliderspace:
					sliders[sliderindex].changepos(sliderwidth - 2*sliderspace)
				elif pos[0] < sliders[sliderindex].getpos().x + 2*sliderspace:
					sliders[sliderindex].changepos(0.0)
				else:
					sliders[sliderindex].changepos(pos[0] - sliderbarwidth/2 - sliders[sliderindex].getpos().x - sliderspace)
	
			pygame.draw.ellipse(screen, BLACK, [ball.posx(),ball.posy(),playerrad,playerrad],2)
			pygame.draw.rect(screen, BLACK, [0,0,width,menulength],5)
			clock.tick(60)
			time += clock.get_time()

			if buttons[0].bool:
				rand = random.uniform(-1.0,1.0)
				ball.delvely(speed*rand)
				rand = random.uniform(-1.0,1.0)
				ball.delvelx(speed*rand)
				index = 0
				for index in range(0,len(enemies)):
					rand = random.uniform(-1.0,1.0)
					enemies[index].setvely(speed*rand)
					rand = random.uniform(-1.0,1.0)
					enemies[index].setvelx(speed*rand)
				buttons[0].clicked()
			
			if time > timeindextwo * collisiontimefactor:
				checkforcollisions(enemies,ball)
				timeindextwo = timeindextwo + 1
				
			if time > timeindexthree * otherfactor:
				if keys[pygame.K_s]:
					ball.delvelx(-slowdown*ball.velx())
					ball.delvely(-slowdown*ball.vely())
				timeindexthree = timeindexthree + 1
		
			temp = math.sqrt(ball.velx()*ball.velx() + ball.vely()*ball.vely())
			if time > (timeindexthree * (otherfactor/8)):
				temp = 'Velocity = '.join(['',str(temp)])
				
			if time > timeindex * timefactor:
				checkenemynumber(enemies,ball,sliders[4].update())
				numberenemies = int(round(sliders[4].update()))
				ball.update()
				index = 0
				for index in range(0,numberenemies):
					pygame.draw.ellipse(screen,enemies[index].color, [enemies[index].pos.x,enemies[index].pos.y,enemyrad,enemyrad],0)
					enemies[index].update()
					index = index + 1
				timeindex = timeindex + 1
			jump = sliders[3].update()
			collision = sliders[2].update()
			gravity = sliders[0].update()
			ball.forcey(gravity-ball.accely()*ball.mass)
			screen.blit(font.render(temp,True,RED),[width - 200,length - 50])
			speed = sliders[1].update()
			pygame.display.flip()
		pygame.quit() 