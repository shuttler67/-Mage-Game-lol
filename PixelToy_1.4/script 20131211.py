man1 = loadImage('res/man1.png')
man2 = loadImage('res/man2.png')

size = 32

MODEUP = "ModeUp"
MODEDOWN = "ModeDown"
MODERIGHT = "ModeRight"
MODELEFT = "ModeLeft"
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
cameray = 0
cameraSpeed = 2

changeTime = 0
currentMode = MODERIGHT
cameraMode = MODERIGHT

platforms = []

class Platform:
	def __init__(self,x,y,length,change):
		self.x = x
		self.y = y
		self.length = length
		self.lengthCoord = self.x+length
		self.heightCoord = self.y+10
		self.change = change
	def isOnTop(self,manx,many):
		manLength = manx+32
		return (manx < self.lengthCoord and manx > self.x and many <= self.heightCoord and many > self.y or manLength < self.lengthCoord and manLength > self.x and many <= self.heightCoord and many > self.y)
	def draw(self,camerax,cameray):
		useColour(0,200,0,255)
		drawRectangle(self.x+camerax,self.y+cameray,self.length,10)
	def checkChange(self,manx):
		if manx > self.x:
			return self.change
		else:
			return False
		
#	Max jump height of guy is 110. Max jump length is 280

def inView(platform,camerax,cameray):
	if platform.lengthCoord < camerax*-1 and cameraMode == MODERIGHT:
		return True
	elif platform.x > camerax*-1+_screenWidth and cameraMode == MODELEFT:
		return True
	elif platform.heightCoord < cameray*-1 and cameraMode == MODEUP:
		return True
	elif platform.y > cameray*-1+_screenHeight and cameraMode == MODEDOWN:
		return True
	else:
		return False

def createPlatform(platforms,change):
	jumpHeightCoord = platforms[-1].y+110
	Plength = random()*225+75
	if currentMode == MODERIGHT:
		Py = random()*min(_screenHeight-100,jumpHeightCoord)
		Px = platforms[-1].lengthCoord + random()*(250-(Py-platforms[-1].y))
	elif currentMode == MODELEFT:
		Py = random()*min(_screenHeight-100,jumpHeightCoord)
		Px = platforms[-1].x - random()*(250-(Py-platforms[-1].y))
		Px-=Plength
	elif currentMode == MODEUP:
		Py = random()*100+platforms[-1].y+10
		Px = (2*random() - 1)*min((_screenWidth-Plength)-(Py-platforms[-1].y),platforms[-1].length)
	elif currentMode == MODEDOWN:
		Py = random()*(_screenHeight-200)+(platforms[-1].y-(_screenHeight-200))
		Px = random()*_screenWidth-200+100
	platforms.append(Platform(Px,Py,Plength,change))
	print 'created platform'

def restart():
	currentMode = MODERIGHT
	cameraMode = MODERIGHT
	camerax = 0
	cameray = 0
	cameraSpeed = 2
	manx = 150
	many = 245
	speedy = 0
	speedx = 0
	
def createStartingPlatforms(platforms):
	platforms[:] = []
	platforms.append(Platform(100,240,100,False))
	for i in xrange(0,5):
		createPlatform(platforms,False)
	print "creating starting platforms"

createStartingPlatforms(platforms)

while True:
	onPlatform = False
	changeTime+=1
	change = False
	
	if cameraMode == MODERIGHT:
		camerax-=cameraSpeed
	elif cameraMode == MODELEFT:
		camerax+=cameraSpeed
	elif cameraMode == MODEUP:
		cameray-=cameraSpeed
	elif cameraMode == MODEDOWN:
		cameray+=cameraSpeed
	
	if changeTime == 1500:
		changeTime = 0
		change = True
		if currentMode == MODERIGHT:
			Rand = round(random())
			if Rand == 0:
				currentMode = MODEUP
			else:
				currentMode = MODEDOWN
		elif currentMode == MODELEFT:
			Rand = round(random())
			if Rand == 0:
				currentMode = MODEUP
			else:
				currentMode = MODEDOWN
		elif currentMode == MODEUP:
			Rand = round(random())
			if Rand == 0:
				currentMode = MODELEFT
			else:
				currentMode = MODERIGHT
		elif currentMode == MODEDOWN:
			Rand = round(random())
			if Rand == 0:
				currentMode = MODELEFT
			else:
				currentMode = MODERIGHT
		
	if len(platforms)<5:
		createPlatform(platforms,change)
		print "platform restored"
		
	for platform in platforms:
		if not inView(platform,camerax,cameray):
			platforms.remove(platform)
		if platform.checkChange(manx):
			cameraMode = currentMode
		platform.draw(camerax,cameray)
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
			
	if many+32 < cameray*-1 or manx+32 < camerax*-1 or many > cameray*-1+_screenHeight or manx > camerax*-1+_screenWidth:
		restart()
		createStartingPlatforms(platforms)
		print "restarting"
	
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
					
		if direction == RIGHT:
			speedx += 0.3
			drawImage(man1,manx+camerax,many+cameray,size,size)
		elif direction == LEFT:
			speedx -= 0.3
			drawImage(man1,manx+camerax,many+cameray,size,size)
		else:
			drawImage(man1,manx+camerax,many+cameray,size,size)
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
		
	manx += speedx
	

	newFrame()