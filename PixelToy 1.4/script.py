import math
marblefloor = loadImage('res/marblefloor.png')
backgroundy = 384
backgroundx = 384



man1 = loadImage('res/man1.png')
man2 = loadImage('res/man2.png')



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
		self.speedx = 0
		self.speedy = 0
		self.size = 64
		self.inAttack = False
	def move(self):
		if isKeyDown('w'):
			self.speedy += 0.3
		if isKeyDown('s'):
			self.speedy -= 0.3
		if isKeyDown('a'):
			self.speedx -= 0.3
		if isKeyDown('d'):
			self.speedx += 0.3
		self.speedx *= 0.9
		self.speedy *= 0.9
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

	
#class Wall:
#	def __init__(self):
		
class Level:
	def __init__(self,mx,my,walls,enemies):
		self.man = Player(mx,my)
		self.walls = walls
		self.enemies = enemies
		self.firstMousedown = True
		self.mousedown = False
		self.projSize = 3
		self.proj = []
		marblefloor = loadImage('res/marblefloor.png')
		self.camerax=0
		self.cameray=0
		self.screenspeed=1
		self.cameraslack=250
		self.cameraslacky=200
	def mainLoop(self):
		for i in range(0,9):
			for j in range(0,9):
				drawImage(marblefloor, (j*backgroundx)-self.camerax, (i*backgroundy)-self.cameray, 384,384)
		
		if self.man.x>(_screenWidth-self.cameraslack):
			self.camerax+=(self.man.x-(_screenWidth-self.cameraslack))
			self.man.x=(_screenWidth-self.cameraslack)
			
		if self.man.y>(_screenHeight-self.cameraslacky):
			self.cameray+=(self.man.y-(_screenHeight-self.cameraslacky))
			self.man.y=(_screenHeight-self.cameraslacky)
				
		if self.man.x<self.cameraslack:
			self.camerax+=(self.man.x-self.cameraslack)
			self.man.x=self.cameraslack
			
		if self.man.y<self.cameraslacky:
			self.cameray+=(self.man.y-self.cameraslacky)
			self.man.y=self.cameraslacky
		
		self.man.move()
		self.man.draw()
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

		for j in range(len(self.proj), 0, -1):
			i = j-1
			self.proj[i].move()
			self.proj[i].draw()
			if self.proj[i].checkIfOut():
				del self.proj[i]
	

walls1 = [0,1]
enemies1 = [0,1]
lvl1 = Level(_screenHeight/2,32,walls1,enemies1)

while True:
	newFrame()
	lvl1.mainLoop()
		
