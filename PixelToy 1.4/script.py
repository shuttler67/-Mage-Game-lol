import math

epicface = loadImage('res/epicface.png')
fireball = loadImage('res/Fireball.png')
marblefloor = loadImage('res/marblefloor.png')
buttonUp = loadImage('res/buttonUp.png')
buttonDown = loadImage('res/buttonDown.png')
backgroundWidth = 384
backgroundHeight = 384

man1 = loadImage('res/man1.png')
man2 = loadImage('res/man2.png')

RIGHT = "right"
<<<<<<< HEAD
LEFT  = "left"
UP    = "up"
DOWN  = "down"
=======
LEFT = "left"
UP = "up"
DOWN = "down"
NIL = "nil"
RESUME= "resume"
PAUSE = "pause"
>>>>>>> 6be2dfb349d271f5e151182a2d4c9fb6c5b573ae

MAXSPEED = 2.7
MANSIZE = 60
CAMERASLACKX=250
CAMERASLACKY=200
KEYSTATES ={}
allKeysUsed =('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','shift','tab','space','escape')

# Colours
#		 R G B Alpha
RED = (255, 0 , 0 ,255)
GREEN = ( 0 ,255, 0 ,255)
BLACK = ( 0 , 0 , 0 ,255)

#Utilities
class Rect:
	def __init__(self,x,y,w,h):
		self.x1 = x
		self.y1 = y
		self.x2 = x+w
		self.y2 = y+h
		self.width = w
		self.height = h
	def rectCollide(self,rect2):
		if rect2.x1>self.x1 and rect2.x1<self.x2 and rect2.y1>self.y1 and rect2.y1<self.y2:
			return True
		if rect2.x2>self.x1 and rect2.x2<self.x2 and rect2.y1>self.y1 and rect2.y1<self.y2:
			return True
		if rect2.x1>self.x1 and rect2.x1<self.x2 and rect2.y2>self.y1 and rect2.y2<self.y2:
			return True
		if rect2.x2>self.x1 and rect2.x2<self.x2 and rect2.y2>self.y1 and rect2.y2<self.y2:
			return True
				
		if self.x1>rect2.x1 and self.x1<rect2.x2 and self.y1>rect2.y1 and self.y1<rect2.y2:
			return True
		if self.x2>rect2.x1 and self.x2<rect2.x2 and self.y1>rect2.y1 and self.y1<rect2.y2:
			return True
		if self.x1>rect2.x1 and self.x1<rect2.x2 and self.y2>rect2.y1 and self.y2<rect2.y2:
			return True
		if self.x2>rect2.x1 and self.x2<rect2.x2 and self.y2>rect2.y1 and self.y2<rect2.y2:
			return True
		return False

def useColourList(colour):
		useColour(colour[0],colour[1],colour[2],colour[3])

def drawRect(rect):
		drawRectangle(self.rect.x1,self.rect.y1,self.rect.width,self.rect.height)

def drawImageRect(image,rect):
		drawImage(image,rect.x1+rect.width/2,rect.y1+rect.height/2,rect.width,rect.height)
#Utilities

#Button class
class Button:

	def __init__(self,x,y,width,text,returnValue):
		self.rect = Rect(x,y,width,35)
		self.text = text
		self.returnValue = returnValue
	def isUnderMouse(self):
		return self.rect.rectCollide(Rect(_mouseX,_mouseY,0,0)) #checking if mouse is over button
	def draw(self):
		useColourList(BLACK)
		if isLeftMouseDown() and self.isUnderMouse():						
			drawImageRect(buttonDown,self.rect)
			drawString(self.rect.x1+self.rect.width/2-len(self.text)*6,self.rect.y1+11,self.text)
		else:
			drawImageRect(buttonUp,self.rect)
			drawString(self.rect.x1+self.rect.width/2-len(self.text)*6,self.rect.y1+13,self.text)

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

			if self.rect.rectCollide(Rect(movedx-(playerSize/2),movedy-(playerSize/2),playerSize,playerSize)):
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
	def __init__(self):
		self.notIdle = False
		self.projSpeed = 2
	def update(self,size,notIdle,x,y,tx,ty):
		self.x = x
		self.y = y
		self.a = ty-self.y
		self.b = tx-self.x
		self.d = math.hypot(self.b,self.a)
		self.notIdle = notIdle
		self.size = size
	def move(self):
		if self.notIdle:
			self.x += self.b/self.d*self.projSpeed
			self.y += self.a/self.d*self.projSpeed
	def draw(self,cameraX,cameraY):
		useColour(255,0,0,100)
		fireball.rotate(-2)
		drawImage(fireball,self.x-cameraX,self.y-cameraY,self.size*2,self.size*2)
	def checkIfOut(self,cameraX,cameraY):
		if self.x-cameraX < -self.size or self.x-cameraX > _screenWidth+self.size or self.y-cameraY < -self.size or self.y-cameraY > _screenHeight+self.size and self.notIdle:
			return True
		else:
			return False
	def checkIfCollide(self,rect):
		if rect.rectCollide(Rect(self.x,self.y,0,0)) and self.notIdle:
			return True
		else:
			return False
#Projectile class

#Enemies
class Enemy:
	def __init__(self,maxHealth,x,y,detectRange,size,minAttackDamage,maxAttackDamage):	
		self.maxHealth = maxHealth-10+random()*10
		self.health = self.maxHealth
		self.x = x
		self.y = y
		self.speedx = 0
		self.speedy = 0
		self.detectRange = detectRange
		self.size = size
		self.minAttackDamage = minAttackDamage
		self.maxAttackDamage = maxAttackDamage
	def touchAttack(self,player):
		if math.hypot(player.x-self.x,player.y-self.y) < (player.size+self.size)/2:
			player.speedx = (player.x-self.x)*-1
			player.speedy = (player.y-self.y)*-1
			self.speedx = 0
			self.speedy = 0
			player.health -= self.minAttackDamage+random()*(self.maxAttackDamage-self.minAttackDamage)
						
						
#Enemies

#PLAY WITH MEEEEE class
class Player:

	def __init__(self):
		self.x = 0
		self.y = 0
		self.rect = Rect(self.x,self.y,MANSIZE,MANSIZE)
		self.speedx = 0
		self.speedy = 0
		self.acceleration = 0.3
		self.inAttack = False
		self.maxHealth = 200
		self.health = self.maxHealth
	def move(self,canNotMoves,cameraX,cameraY):
		self.directions = []
		if self.inAttack:
			self.acceleration = 0.1
		else:
			self.acceleration = 0.3
				
		if KEYSTATES['w']:
			self.speedy += self.acceleration
		if KEYSTATES['a']:
			self.speedx -= self.acceleration
		if KEYSTATES['s']:
			self.speedy -= self.acceleration
		if KEYSTATES['d']:
			self.speedx += self.acceleration
				
		self.speedx *= 0.9
		self.speedy *= 0.9
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

				
	def draw(self,cameraX,cameraY):
		if self.inAttack:
			drawImage(man2,self.x-cameraX,self.y-cameraY,MANSIZE,MANSIZE)
		else:
			drawImage(man1,self.x-cameraX,self.y-cameraY,MANSIZE,MANSIZE)
#Player class

#Level Up! class
class Level:

	def __init__(self,levelDICT): 
		self.walls = levelDICT["WALLS"]
		self.enemies = levelDICT["ENEMIES"]
		self.buttons = levelDICT["BUTTONS"]
		self.projSize = 3
		self.proj = []
	def handleObjects(self,manX,manY,cameraX,cameraY):
		canNotMoves = []			
			
		for wall in self.walls:
			canNotMoves += wall.playerCollide(manX,manY,MANSIZE)
				for j in range(len(self.proj), 0, -1):
					i = j-1
					projectile = self.proj[i]
					projectile.move()
					if projectile.checkIfOut(cameraX,cameraY) or projectile.checkIfCollide(wall.rect):
						del self.proj[i]
			return canNotMoves

	def handleMouseUp(self,manX,manY,cameraX,cameraY):
		overButton = False
		for button in self.buttons:
			if button.isUnderMouse():
				overButton = True
			if not overButton:
				self.proj.append(Projectile())
				self.proj[-1].update(self.projSize,True,manX,manY+MANSIZE/2+self.projSize/2,_mouseX+cameraX,_mouseY+cameraY)
	def drawLevel(self,cameraX,cameraY):
		for i in range(0,9):
			for j in range(0,9):
				drawImage(marblefloor, (j*backgroundWidth)-cameraX, (i*backgroundHeight)-cameraY, backgroundWidth,backgroundHeight)
		for wall in self.walls:
			wall.draw(cameraX,cameraY)
		for projectile in self.proj:
			projectile.draw(cameraX,cameraY)
		for button in self.buttons:
			button.draw()
#Level class

class Game:
	def __init__(self):
		self.man = Player()
		self.cameraX= -_screenWidth/2
		self.cameraY= -_screenHeight/2
		self.mousedown = False
		self.currentLevel = Level(LEVELS[0])
	def gameLoop(self):
		firstMousedown = False
		firstMouseup = False
			
		if isLeftMouseDown() and not self.mousedown:
			firstMousedown = True
			self.mousedown = True
		if not isLeftMouseDown() and self.mousedown:
			firstMouseup = True
			self.mousedown = False
				
		for key in allKeysUsed:
			KEYSTATES[key]= isKeyDown(key)
				
		canNotMoves = self.currentLevel.handleObjects(self.man.x,self.man.y,self.cameraX,self.cameraY)
				
		if firstMouseup:
			self.currentLevel.handleMouseUp(self.man.x,self.man.y,self.cameraX,self.cameraY)
				
		self.currentLevel.drawLevel(self.cameraX,self.cameraY)
		self.man.draw(self.cameraX, self.cameraY)
				
		self.man.move(canNotMoves,self.cameraX,self.cameraY)
				
				
				
		if self.man.x-self.cameraX > (_screenWidth-CAMERASLACKX) or self.man.x-self.cameraX < CAMERASLACKX:
			self.cameraX+=self.man.speedx
								
		if self.man.y-self.cameraY > (_screenHeight-CAMERASLACKY) or self.man.y-self.cameraY < CAMERASLACKY:
			self.cameraY+=self.man.speedy
						
LEVELS= [{"BUTTONS":[Button(0,_screenHeight-35,100,'pause',PAUSE)],"WALLS":[Wall(100,100,10,1),Wall(200,100,1,10)],"ENEMIES":[0,1]}]

game = Game()
while True:
	newFrame()
	game.gameLoop()
								

