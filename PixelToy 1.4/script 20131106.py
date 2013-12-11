man1 = loadImage('res/man1.png')
man2 = loadImage('res/man2.png')

size = 32

RIGHT = "right"
LEFT = "left"
STILL = "still"
inJump = False

jumpHeight = 4.9

direction = STILL
manx = 150
many = 245

speedy = 0
speedx = 0

downTime = 0

camerax = 0
cameraSpeed = 2

platforms = []

class Platform:
	def __init__(self,x,y,length):
		self.x = x
		self.y = y
		self.length = length
		self.lengthCoord = self.x+length
		self.heightCoord = self.y+10
	def isOnTop(self,manx,many):
		manLength = manx+32
		return (manx < self.lengthCoord and manx > self.x and many <= self.heightCoord and many > self.y or manLength < self.lengthCoord and manLength > self.x and many <= self.heightCoord and many > self.y)
	def draw(self,camerax):
		useColour(0,200,0,255)
		drawRectangle(self.x+camerax,self.y,self.length,10)
		
#	Max jump height of guy is 110. Max jump length is 280

def createPlatform(platforms):
	jumpHeight = platforms[-1].y+110
	Py = random()*min(_screenHeight-100,jumpHeight)
	Px = platforms[-1].lengthCoord + random()*(250-(Py-platforms[-1].y))
	Plength = random()*225+75
	platforms.append(Platform(Px,Py,Plength))

def createStartingPlatforms(platforms):
	platforms[:] = []
	platforms.append(Platform(100,240,100))
	print platforms[-1]
	for i in xrange(0,5):
		createPlatform(platforms)

createStartingPlatforms(platforms)

while True:
	onPlatform = False
	
	camerax-=cameraSpeed
#	cameraSpeed+=0.001
	
	if len(platforms)<=5:
		createPlatform(platforms)
		
	if platforms[0].lengthCoord < camerax*-1:
		platforms.pop(0)
		
	for platform in platforms:
		platform.draw(camerax)
		if not isKeyDown('DOWN') or downTime > 45:
			if platform.isOnTop(manx,many) and speedy<0:
				speedy = 0
				inJump = False
				many = platform.y+1
				onPlatform = True
				downTime = 0
		else:
			downTime += 1
		
	if onPlatform == False:
		inJump = True
			
	if many+32 < 0 or manx+32 < camerax*-1:
		createStartingPlatforms(platforms)
		camerax = 0
		cameraSpeed = 2
		manx = 150
		many = 245
		speedy = 0
		speedx = 0
	
	many += speedy
	speedy -= 0.1
		
	if inJump == False:
		if isKeyDown('LEFT'):
			if direction != LEFT:
				direction = LEFT
		elif isKeyDown('RIGHT'):
			if direction != RIGHT:
				direction = RIGHT
		else:
			direction = STILL

		if isKeyDown('UP'):
			inJump = True
			speedy = jumpHeight
			print(str(manx)+" "+str(many))
					
		if direction == RIGHT:
			speedx += 0.3
			drawImage(man1,manx+camerax,many,size,size)
		elif direction == LEFT:
			speedx -= 0.3
			drawImage(man1,manx+camerax,many,size,size)
		else:
			drawImage(man1,manx+camerax,many,size,size)
		speedx *= 0.9
	else:
		drawImage(man2,manx+camerax,many,size,size)
		if speedx < -2.65:
			speedx = -2.65
		elif speedx > 2.65:
			speedx = 2.65
		else:
			if isKeyDown('RIGHT'):
				speedx += 0.05
			elif isKeyDown('LEFT'):
				speedx -= 0.05
		print(manx)
		
	manx += speedx
	

	newFrame()