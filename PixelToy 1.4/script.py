import math
man1 = loadImage('res/man1.png')
man2 = loadImage('res/man2.png')
msize = 32

manx = 32
many = 32

speedx = 0
speedy = 0

mousedown = False

projSpeed = 6
projSize = 3
lol = True
proj = []

class Projectile:
	def __init__(self):
		self.updatePos = False
	def update(self,size,boolean,x,y,tx,ty):
		self.x = x
		self.y = y
		self.a = ty-self.y
		self.b = tx-self.x
		self.d = math.hypot(self.b,self.a)
		self.updatePos = boolean
		self.size = size
	def draw(self):
		if self.updatePos:
			self.x += self.b/self.d*projSpeed
			self.y += self.a/self.d*projSpeed
		drawCircle(self.x,self.y,self.size)
	def checkIfOut(self):
		if self.x < 0 or self.x > _screenWidth or self.y < 0 or self.y > _screenHeight:
			return True
		else:
			return False
		
while True:
	newFrame()
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

	if isMouseDown():
		mousedown = True
		if lol:
			proj.append(Projectile())
			lol = False
		if projSize <= 6:
			projSize += 0.1
		proj[-1].update(projSize,False,manx,many+(msize/2)+projSize,mousex,mousey)
		drawImage(man2,manx-(msize/2),many-(msize/2),msize,msize)
	else:
		drawImage(man1,manx-(msize/2),many-(msize/2),msize,msize)
	if not isMouseDown() and mousedown == True:
		proj[-1].update(projSize,True,manx,many+(msize/2),mousex,mousey)
		projSize = 3
		mousedown = False
		lol = True

	for projectile in proj:
		projectile.draw()
	
	
