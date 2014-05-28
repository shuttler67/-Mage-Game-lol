#!/git/-Mage-Game-lol/PixelToy\ 1.4

import math, sys

from astar import *
from utilities import *

epicface = loadImage('res/epicface.png',False)
fireball = loadImage('res/Fireball.png',False)
floor = loadImage('res/floor.png')
trollface = loadImage('res/trollface.png')
cloudLightning = loadImage('res/cloud.png',False)
mails = ['res/mail4.png','res/mail1.png','res/mail2.png','res/mail5.png','res/mail6.png']
mail4=loadImage('res/postcard.png')
backgroundWidth = 510
backgroundHeight = 510

still = loadImage('res/postmanstill.png',False)
still2 = loadImage('res/postmanstill2.png',False)
charge1 = loadImage('res/postmancharge1.png',False)
charge2 = loadImage('res/postmancharge2.png',False)
walk1 = loadImage('res/postmanwalk1.png',False)
walk2 = loadImage('res/postmanwalk2.png',False)
walk3 = loadImage('res/postmanwalk3.png',False)
walk4 = loadImage('res/postmanwalk4.png',False)

RIGHT = "right"
LEFT  = "left"
UP    = "up"
DOWN  = "down"
NIL = 'nil'

MAXSPEED = 2.7
MANSIZE = 60
CAMERASLACKX=250/5
CAMERASLACKY=200/5

FRAMECOUNT = 0
allKeysUsed =('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','SHIFT','TAB','SPACE','ESCAPE')
KEYSTATES = {}
PREV_KEYSTATES = {}
for key in allKeysUsed:
	KEYSTATES[key]= isKeyDown(key)

	
global WALLSIZE
WALLSIZE = 30

#		 R G B Alpha
RED = (255, 0 , 0 ,255)
GREEN = ( 0 ,200, 30 ,255)
BLACK = ( 0 , 0 , 0 ,255)
BLUE = (0, 0 , 200 ,255)
GREY = (64,64,64,255)
WHITE = (255,255,255,255)

def readLevelFile():
	levelFile = open('levels','r')
	data = levelFile.readlines() + ['\r\n']
	levelFile.close()
	
	levelTextMap = [] #list to hold level text format thing
	levelWalls = []
	levelWallMAP = []
	
	for lineNum in range(len(data)):
		line = data[lineNum].rstrip('\r\n')
		if '//' in line:
			line = line[:line.find('//')]
		if line !='':
			if '-' in line:
				line = line[1:]
				levelTextMap.append(line)
			
			if '>' in line:
				levelTextMap.reverse()
				for y in range(len(levelTextMap)):
					wallLength = 0
					wallStartIndex = None
					
					for x in range(len(levelTextMap[y])):

						if y == 0:
							levelWallMAP.append([])
						
						if levelTextMap[y][x] == "#":
							if wallLength == 0:
								wallStartIndex = x
							wallLength += 1
							levelWallMAP[x].append(True)
						else:
							levelWallMAP[x].append(False)
							
						if (x == len(levelTextMap[y])-1 or levelTextMap[y][x] == " ") and wallLength != 0:
							levelWalls.append(Wall(wallStartIndex*WALLSIZE,y*WALLSIZE,(wallStartIndex+wallLength)*WALLSIZE,y*WALLSIZE+WALLSIZE))
							wallLength = 0
							

				levelTextMap = []
		
	return levelWalls, levelWallMAP
	


class Camera:
	def update(self,x,y,pause):
		self.x = x
		self.y = y
		self.pause = pause
		
	def __init__(self,x,y,pause):
		self.update(x,y,pause)
		
	def getCameraView(self,pos): #vector please
		return pos.x - self.x, pos.y - self.y

	def getWorldView(self,pos): #vector please
		return pos.x + self.x, pos.y + self.y

class Entity:
	def setStatic(self):
		self.mass = 0.0
		self.invMass = 0.0

	def __init__(self, x, y, hit_box, restitution = 0.2, density = 1, isDynamic = True):
		self.pos = Vect(x,y)
		self.speed = Vect(0,0.0)
		self.hit_box = hit_box
		self.restitution = restitution
		self.directions = []
		self.netForce = Vect(0.0,0.0)
		
		if isinstance(self.hit_box, Rect):
			self.shape = 'Rect'
			if self.hit_box.h > self.hit_box.w:
				self.radius = self.hit_box.h/2
			else:
				self.radius = self.hit_box.w/2
			
		elif isinstance(self.hit_box, Circ):
			self.shape = 'Circ'
			self.radius = self.hit_box.r
		
		if isDynamic:
			self.mass = self.hit_box.Area() * density
			self.invMass = 1/self.mass
		else:
			self.setStatic()

	def applyForce(self,f):
		self.netForce += f

	def update(self):
		self.speed += self.netForce * self.invMass
		self.speed *= 1.001
		self.directions = []
		if self.speed.x > 0.5:
			self.directions.append(RIGHT)
		if self.speed.x < -0.5:
			self.directions.append(LEFT)
		if self.speed.y > 0.5:
			self.directions.append(UP)
		if self.speed.y < -0.5:
			self.directions.append(DOWN)

		self.pos += self.speed
		self.netForce.Set(0.0,0.0)
		self.hit_box.update(self.pos.x, self.pos.y)
		
	def findCollisionFunc(self,other):
		if self.shape == 'Rect':
		
			if other.shape == 'Rect':
				SATfunc = AABBvsAABB
				
			if other.shape == 'Circ':
				SATfunc = AABBvsCIRC
				
		elif self.shape == 'Circ':
		
			if other.shape == 'Rect':
				SATfunc = CIRCvsAABB
				
			if other.shape == 'Circ':
				SATfunc = CIRCvsCIRC
		return SATfunc

	def resolveCollision(self, other):
		SATfunc = self.findCollisionFunc(other)
		collision = SATfunc(self.hit_box, other.hit_box)
		if bool(collision):
			normal, penetration = collision
			
			#find relative velocity
			rv = other.speed - self.speed
			
			#find relative velocity in terms of the normal
			velAlongNormal = Vect.Dot(rv, normal)
			
			#if velocities are separating: NO SOLVE
			if velAlongNormal > 0.0:
				return
			
			if isinstance(self,Enemy) and isinstance(other,Enemy):
				e = 0.2
			else:
				e = min(self.restitution, other.restitution)
			
			#find impulse scalar
			j = -1*(1+e) * velAlongNormal
			j /= (self.invMass + other.invMass)
			#Apply impulse
			impulse = j * normal
			
			self.speed -= self.invMass * impulse
			other.speed += other.invMass * impulse

			#positional correction

			percent = 0.1
			slop = 0.01
			correction = max(abs(penetration) - slop, 0.0) / (self.invMass + other.invMass) * percent * normal
			self.pos -= self.invMass * correction
			other.pos += other.invMass * correction
			return True
		return False
		
#Wall class
class Wall(Entity):
	def __init__(self,x1,y1,x2,y2): 
		hit_box = Rect(x2 - (x2 - x1)/2, y2 - (y2 - y1)/2, (x2 - x1), (y2 - y1)) #confusing change from min-max type of rect to xywh type of rect
		Entity.__init__(self,hit_box.center.x, hit_box.center.y, hit_box, 1, isDynamic = False)
	def draw(self,cam):
		useColourList(BLUE)
		useColour(0,0,255)
		cam_x, cam_y = cam.getCameraView(self.hit_box.center)
		rect = Rect(self.hit_box.center.x, self.hit_box.center.y, self.hit_box.w, self.hit_box.h)
		rect.update(cam_x, cam_y)
		drawRect(rect)

#Wall class

#Projectile class
class Projectile:
	def __init__(self,x,y,tx,ty,image):
		if round(random()) == 0:
			spin = -10
		else: 
			spin = 10

		self.rotateSpeed = spin
		self.image = image
		self.image.setRotation(int(random()*360))
		self.pos = Vect(x,y)
		self.size = 15 + random()*7

		cosine, sine = findTrajectory(self.pos.x,self.pos.y,tx,ty)
		self.trajectory = Vect(cosine, sine)
		self.trajectory *= 16
	def move(self):
		self.pos += self.trajectory

	def draw(self,cam):
		cam_x, cam_y = cam.getCameraView(self.pos)
		if not cam.pause:
			self.image.rotate(self.rotateSpeed) 
		drawImage(self.image,cam_x, cam_y,self.size,self.size)
		
	def checkIfOut(self,cam):
		cam_x, cam_y = cam.getCameraView(self.pos)
		return cam_x < -self.size or cam_x > _screenWidth+self.size or cam_y < -self.size or cam_y > _screenHeight+self.size
		
	def checkIfCollide(self,rect_or_circ):
		if isinstance(rect_or_circ, Rect):
			return bool(CIRCvsAABB(Circ(self.pos.x,self.pos.y,self.size), rect_or_circ))
		else:
			return bool(CIRCvsCIRC(Circ(self.pos.x,self.pos.y,self.size), rect_or_circ))
#Projectile class

		
#Enemies
class Enemy(Entity):
	def __init__(self, x, y, hit_box, maxHealth, minAttackDamage, maxAttackDamage, knockback, radar, speed, density = 1):
		#initialise Entity part of Enemy
		Entity.__init__(self,x,y,hit_box, knockback, density)
		
		#basic setup
		self.maxHealth = maxHealth-10+random()*10
		self.health = self.maxHealth
		self.minAttackDamage = minAttackDamage
		self.maxAttackDamage = maxAttackDamage
		self.radar = radar
		self.moveSpeed = speed
		
		#astar setup
		self.astar = AStar(self.radius, self.canMoveTo, self.isDisliked)
		self.AStarRepeatTime = int(random()*100)
		self.hasPath = False
		self.currentNode = (self.pos.x,self.pos.y)
		
		# AI setup
		self.isWandering = True
		self.isCirclingTimer = 0
		self.attackTimer = 0

	@staticmethod
	def canMoveTo(node, MAP):
		
		if node.x < 0 or node.y < 0 or node.x >= len(MAP)-1 or node.y >= len(MAP[0])-1:
			return False
		
		if MAP[node.x][node.y]:
			return False

		if not node.isParentless:
			parent = node.cameFromPos
	
			for i in (-1,1):
				if abs(parent[0]-node.x) + abs(parent[1]-node.y) == 2:
					if MAP[ parent[0] + i][ parent[1] ] or MAP[ parent[0] ][ parent[1] + i]:
						return False
		return True
	@staticmethod
	def isDisliked(node,radius, MAP):
		deletionDepth = int(round(radius/float(WALLSIZE)))
		
		for i in xrange(-deletionDepth,deletionDepth):
			for j in xrange(-deletionDepth,deletionDepth):
				if abs(node.x) + abs(i) >= len(MAP) or abs(node.y) + abs(j) >= len(MAP[0]):
					continue
				if i == 0 and j == 0:
					continue
				if node.x + i < 0 or node.y + j < 0 or node.x + i > len(MAP)-1 or node.y + j > len(MAP[0])-1:
					return True
				if MAP[node.x + i][node.y + j]:
					return True
		
	def followPath(self, isNewPath = False):
		if len(self.path) != 0:
			if isNewPath:
				node = self.path.pop()
				self.currentNode = (node[0] * WALLSIZE + WALLSIZE/2 , node[1] * WALLSIZE + WALLSIZE/2)
				
			elif CIRCvsCIRC(Circ(self.currentNode[0],self.currentNode[1],0),Circ(self.pos.x,self.pos.y,self.radius/2)): #If player is within node boundary

				node = self.path.pop()
				self.currentNode = (node[0] * WALLSIZE + WALLSIZE/2 , node[1] * WALLSIZE + WALLSIZE/2)
				
			self.walkTowards(self.currentNode)
		else:
			return True
			
	def wander(self):
		global FRAMECOUNT

	def update(self,playerPos, MAP):

		#global FRAMECOUNT
		if CIRCvsCIRC(Circ(playerPos.x, playerPos.y,MANSIZE/2),Circ(self.pos.x,self.pos.y,self.radar)):
			if self.isWandering:
				path = self.astar.findPath((int(self.pos.x/WALLSIZE),int(self.pos.y/WALLSIZE)),(int(playerPos.x/WALLSIZE),int(playerPos.y/WALLSIZE)), MAP)
				if path != None:
					self.path = path
					self.followPath(True)
					self.hasPath = True
				else:
					self.hasPath = False
					self.attackTimer = 1

				self.isWandering = False

			elif not CIRCvsCIRC(Circ(playerPos.x, playerPos.y,0),Circ(self.pos.x,self.pos.y,100)) and FRAMECOUNT % 100 == self.AStarRepeatTime:
				self.isWandering = True
					
			elif self.hasPath:
				if self.followPath():
					self.attackTimer = 1
					self.hasPath = False
					
			if self.attackTimer != 0:
				self.walkTowards((playerPos.x, playerPos.y))
				self.attackTimer += 1
				if self.attackTimer == 60:
					self.attackTimer = 0
					self.isWandering = True 
			
			if self.isCirclingTimer != 0:
				self.isCirclingTimer -= 1
				
				if CIRCvsCIRC(Circ(playerPos.x, playerPos.y,1),Circ(self.pos.x,self.pos.y,50)):
					self.walkAway(playerPos)
				else:
					move = Vect(*findTrajectory(self.pos.x,self.pos.y, playerPos.x, playerPos.y))
					move *= self.moveSpeed
					move *= self.mass
					move.Rotate(math.radians(90.0))
					self.applyForce(move)
					
				if self.isCirclingTimer == 0:
					self.attackTimer = 60
		else:
			self.isWandering = True
			self.wander()
		
		Entity.update(self)

	def walkTowards(self,posTuple):
		#print posTuple
		cos, sin = findTrajectory(self.pos.x,self.pos.y,*posTuple)
		self.applyForce(Vect(cos * self.moveSpeed * self.mass, sin * self.moveSpeed * self.mass))
	
	def walkAway(self,posVect):
		#print posTuple
		cos, sin = findTrajectory(posVect.x,posVect.y,self.pos.x,self.pos.y)
		self.applyForce(Vect(cos * self.moveSpeed * self.mass, sin * self.moveSpeed * self.mass))
	
	def draw(self,cam):
			
		cam_x, cam_y = cam.getCameraView(self.pos)
		
		useColourList(GREY)
		drawRectangle(cam_x - self.radius, cam_y  + self.radius, self.radius*2, 10)
		useColourList(RED)
		drawRectangle(cam_x - self.radius+2, cam_y + self.radius+2, self.health/self.maxHealth*(self.radius*2 - 4), 6)
	
	def drawPath(self,cam):
		if not self.hasPath:
			return
		path = self.path[:]
		
		for i in range(len(path)):
			path[i] = (path[i][0] * WALLSIZE , path[i][1] * WALLSIZE)
			
		for i,node in enumerate(path):
			if i+1 != len(path):
				node1 = path[i]
				node2 = path[i+1]
				x1,y1 = cam.getCameraView(Vect(*node1))
				x2,y2 = cam.getCameraView(Vect(*node2))
				useColourList(GREEN)
				drawLine(x1 + WALLSIZE/2,y1 + WALLSIZE/2,x2 + WALLSIZE/2,y2 + WALLSIZE/2)
		
		nx,ny = cam.getCameraView(Vect(*self.currentNode))
		drawCircle(nx,ny,5)
			

# x, y, hit_box, maxHealth, minAttackDamage, maxAttackDamage, knockback, radar, speed, density
class EpicFace(Enemy):
	def __init__(self,x,y):
		Enemy.__init__(self,x,y,Circ(x,y,15), 40, 2, 5, 2, 1600, 0.29,2)

	def draw(self,cam):
		cam_x, cam_y = cam.getCameraView(self.pos)
		drawImage(epicface, cam_x, cam_y, self.hit_box.r * 2,self.hit_box.r * 2)
		Enemy.draw(self,cam)
		
class TrollFace(Enemy):
	def __init__(self,x,y):
		Enemy.__init__(self,x,y,Circ(x,y,45), 100, 7, 20, 3, 1900, 0.2,4)
		print self.radius

	def draw(self,cam):
		cam_x, cam_y = cam.getCameraView(self.pos)

		drawImage(trollface,cam_x, cam_y, self.hit_box.r * 2,self.hit_box.r * 2)
		Enemy.draw(self,cam)
		
class CloudMan(Enemy):
	def __init__(self,x,y):
		Enemy.__init__(self,x,y,Circ(x,y,44), 100, 7, 20, 3, 1900, 0.35,2)

	def draw(self,cam):
		cam_x, cam_y = cam.getCameraView(self.pos)

		drawImage(cloudLightning,cam_x, cam_y, self.hit_box.r * 2,self.hit_box.r * 2)
		Enemy.draw(self,cam)

#Enemies

#PLAY WITH MEEEEE class
class Player(Entity):
	def __init__(self,x,y):
		Entity.__init__(self,x,y, Rect(x,y, MANSIZE/3, MANSIZE),100,1)#Circ(0.0,0.0,MANSIZE),100,1)#
		self.inAttack = False
		self.maxHealth = 200.0
		self.health = 200.0
		
		self.invulnTimer = 0
		
		self.maxMana = 100.0
		self.mana = self.maxMana
		self.isMoving = False
		self.facing = RIGHT
		
	def update(self):
		if self.invulnTimer != 0:
			self.invulnTimer -= 1

		accel = Vect(0.0,0.0)

		if self.inAttack:
			movement = 0.1
		else:
			movement = 0.35
				
		if KEYSTATES['w']:
			accel.y += movement
		if KEYSTATES['a']:
			accel.x -= movement
		if KEYSTATES['s']:
			accel.y -= movement
		if KEYSTATES['d']:
			accel.x += movement

		if accel.x != 0.0 and accel.y != 0.0:
			accel *= 0.7 # cos(45) = ~0.707
		
		accel *= self.mass
		
		self.isMoving = bool(self.directions)

		self.applyForce(accel)
		Entity.update(self)
		
	def draw(self,cam):
		global FRAMECOUNT
		if self.facing == RIGHT and LEFT in self.directions:
			self.facing = LEFT
		if self.facing == LEFT and RIGHT in self.directions:
			self.facing = RIGHT
			
		cam_x, cam_y = cam.getCameraView(self.pos)
		
		if KEYSTATES['t'] and not PREV_KEYSTATES['t']:
			mx,my = cam.getWorldView(Vect(_mouseX,_mouseY))
			self.pos.Set(mx,my)

		if self.inAttack:
			if FRAMECOUNT%30<15:
				image = charge1
			else:
				image = charge2
		
		elif self.isMoving:
			if self.facing == RIGHT:
				if FRAMECOUNT%30>15:
					image = walk3
				else:
					image = walk4
			if self.facing == LEFT:
				if FRAMECOUNT%30<15:
					image = walk1
				else:
					image = walk2

		else:
			if self.facing == LEFT:
				image = still
			else:
				image = still2
				
		drawImage(image,cam_x, cam_y,MANSIZE,MANSIZE)

#Player class

#GUI class

class GUI:
	def __init__(self):
		self.buttons = [Button(50,_screenHeight-35/2,100,'pause','pause')]
	def update(self,pause):
		if pause:
			self.buttons = [Button(_screenWidth/2,_screenHeight/2+35,200,'resume game','unpause'),Button(_screenWidth/2,_screenHeight/2,200,'main menu','main'),Button(_screenWidth/2,_screenHeight/2-35,200,'quit game','quit')]
		else:
			self.buttons = [Button(50,_screenHeight-35/2,100,'pause','pause')]
			
	def handleMouseUp(self):
		returnValue = None
		overButton = False
		for button in self.buttons:
			if button.isUnderMouse(Vect(_mouseX,_mouseY)):
				overButton = True
				returnValue = button.returnValue
		return returnValue, overButton
		
	def drawButtons(self):
		for button in self.buttons:
			button.draw(Vect(_mouseX,_mouseY))
			
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
	def __init__(self):
		self.walls, self.MAP = readLevelFile()
		self.enemies = []
		self.proj = []
		self.enemySpawnRate = 700 #number of seconds between spawns

	def handleObjects(self,player,cam):	
		
		#spawning enemies
		if FRAMECOUNT % self.enemySpawnRate == 0:
			ranPosX = WALLSIZE*2 + random()* WALLSIZE * (len(self.MAP)-3)
			ranPosY = WALLSIZE*2 + random()* WALLSIZE * (len(self.MAP[0])-3)
			
			randomEnemy = random()
			
			'''if randomEnemy < 0.3:
				self.enemies.append(EpicFace(ranPosX,ranPosY))
			elif randomEnemy < 0.6:
				self.enemies.append(CloudMan(ranPosX,ranPosY))
			else:
				self.enemies.append(TrollFace(ranPosX,ranPosY))'''

			self.enemySpawnRate = 1+int(random() * 500)
		
		#update projectiles (letters) 
		for i in range(len(self.proj)-1, -1, -1):
			self.proj[i].move()
			if self.proj[i].checkIfOut(cam):
				del self.proj[i]
			else:
				for wall in self.walls:
					if self.proj[i].checkIfCollide(wall.hit_box):
						del self.proj[i]
						break
		
		#update enemies
		for i in range(len(self.enemies)-1, -1, -1):
			self.enemies[i].update(player.pos, self.MAP)
			if self.enemies[i].resolveCollision(player) and player.invulnTimer == 0:
				player.health -= self.enemies[i].minAttackDamage+random()*(self.enemies[i].maxAttackDamage - self.enemies[i].minAttackDamage)
				self.enemies[i].attackTimer = 0
				self.enemies[i].isCirclingTimer = 60
				player.invulnTimer = 60
			
			for j in range(len(self.proj)-1, -1, -1):
				if self.proj[j].checkIfCollide(self.enemies[i].hit_box):
					if not KEYSTATES['c']:
						del self.proj[j]
					self.enemies[i].health -= random()*(10-5)+5
					
			if self.enemies[i].health <= 0:
				del self.enemies[i]
				
		#stop enemies from overlapping
		for index, enemy1 in enumerate(self.enemies[:-1]):
			for enemy2 in self.enemies[index+1:]:
				enemy1.resolveCollision(enemy2)
		
		#stop all entities from passing through walls
		entities = self.enemies + [player]
		for wall in self.walls:
			for entity in entities:
				wall.resolveCollision(entity)

	def spawnProjectile(self,overButtons,playerPos,cam):
		random1 = int(random()*len(mails))
		mail = loadImage(mails[random1])
	
		if not overButtons:
			self.proj.append(Projectile(playerPos.x,playerPos.y,_mouseX+cam.x,_mouseY+cam.y,mail))

	def drawLevel(self,cam):
		#for i in range(0,9):
		#	for j in range(0,9):
		#		drawImage(floor, (j*backgroundWidth)-cam.x, (i*backgroundHeight)-cam.y, backgroundWidth,backgroundHeight)
				
		for wall in self.walls:
			wall.draw(cam)

		for projectile in self.proj:
			projectile.draw(cam)

		for enemy in self.enemies:
			enemy.draw(cam)
			enemy.drawPath(cam)
#Level class

class Game:
	def __init__(self):
		self.man = Player(300,300)
		self.cam = Camera(-_screenWidth/2, -_screenHeight/2, False)
		self.mousedown = False
		self.currentLevel = Level()
		self.GUI = GUI()
		
	def gameLoop(self):	
		if self.update():	
			self.draw()
			return True

	def update(self):
		firstMousedown = False
		firstMouseup = False
			
		if isLeftMouseDown() and not self.mousedown:
			firstMousedown = True
			self.mousedown = True
		if not isLeftMouseDown() and self.mousedown:
			firstMouseup = True
			self.mousedown = False

		if firstMouseup:
			returnValue, overButtons = self.GUI.handleMouseUp()
			
			if returnValue == None:
				pass
			elif returnValue == 'pause':
				self.cam.pause = True
			elif returnValue == 'unpause':
				self.cam.pause = False
			else:
				return returnValue
			if not self.cam.pause:
				self.currentLevel.spawnProjectile(overButtons,self.man.pos,self.cam)
		
		if KEYSTATES['c']:
			self.currentLevel.spawnProjectile(False,self.man.pos,self.cam)

		if KEYSTATES['ESCAPE'] and not PREV_KEYSTATES['ESCAPE']:
			self.cam.pause = not self.cam.pause
		
		if not self.cam.pause:
			self.man.inAttack = self.mousedown
			self.man.update()
			self.currentLevel.handleObjects(self.man,self.cam)

		self.GUI.update(self.cam.pause)
		if self.man.health <= 0:
			return "player dead"
		cam_x, cam_y = self.cam.getCameraView(self.man.pos)
		cam_x -= _screenWidth/2
		cam_y -= _screenHeight/2

		displace = abs(cam_x) - CAMERASLACKX
		if displace > 0:
			if cam_x < 0:
				self.cam.x -= displace
			else:
				self.cam.x += displace

		displace = abs(cam_y) - CAMERASLACKY
		if displace > 0:
			if cam_y < 0:
				self.cam.y -= displace
			else:
				self.cam.y += displace
			
			
		if KEYSTATES['p']:
			print self.man.pos.x, self.man.pos.y

	def draw(self):
		self.currentLevel.drawLevel(self.cam)
		self.man.draw(self.cam)
		self.GUI.draw(self.man.health,self.man.mana,self.man.maxHealth,self.man.maxMana)
		
		if FRAMECOUNT < 300:
			useColourList(RED)
			drawString(_screenWidth/2-6*8, _screenHeight/2,"GET READY")
		
		elif FRAMECOUNT < 400:
			useColourList(GREEN)
			drawString(_screenWidth/2-12, _screenHeight/2,"GO")
			
		if self.cam.pause:
			useColour(0,0,0,130)
			drawRectangle(0,0,_screenWidth,_screenHeight)
			drawImage(mail4,_screenWidth/2,_screenHeight/2,_screenWidth/2,_screenWidth/2)
			
		self.GUI.drawButtons()	

class Menu:
	def __init__(self,buttonList):
		self.buttons = buttonList
		self.mousedown = False

	def update(self):
		firstMousedown = False
		firstMouseup = False
			
		if isLeftMouseDown() and not self.mousedown:
			firstMousedown = True
			self.mousedown = True
		if not isLeftMouseDown() and self.mousedown:
			firstMouseup = True
			self.mousedown = False
			
		if firstMouseup:
			for button in self.buttons:
				if button.isUnderMouse(Vect(_mouseX,_mouseY)):
					return button.returnValue

	def draw(self):
		for button in self.buttons:
			button.draw(Vect(_mouseX,_mouseY))

#Wall((POS),SIZE) ENEMY(HEALTH;(POS);SIZE;(ATCK DMG),KNOCKBACK;RADAR)
MENUS = {"main": Menu([Button(_screenWidth/2,_screenHeight/2+35/2,200,'PLAY!','game'),Button(_screenWidth/2,_screenHeight/2-35/2,200,'QUIT!','quit')])}

currentWindow = MENUS["main"]

while True:
	PREVIOUSscreenHeight = _screenHeight
	PREV_KEYSTATES = KEYSTATES.copy()
	newFrame()
	FRAMECOUNT += 1
	
	for key in allKeysUsed:
		KEYSTATES[key]= isKeyDown(key)
	
	updateReport = currentWindow.update()
	
	if updateReport:
		if updateReport == "player dead":
			currentWindow = MENUS["main"]
			
		elif updateReport == "game":
			currentWindow = Game()
			FRAMECOUNT = 0
		
		elif updateReport == "quit":
			quit()
		else:
			currentWindow = MENUS[updateReport]
	else:
		currentWindow.draw()
		drawString(0,0,str(_mouseX/WALLSIZE)+ " " +str(_mouseY/WALLSIZE))
				
			
