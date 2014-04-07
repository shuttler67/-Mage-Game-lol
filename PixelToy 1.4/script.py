#!/git/-Mage-Game-lol/PixelToy\ 1.4

import math

from astar import *
from utilities import *

epicface = loadImage('res/epicface.png')
fireball = loadImage('res/Fireball.png')
floor = loadImage('res/floor.png')
mails = ['res/mail4.png','res/mail1.png','res/mail2.png','res/mail5.png','res/mail6.png']
mail4=loadImage('res/postcard.png')
backgroundWidth = 510
backgroundHeight = 510

still = loadImage('res/postmanstill.png')
still2 = loadImage('res/postmanstill2.png')
charge1 = loadImage('res/postmancharge1.png')
charge2 = loadImage('res/postmancharge2.png')
walk1 = loadImage('res/postmanwalk1.png')
walk2 = loadImage('res/postmanwalk2.png')
walk3 = loadImage('res/postmanwalk3.png')
walk4 = loadImage('res/postmanwalk4.png')

RIGHT = "right"
LEFT  = "left"
UP    = "up"
DOWN  = "down"
NIL = 'nil'

MAXSPEED = 2.7
MANSIZE = 60
CAMERASLACKX=250
CAMERASLACKY=200
KEYSTATES ={}
FRAMECOUNT = 0
allKeysUsed =('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','shift','tab','space','escape')

# Colours
#		 R G B Alpha
RED = (255, 0 , 0 ,255)
GREEN = ( 0 ,200, 30 ,255)
BLACK = ( 0 , 0 , 0 ,255)
BLUE = (0, 0 , 200 ,255)
GREY = (64,64,64,255)
WHITE = (255,255,255,255)



#Button class

#Wall class
class Wall:
	def __init__(self,x,y,w,h):
		self.rect = Rect(x,y,w*10,h*10)
	def playerCollide(self,playerx,playery,playerSize):
		canNotMoves = []
		movedx = playerx
		movedy = playery
		playerDirections = [RIGHT,LEFT,UP,DOWN]
		for direction in playerDirections:
			if direction == RIGHT:
				movedx = playerx + MAXSPEED
			if direction == LEFT:
				movedx = playerx - MAXSPEED
			if direction == UP:
				movedy = playery + MAXSPEED
			if direction == DOWN:
				movedy = playery - MAXSPEED

			if self.rect.rectCollide(Rect(movedx-(playerSize/6),movedy-(playerSize/2),playerSize/3,playerSize)):
				canNotMoves.append(direction)
			movedx = playerx
			movedy = playery
		return canNotMoves
	def draw(self,cameraX,cameraY):
		useColourList(GREEN)
		drawRectangle(self.rect.x1-cameraX,self.rect.y1-cameraY,self.rect.width,self.rect.height)

#Wall class

#Projectile class
class Projectile:
	def __init__(self,x,y,tx,ty,image):
		self.projSpeed = 2.7
		if round(random()) == 0:
			spin = -10
		else: spin = 10
		self.rotateSpeed = spin
		self.size = 20
		self.image = image
		self.image.setRotation(int(random()*360))
		self.x = x
		self.y = y
		self.cosine, self.sine = findTrajectory(self.x,self.y,tx,ty)
	def move(self):
		self.x += self.cosine*self.projSpeed
		self.y += self.sine*self.projSpeed
	def draw(self,cameraX,cameraY,pause):
		useColour(255,0,0,100)
		if not pause:
			self.image.rotate(self.rotateSpeed) 
		drawImage(self.image,self.x-cameraX,self.y-cameraY,self.size,self.size)
	def checkIfOut(self,cameraX,cameraY):
		return self.x-cameraX < -self.size or self.x-cameraX > _screenWidth+self.size or self.y-cameraY < -self.size or self.y-cameraY > _screenHeight+self.size
	def checkIfCollide(self,rect):
		return rect.rectCollide(Rect(self.x,self.y,0,0))
#Projectile class


class Entity:
	def __init__(self,maxHealth,x,y,size):
		self.x = x
		self.y = y
		self.speedx = 0
		self.speedy = 0
		self.size = size
		self.maxHealth = maxHealth
		self.health = self.maxHealth
		self.directions = []
	def move(self,canNotMoves,accelerationX,accelerationY):
		if self.speedx < 0.001 and self.speedx > -0.001 and self.speedx != 0:
			self.speedx = 0
		if self.speedy < 0.001 and self.speedy > -0.001 and self.speedx != 0:
			self.speedy = 0
		
		self.speedy *= 0.9
		self.speedx *= 0.9
		self.speedy += accelerationY
		self.speedx += accelerationX
		self.directions = []
		if self.speedx > 0:
			self.directions.append(RIGHT)
		if self.speedx < 0:
			self.directions.append(LEFT)
		if self.speedy > 0:
			self.directions.append(UP)
		if self.speedy < 0:
			self.directions.append(DOWN)
		for direction in self.directions:
			for canNotMove in canNotMoves:
				if canNotMove == direction:
					if canNotMove == UP or canNotMove == DOWN:
						self.speedy = 0.0
					if canNotMove == RIGHT or canNotMove == LEFT:
						self.speedx = 0.0		
		self.x += self.speedx
		self.y += self.speedy
#Enemies
class Enemy(Entity):
	def __init__(self,maxHealth,x,y,size,minAttackDamage,maxAttackDamage,radar):	
		Entity.__init__(self,maxHealth-10+random()*10,x,y,size)
		self.minAttackDamage = minAttackDamage
		self.maxAttackDamage = maxAttackDamage
		self.radar = radar
		self.astar = AStar()
		self.isWandering = True

	def followPath(self, path = None):
		if path != None:
			self.pathIter = iter(path)
			node = self.pathIter.next()
			self.currentNode = (node[0]*30,node[1]*30)
		if circleVScircle(self.currentNode[0],self.currentNode[1],25,self.x,self.y,0):
			self.currentNode = self.pathIter.next()
		
		self.walkTowards(self.currentNode)
		
	def wander(self):
		global FRAMECOUNT

	def update(self,playerPos,canMoveTo):
		#global FRAMECOUNT
		if circleVScircle(playerPos[0],playerPos[1],MANSIZE/2,self.x,self.y,self.radar):
			if self.isWandering:
				path = self.astar.findPath((int(self.x/30),int(self.y/30)),(int(playerPos[0]/30),int(playerPos[1]/30)),canMoveTo)
				self.followPath(path)
				self.isWandering = False
			elif FRAMECOUNT%15 == 0:
				path = self.astar.findPath((int(self.x/30),int(self.y/30)),(int(playerPos[0]/30),int(playerPos[1]/30)),canMoveTo)
				self.followPath(path)
			else:
				self.followPath()
		else:
			self.isWandering = True
			self.wander()

	def walkTowards(self,posTuple):
		cos, sin = findTrajectory(self.x,self.y,*posTuple)
		Entity.move(self,[],cos*0.2,sin*0.2)

	def draw(self,cameraX, cameraY):
		useColourList(GREY)
		drawRectangle(self.x-cameraX-self.size/2,self.y-cameraY+self.size/2,self.size,10)
		useColourList(RED)
		drawRectangle(self.x-cameraX-self.size/2+2,self.y-cameraY+self.size/2+2, self.health/self.maxHealth*(self.size-4), 6)
		
class meleeEnemy(Enemy):
	def __init__(self,maxHealth,x,y,size,minAttackDamage,maxAttackDamage,knockback,radar):	
		Enemy.__init__(self,maxHealth-10+random()*10,x,y,size,minAttackDamage,maxAttackDamage,radar)
		self.knockback = knockback
	def touchAttack(self,player):
		if circleVScircle(player.x,player.y,MANSIZE/2,self.x,self.y,self.size/2):
			player.speedx = (player.x-self.x)*self.knockback
			player.speedy = (player.y-self.y)*self.knockback
			self.speedx = 0
			self.speedy = 0
			player.health -= self.minAttackDamage+random()*(self.maxAttackDamage-self.minAttackDamage)
			self.isWandering = True
	def draw(self,cameraX, cameraY):
		drawImage(epicface,self.x-cameraX,self.y-cameraY,self.size,self.size)
		Enemy.draw(self,cameraX, cameraY)
		
	
#Enemies

#PLAY WITH MEEEEE class
class Player(Entity):
	def __init__(self):
		Entity.__init__(self,200.0,0,0,MANSIZE)
		self.inAttack = False
		self.maxMana = 100.0
		self.mana = self.maxMana
		self.isMoving = False
		self.facing = RIGHT
#	def 
	def move(self,canNotMoves):
		accelerationY = 0
		accelerationX = 0
		if self.inAttack:
			movement = 0.1
		else:
			movement = 0.3
				
		if KEYSTATES['w']:
			accelerationY += movement
		if KEYSTATES['a']:
			accelerationX -= movement
		if KEYSTATES['s']:
			accelerationY -= movement
		if KEYSTATES['d']:
			accelerationX += movement

		self.isMoving = KEYSTATES['w'] or KEYSTATES['a'] or KEYSTATES['s'] or KEYSTATES['d']

		Entity.move(self,canNotMoves,accelerationX,accelerationY)

	def draw(self,cameraX,cameraY):
		global FRAMECOUNT
		if self.facing == RIGHT and LEFT in self.directions:
			self.facing = LEFT
		if self.facing == LEFT and RIGHT in self.directions:
			self.facing = RIGHT
			
		if self.inAttack:
			if FRAMECOUNT%30<15:
				drawImage(charge1,self.x-cameraX,self.y-cameraY,MANSIZE,MANSIZE)
			else:
				drawImage(charge2,self.x-cameraX,self.y-cameraY,MANSIZE,MANSIZE)
		elif self.isMoving:
			if self.facing == RIGHT:
				if FRAMECOUNT%30>15:
					drawImage(walk3,self.x-cameraX,self.y-cameraY,MANSIZE,MANSIZE)
				else:
					drawImage(walk4,self.x-cameraX,self.y-cameraY,MANSIZE,MANSIZE)
			if self.facing == LEFT:
				if FRAMECOUNT%30<15:
					drawImage(walk1,self.x-cameraX,self.y-cameraY,MANSIZE,MANSIZE)
				else:
					drawImage(walk2,self.x-cameraX,self.y-cameraY,MANSIZE,MANSIZE)

		else:
			if self.facing == LEFT:
				drawImage(still,self.x-cameraX,self.y-cameraY,MANSIZE,MANSIZE)
			else:
				drawImage(still2,self.x-cameraX,self.y-cameraY,MANSIZE,MANSIZE)

#Player class

#GUI class

class GUI:
	def __init__(self):
		self.buttons = [Button(0,_screenHeight-35,100,'pause','pause')]
	def update(self,pause):
		if pause:
			self.buttons = [Button(_screenWidth/2-100,_screenHeight/2,200,'resume game','unpause'),Button(_screenWidth/2-100,_screenHeight/2-35,200,'main menu',NIL)]
		else:
			self.buttons = [Button(0,_screenHeight-35,100,'pause','pause')]
	def handleMouseUp(self):
		returnValue = NIL
		overButton = False
		for button in self.buttons:
			if button.isUnderMouse((_mouseX,_mouseY)):
				overButton = True
				returnValue = button.returnValue
		return returnValue, overButton
	def drawButtons(self):
		for button in self.buttons:
			button.draw((_mouseX,_mouseY))
	def draw(self,health,mana,maxHealth,maxMana):
		barWidth = _screenWidth/3
		useColourList(GREY)
		drawRectangle(_screenWidth/2-barWidth/2,_screenHeight-19,barWidth,17)
		drawRectangle(_screenWidth/2-barWidth/2,_screenHeight-37,barWidth,17)

		useColourList(RED)
		drawRectangle(_screenWidth/2-barWidth/2+3, _screenHeight-17, health/maxHealth*(barWidth-4), 13)
		useColourList(BLUE)
		drawRectangle(_screenWidth/2-barWidth/2+2,_screenHeight-35,mana/maxMana*(barWidth-4), 13)

		useColourList(WHITE)
		drawString(_screenWidth/2-len(str(int(health)))*6,_screenHeight-18,str(int(health)))
		drawString(_screenWidth/2-len(str(int(mana)))*6,_screenHeight-36,str(int(mana)))
#GOOEY class

#Level Up! class
class Level:
	def __init__(self,levelDICT): 
		self.walls = levelDICT["WALLS"]
		self.enemies = levelDICT["ENEMIES"]
		self.proj = []
	@staticmethod
	def canNotMove(node):
		return True
	def handleObjects(self,player,cameraX,cameraY):
		canNotMoves = []		
				
		for wall in self.walls:
			canNotMoves += wall.playerCollide(player.x,player.y,MANSIZE)
			for i in range(len(self.proj)-1, -1, -1):
				projectile = self.proj[i]
				projectile.move()
				if projectile.checkIfOut(cameraX,cameraY) or projectile.checkIfCollide(wall.rect):
					del self.proj[i]
		for enemy in self.enemies:
			enemy.update((player.x,player.y),self.canNotMove)
			enemy.touchAttack(player)
			for i in range(len(self.proj)-1, -1, -1):
				if circleVScircle(self.proj[i].x,self.proj[i].y,self.proj[i].size/2,enemy.x,enemy.y,enemy.size/2):
					del self.proj[i]
					enemy.health -= random()*(10-5)+5

		return canNotMoves

	def spawnProjectile(self,overButtons,manX,manY,cameraX,cameraY):
		random1 = int(random()*len(mails))
		mail = loadImage(mails[random1])
	#
		if not overButtons:
			self.proj.append(Projectile(manX,manY,_mouseX+cameraX,_mouseY+cameraY,mail))
	def drawLevel(self,cameraX,cameraY,pause):
		for i in range(0,9):
			for j in range(0,9):
				drawImage(floor, (j*backgroundWidth)-cameraX, (i*backgroundHeight)-cameraY, backgroundWidth,backgroundHeight)
		for wall in self.walls:
			wall.draw(cameraX,cameraY)

		for projectile in self.proj:
			projectile.draw(cameraX,cameraY,pause)

		for enemy in self.enemies:
			enemy.draw(cameraX,cameraY)
#Level class

class Game:
	def __init__(self):
		self.man = Player()
		self.cameraX= -_screenWidth/2
		self.cameraY= -_screenHeight/2
		self.mousedown = False
		self.currentLevel = Level(LEVELS[0])
		self.GUI = GUI()
		self.pause = False
	def gameLoop(self):	
		for key in allKeysUsed:
			KEYSTATES[key]= isKeyDown(key)
		self.update()
		self.draw()

	def update(self):
		firstMousedown = False
		firstMouseup = False
			
		if isLeftMouseDown() and not self.mousedown:
			firstMousedown = True
			self.mousedown = True
		if not isLeftMouseDown() and self.mousedown:
			firstMouseup = True
			self.mousedown = False

		if not self.pause:
			canNotMoves = self.currentLevel.handleObjects(self.man,self.cameraX,self.cameraY)
			self.man.inAttack = self.mousedown
			self.man.move(canNotMoves)

		self.GUI.update(self.pause)

		if firstMouseup:
			returnValue,overButtons = self.GUI.handleMouseUp()
			if returnValue == 'pause':
				self.pause = True
			if returnValue == 'unpause':
				self.pause = False
			if not self.pause:
				self.currentLevel.spawnProjectile(overButtons,self.man.x,self.man.y,self.cameraX,self.cameraY)
				
		if self.man.x-self.cameraX > (_screenWidth-CAMERASLACKX) or self.man.x-self.cameraX < CAMERASLACKX:
			self.cameraX+=self.man.speedx
								
		if self.man.y-self.cameraY > (_screenHeight-CAMERASLACKY) or self.man.y-self.cameraY < CAMERASLACKY:
			self.cameraY+=self.man.speedy
	def draw(self):
		self.currentLevel.drawLevel(self.cameraX,self.cameraY,self.pause)
		self.man.draw(self.cameraX, self.cameraY)
		self.GUI.draw(self.man.health,self.man.mana,self.man.maxHealth,self.man.maxMana)
		
		if self.pause:
			useColour(0,0,0,130)
			drawRectangle(0,0,_screenWidth,_screenHeight)
			drawImage(mail4,_screenWidth/2,_screenHeight/2,_screenWidth/2,_screenWidth/2)
			
		self.GUI.drawButtons()	
		
		
#Wall((POS),SIZE) ENEMY(HEALTH;(POS);SIZE;(ATCK DMG),KNOCKBACK;RADAR)
LEVELS= [{"WALLS":[Wall(100,100,10,1),Wall(200,100,1,10)],"ENEMIES":[meleeEnemy(100,300,300,60,5,20,0.1,500)]}]

game = Game()
while True:
	PREVIOUSscreenHeight = _screenHeight
	newFrame()
	FRAMECOUNT += 1
	
	game.gameLoop()
								

