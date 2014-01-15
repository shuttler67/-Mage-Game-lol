import math

marblefloor = loadImage('res/marblefloor.png')
backgroundy = 384
backgroundx = 384

man1 = loadImage('res/man1.png')
man2 = loadImage('res/man2.png')

RIGHT = "right"
LEFT  = "left"
UP    = "up"
DOWN  = "down"
NIL   = "nil"

MAXSPEED = 2.7
#yolo
allKeysUsed = ('w','a','s','d')
RED = "red"
GREEN = "green"

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
#What does this even do?
class Button:
	def __init__(self,rect,text,function):
		self.rect = rect
		self.text = text
		self.function = function
		self.colour = RED
	def checkClick(self,mousex,mousey,mousedown,firstMouseup):
		if self.rect.rectCollide(Rect(mousex,mousey,0,0)): #checking if mouse is over button
			if mousedown:
				self.colour = GREEN
			else:
				self.colour = RED
			if firstMouseup:
				function()
	def draw(self):
		if self.colour == RED:
			useColour(255,0,0,255)
		elif self.colour == GREEN:
			drawRectangle(self.rect.x1,self.rect.y1,self.rect.width,self.rect.height)
#The walls
class Wall:
	def __init__(self,rect):
		self.rect = rect
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
	def draw(self,camerax,cameray):
		useColour(255,0,0,255)
		drawRectangle(self.rect.x1-camerax,self.rect.y1-cameray,self.rect.width,self.rect.height)
#Project Ile
class Projectile:
	def __init__(self):
		self.notIdle = False
		self.projSpeed = 4
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
	def draw(self,camerax,cameray):
		useColour(255,0,0,100)
		drawCircle(self.x-camerax,self.y-cameray,self.size)
	def checkIfOut(self,camerax,cameray):
		if self.x-camerax < -self.size or self.x-camerax > _screenWidth+self.size or self.y-cameray < -self.size or self.y-cameray > _screenHeight+self.size and self.notIdle:
			return True
		else:
			return False
	def checkIfCollide(self,rect):
		if rect.rectCollide(Rect(self.x,self.y,0,0)) and self.notIdle:
			return True
		else:
			return False
#PLAY WITH MEEEEE
class Player:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.size = 64
		self.rect = Rect(x,y,self.size,self.size)
		self.speedx = 0
		self.speedy = 0
		self.acceleration = 0.3
		self.inAttack = False
		self.projSize = 3
		self.proj = []
	def powerup(self,mousex,mousey,firstMousedown,camerax,cameray):
		if firstMousedown:
			self.proj.append(Projectile())
		if self.projSize <= 6:
			self.projSize += 0.1
		self.proj[-1].update(self.projSize,False,self.x,self.y+self.size/2+self.projSize/2,mousex+camerax,mousey+cameray)
		self.inAttack = True
	def attack(self,mousex,mousey,camerax,cameray):
		self.proj[-1].update(self.projSize,True,self.x,self.y+self.size/2+self.projSize/2,mousex+camerax,mousey+cameray)
		self.projSize = 3
		self.inAttack = False
	def move(self,canNotMoves,pressedKeys,camerax,cameray):
		self.directions = []
		if self.inAttack:
			self.acceleration = 0.1
		else:
			self.acceleration = 0.3
		for key in pressedKeys:
			if key == 'w':
				self.speedy += self.acceleration
			if key == 'a':
				self.speedx -= self.acceleration
			if key == 's':
				self.speedy -= self.acceleration
			if key == 'd':
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

		
	def draw(self,camerax,cameray):
		if self.inAttack:
			drawImage(man2,self.x-camerax,self.y-cameray,self.size,self.size)
		else:
			drawImage(man1,self.x-camerax,self.y-cameray,self.size,self.size)
#Level Up!
class Level:
	def __init__(self,player,buttons):
		self.hasMan = False
		if not player == NIL:
			self.man = player
			self.hasMan = True
		self.buttons = buttons
		self.mousedown = False
		self.pressedkeys = []
		marblefloor = loadImage('res/marblefloor.png')
		self.camerax=0
		self.cameray=0
		self.screenspeed=1
		self.cameraslack=250
		self.cameraslacky=200
	def updateObstacles(self,walls,enemies):
		self.walls = walls
		self.enemies = enemies
	def mainLoop(self):
		canNotMoves = []
		self.pressedKeys = []
		firstMousedown = False
		firstMouseup = False
		
		if self.man.x-self.camerax>(_screenWidth-self.cameraslack):
			self.camerax+=self.man.speedx

			
		if self.man.y-self.cameray>(_screenHeight-self.cameraslacky):
			self.cameray+=self.man.speedy		
				
		if self.man.x-self.camerax<self.cameraslack:
			self.camerax+=self.man.speedx
		
			
		if self.man.y-self.cameray<self.cameraslacky:
			self.cameray+=self.man.speedy
		
		print self.camerax, self.cameray
		
		if isLeftMouseDown() and self.mousedown == False:
			firstMousedown = True
			self.mousedown = True
		if not isLeftMouseDown() and self.mousedown == True:
			firstMouseup = True
			self.mousedown = False
		
		for key in allKeysUsed:
			if isKeyDown(key):
				self.pressedKeys.append(key)
		
		
		
		for i in range(0,9):
			for j in range(0,9):
				drawImage(marblefloor, (j*backgroundx)-self.camerax, (i*backgroundy)-self.cameray, 384,384)
				
		if self.hasMan:
			for wall in self.walls:
				canNotMoves += wall.playerCollide(self.man.x,self.man.y,self.man.size)
				for j in range(len(self.man.proj), 0, -1):
					i = j-1
					projectile = self.man.proj[i]
					projectile.move()
					projectile.draw(self.camerax,self.cameray)
					if projectile.checkIfOut(self.camerax,self.cameray) or projectile.checkIfCollide(wall.rect):
						del self.man.proj[i]
			if self.mousedown:
				self.man.powerup(_mouseX,_mouseY,firstMousedown,self.camerax, self.cameray)
			if firstMouseup:
				self.man.attack(_mouseX,_mouseY,self.camerax, self.cameray)
			self.man.move(canNotMoves,self.pressedKeys,self.camerax,self.cameray)
			self.man.draw(self.camerax, self.cameray) 
		
		for wall in self.walls:
			wall.draw(self.camerax, self.cameray)

LVL1= {"LVL":Level(Player(_screenWidth/2,_screenHeight/2),[1,2]),"WALLS":[Wall(Rect(100,100,100,10)),Wall(Rect(200,100,10,100))],"ENEMIES":[0,1]}
currentLVL = LVL1
currentLVL["LVL"].updateObstacles(currentLVL["WALLS"],currentLVL["ENEMIES"])
while True:
	newFrame()
	currentLVL["LVL"].mainLoop()
