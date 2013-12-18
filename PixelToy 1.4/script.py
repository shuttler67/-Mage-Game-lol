import math
marblefloor = loadImage('res/marblefloor.png')
backgroundy = 384
backgroundx = 384
isbackgrounddrawn = False
isoutofscreen = False

man1 = loadImage('res/man1.png')
man2 = loadImage('res/man2.png')

RIGHT = "right"
LEFT  = "left"
UP    = "up"
DOWN  = "down"

class Rect:
	def __init__(self,x,y,w,h):
		self.x1 = x
		self.y1 = y
		self.x2 = x+w
		self.y2 = y+h
		self.width = w
		self.height = h
	def isCollide(self,rect2):
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

class Wall:
	def __init__(self,rect):
		self.rect = rect
	def playerCollide(self,playerRect):
		if playerRect.isCollide(self.rect):
			return True
	def draw(self):
		print "drawn"
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
		self.inAttack = False
		self.direction = RIGHT
	def move(self,canMove):
		if isKeyDown('w'):
			self.speedy += 0.3
			self.direction = UP
		if isKeyDown('s'):
			self.speedy -= 0.3
			self.direction = DOWN
		if isKeyDown('a'):
			self.speedx -= 0.3
			self.direction = LEFT
		if isKeyDown('d'):
			self.speedx += 0.3
			self.direction = RIGHT
		self.speedx *= 0.9
		self.speedy *= 0.9
		if canMove:
			self.y += self.speedy
			self.x += self.speedx
	def powerup(self,projSize,mousex,mousey,proj):
		proj[-1].update(projSize,False,self.x,self.y+self.size/2+projSize/2,mousex,mousey)
		self.inAttack = True
	def attack(self,projSize,mousex,mousey,proj):
		proj[-1].update(projSize,True,self.x,self.y+self.size/2+projSize/2,mousex,mousey)
		self.inAttack = False
	def draw(self):
		if self.inAttack:
			drawImage(man2,self.x,self.y,self.size,self.size)
		else:
			drawImage(man1,self.x,self.y,self.size,self.size)
	
		
class Level:
	def __init__(self,mx,my):
		self.man = Player(mx,my)
		self.firstMousedown = True
		self.mousedown = False
		self.projSize = 3
		self.proj = []
	def updateObstacles(self,walls,enemies):
		self.walls = walls
		self.enemies = enemies
	def mainLoop(self):
		canMove = True
		if isLeftMouseDown():
			self.mousedown = True
			if self.firstMousedown:
				self.proj.append(Projectile())
				self.firstMousedown = False
			if self.projSize <= 6:
				self.projSize += 0.1
			self.man.powerup(self.projSize,_mouseX,_mouseY,self.proj)
		if not isLeftMouseDown() and self.mousedown == True:
			self.man.attack(self.projSize,_mouseX,_mouseY,self.proj)
			self.projSize = 3
			self.mousedown = False
			self.firstMousedown = True
		
		for wall in self.walls:
			wall.draw()
			if wall.playerCollide(Rect(self.man.x+self.man.speedx-self.man.size/2,self.man.y+self.man.speedy-self.man.size/2,self.man.size,self.man.size)):
				canMove = False
				
		for j in range(len(self.proj), 0, -1):
			i = j-1
			self.proj[i].move()
			self.proj[i].draw()
			if self.proj[i].checkIfOut():
				del self.proj[i]
		
		self.man.move(canMove)
		self.man.draw()

LVL1= {"LVL":Level(32,_screenHeight/2),"WALLS":[Wall(Rect(100,100,100,10)),Wall(Rect(200,100,10,100))],"ENEMIES":[0,1]}
currentLVL = LVL1

while True:
	newFrame()
	currentLVL["LVL"].updateObstacles(currentLVL["WALLS"],currentLVL["ENEMIES"])
	currentLVL["LVL"].mainLoop()
		