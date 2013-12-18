import math
marblefloor = loadImage('res/marblefloor.png')
backgroundy = 384
backgroundx = 384
isbackgrounddrawn = False
isoutofscreen = False

man1 = loadImage('res/man1.png')
man2 = loadImage('res/man2.png')

mousedown = False

projSize = 3
proj = []

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
	def __init__(self):
		self.x = 32
		self.y = 32
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
	def powerup(self,projSize,mousex,mousey):
		proj[-1].update(projSize,False,self.x,self.y+(self.size/2)+projSize,mousex,mousey)
		self.inAttack = True
	def attack(self,projSize,mousex,mousey):
		proj[-1].update(projSize,True,self.x,self.y+(self.size/2),mousex,mousey)
		self.inAttack = False
	def draw(self):
		if self.inAttack:
			drawImage(man2,self.x-(self.size/2),self.y-(self.size/2),self.size,self.size)
		else:
			drawImage(man1,self.x-(self.size/2),self.y-(self.size/2),self.size,self.size)
			
man = Player()
firstMousedown = True
while True:
	newFrame()
	if isbackgrounddrawn == False:
		for i in range(0,6):
			for j in range(0,6):
				drawImage(marblefloor, j*backgroundx, i*backgroundy	,384, 384)
	mousex = _mouseX
	mousey = _mouseY
	if isKeyDown('w'):
		speedy += 0.3
	if isKeyDown('s'):
		speedy -= 0.3
	if isKeyDown('a'):
		speedx -= 0.3
	if isKeyDown('d'):
		speedx += 0.3
	speedx *= 0.9
	speedy *= 0.9
	many += speedy
	manx += speedx
	
	man.move()
	man.draw()

	if isMouseDown():
		mousedown = True
		if firstMousedown:
			proj.append(Projectile())
			firstMousedown = False
		if projSize <= 6:
			projSize += 0.1
		man.powerup(projSize,_mouseX,_mouseY)
	if not isMouseDown() and mousedown == True:
		man.attack(projSize,_mouseX,_mouseY)
		projSize = 3
		mousedown = False
		firstMousedown = True
	for projectile in proj:
		projectile.draw()
	
	for j in range(len(proj), 0, -1):
		i = j-1
		proj[i].move()
		proj[i].draw()
		if proj[i].checkIfOut():
			del proj[i]
