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

allKeysUsed = ('w','a','s','d')
print "startup"
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
	def draw(self):
		useColour(255,0,0,255)
		drawRectangle(self.rect.x1,self.rect.y1,self.rect.width,self.rect.height)

class Projectile:
	def __init__(self):
		self.notIdle = False
		self.projSpeed = 6
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
	def draw(self):
		useColour(255,0,0,100)
		drawCircle(self.x,self.y,self.size)
	def checkIfOut(self):
		if self.x < -self.size or self.x > _screenWidth+self.size or self.y < -self.size or self.y > _screenHeight+self.size:
			return True
		else:
			return False

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
	def powerup(self,mousex,mousey,firstMousedown):
		if firstMousedown:
			self.proj.append(Projectile())
		if self.projSize <= 6:
			self.projSize += 0.1
		self.proj[-1].update(self.projSize,False,self.x,self.y+self.size/2+self.projSize/2,mousex,mousey)
		self.inAttack = True
	def attack(self,mousex,mousey):
		self.proj[-1].update(self.projSize,True,self.x,self.y+self.size/2+self.projSize/2,mousex,mousey)
		self.projSize = 3
		self.inAttack = False
	def move(self,canNotMoves,pressedKeys):
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

		for j in range(len(self.proj), 0, -1):
			i = j-1
			self.proj[i].move()
			self.proj[i].draw()
			if self.proj[i].checkIfOut():
				del self.proj[i]
	def draw(self):
		if self.inAttack:
			drawImage(man2,self.x,self.y,self.size,self.size)
		else:
			drawImage(man1,self.x,self.y,self.size,self.size)

class Level:
	def __init__(self,player,buttons):
		self.hasMan = False
		if not player == NIL:
			self.man = player
			self.hasMan = True
		self.buttons = buttons
		self.mousedown = False
		self.pressedkeys = []
	def updateObstacles(self,walls,enemies):
		self.walls = walls
		self.enemies = enemies
	def mainLoop(self):
		canNotMoves = []
		self.pressedKeys = []
		firstMousedown = False
		firstMouseup = False
		if isLeftMouseDown() and self.mousedown == False:
			firstMousedown = True
			self.mousedown = True
		if not isLeftMouseDown() and self.mousedown == True:
			firstMouseup = True
			self.mousedown = False
		
		for key in allKeysUsed:
			if isKeyDown(key):
				self.pressedKeys.append(key)
			
		for wall in self.walls:
			wall.draw()
			if self.hasMan:
				canNotMoves += wall.playerCollide(self.man.x,self.man.y,self.man.size)

		if self.hasMan:
			if self.mousedown:
				self.man.powerup(_mouseX,_mouseY,firstMousedown)
			if firstMouseup:
				self.man.attack(_mouseX,_mouseY)
			self.man.move(canNotMoves,self.pressedKeys)
			self.man.draw() 

LVL1= {"LVL":Level(Player(50,_screenHeight/2),[1,2]),"WALLS":[Wall(Rect(100,100,100,10)),Wall(Rect(200,100,10,100))],"ENEMIES":[0,1]}
currentLVL = LVL1
currentLVL["LVL"].updateObstacles(currentLVL["WALLS"],currentLVL["ENEMIES"])
while True:
	newFrame()
	currentLVL["LVL"].mainLoop()
