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
LEFT = "left"
UP = "up"
DOWN = "down"
NIL = "nil"
RESUME= "resume"
PAUSE = "pause"

MAXSPEED = 2.7

allKeysUsed =('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','shift','tab','space','escape')

# Colours
#         R G B Alpha
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
                self.image = buttonUp
        def isUnderMouse(self,mousex,mousey,mousedown):
                if self.rect.rectCollide(Rect(mousex,mousey,0,0)): #checking if mouse is over button
                        if mousedown:
                                self.image = buttonDown
                        else:
                                self.image = buttonUp
                        return True
                return False
        def draw(self):
                drawImageRect(self.image,self.rect)
                useColourList(BLACK)
                if self.image == buttonUp:
                        drawString(self.rect.x1+self.rect.width/2-len(self.text)*6,self.rect.y1+13,self.text)
                else:
                        drawString(self.rect.x1+self.rect.width/2-len(self.text)*6,self.rect.y1+11,self.text)
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
        def draw(self,camerax,cameray):
                useColourList(GREEN)
                drawRectangle(self.rect.x1-camerax,self.rect.y1-cameray,self.rect.width,self.rect.height)
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
        def draw(self,camerax,cameray,fireball):
                useColour(255,0,0,100)
                fireball.rotate(-2)
                drawImage(fireball,self.x-camerax,self.y-cameray,self.size*2,self.size*2)
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
				self.maxHealth = 200
				self.health = self.maxHealth
        def powerup(self,mousex,mousey,firstMousedown,camerax,cameray):
                if firstMousedown:
                        self.proj.append(Projectile())
                if self.projSize <= 10:
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
#Player class

#Level Up! class
class Level:
        def __init__(self,player,buttons,walls,enemies):
                self.hasMan = False
                if not player == NIL:
                        self.man = player
                        self.hasMan = True
                        self.camerax=self.man.x-_screenWidth/2
                        self.cameray=self.man.y-_screenHeight/2
                else:
                        self.camerax=0
                        self.cameray=0
                self.walls = walls
                self.enemies = enemies
                self.buttons = buttons
                self.mousedown = False
                self.pressedkeys = []
                
                self.cameraslack=250
                self.cameraslacky=200
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
                                
                for i in range(0,9):
                        for j in range(0,9):
                                drawImage(marblefloor, (j*backgroundWidth)-self.camerax, (i*backgroundHeight)-self.cameray, backgroundWidth,backgroundHeight)
                
                overButtons = False
                for button in self.buttons:
                        button.draw()
                        if self.hasMan:
                                if not self.man.inAttack:
                                        overButtons = button.isUnderMouse(_mouseX,_mouseY,self.mousedown)
                        elif button.isUnderMouse(_mouseX,_mouseY,self.mousedown):
                                break
                if self.hasMan:
                        if self.man.x-self.camerax>(_screenWidth-self.cameraslack) or self.man.x-self.camerax<self.cameraslack:
                                self.camerax+=self.man.speedx

                        if self.man.y-self.cameray>(_screenHeight-self.cameraslacky) or self.man.y-self.cameray<self.cameraslacky:
                                self.cameray+=self.man.speedy
                        for wall in self.walls:
                                canNotMoves += wall.playerCollide(self.man.x,self.man.y,self.man.size)
                                for j in range(len(self.man.proj), 0, -1):
                                        i = j-1
                                        projectile = self.man.proj[i]
                                        projectile.move()
                                        projectile.draw(self.camerax,self.cameray,fireball)
                                        if projectile.checkIfOut(self.camerax,self.cameray) or projectile.checkIfCollide(wall.rect):
                                                del self.man.proj[i]

                        if not overButtons:
                                if self.mousedown:                                
                                        self.man.powerup(_mouseX,_mouseY,firstMousedown,self.camerax, self.cameray)
                                if firstMouseup:
                                        self.man.attack(_mouseX,_mouseY,self.camerax, self.cameray)
                        self.man.move(canNotMoves,self.pressedKeys,self.camerax,self.cameray)
                        self.man.draw(self.camerax, self.cameray)
                
                for wall in self.walls:
                        wall.draw(self.camerax, self.cameray)
                
                for button in self.buttons:
                        if firstMouseup and button.isUnderMouse(_mouseX,_mouseY,self.mousedown):
                                return button.returnValue
                return NIL
#Level class


LEVELS= [Level(Player(1000,1000),[Button(0,_screenHeight-35,100,'pause',PAUSE)],[Wall(100,100,10,1),Wall(200,100,1,10)],[0,1])]
SPECIALLEVELS= {"PAUSE":Level(NIL,[Button(_screenWidth/2-75,_screenHeight/2-35/2,150,'resume game',RESUME)],[],[1,0])}
currentLVL = LEVELS[0]
pausedGame = currentLVL
while True:
        newFrame()
        lvlReturn = currentLVL.mainLoop()
        if lvlReturn != NIL:
                if lvlReturn == PAUSE:
                        pausedGame = currentLVL
                        currentLVL = SPECIALLEVELS["PAUSE"]
                if lvlReturn == RESUME:
                        currentLVL = pausedGame