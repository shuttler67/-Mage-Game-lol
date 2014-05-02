from init import *
import math
buttonUp = loadImage('res/buttonUp.png')
buttonDown = loadImage('res/buttonDown.png')
#Utilities

def Clamp(_min, _max, a):
	if a < _min:
		return _min
	if a > _max:
		return _max
	return a
	
class Vect:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def Length(self):
		return math.sqrt(self.x**2+self.y**2)

	def LengthSqr(self):
		return self.x**2+self.y**2

	def Rotate(self, radians):
		c = cos(radians)
		s = sin(radians)
		self.x = self.x * c - self.y * s
		self.y = self.y * s + self.y * c

	def Set(self,x, y):
		self.x = x
		self.y = y

	def Normalise(self):
		length = self.Length()
		
		if length > 0.0001:
			self.x /= length
			self.y /= length
			
	def __add__(self,vect_or_scal):
		if isinstance(vect_or_scal,Vect):
			return Vect(vect_or_scal.x + self.x, vect_or_scal.y + self.y) 
		else:
			return Vect(vect_or_scal + self.x, vect_or_scal + self.y)
			
	def __radd__(self,vect_or_scal):
		if isinstance(vect_or_scal,Vect):
			return Vect(vect_or_scal.x + self.x, vect_or_scal.y + self.y) 
		else:
			return Vect(vect_or_scal + self.x, vect_or_scal + self.y)
	
	def __iadd__(self,vect_or_scal):
		if isinstance(vect_or_scal, Vect):
			self.x += vect_or_scal.x
			self.y += vect_or_scal.y
		else:
			self.x += vect_or_scal
			self.y += vect_or_scal
			
		return self

	def __sub__(self,vect_or_scal):
		if isinstance(vect_or_scal,Vect):
			return Vect(self.x - vect_or_scal.x, self.y - vect_or_scal.y) 
		else:
			return Vect(self.x - vect_or_scal, self.y - vect_or_scal)
			
	def __rsub__(self,vect_or_scal):
		if isinstance(vect_or_scal,Vect):
			return Vect(self.x - vect_or_scal.x, self.y - vect_or_scal.y) 
		else:
			return Vect(self.x - vect_or_scal, self.y - vect_or_scal)
		
	def __isub__(self,vect_or_scal):
		if isinstance(vect_or_scal,Vect):
			self.x -= vect_or_scal.x
			self.y -= vect_or_scal.y
		else:
			self.x -= vect_or_scal
			self.y -= vect_or_scal
						
		return self
		
	def __mul__(self,scal):
		return Vect(scal * self.x, scal * self.y)
		
	def __rmul__(self,scal):
		return Vect(scal * self.x, scal * self.y)
		
	def __imul__(self,scal):
		self.x *= scal
		self.y *= scal
					
		return self
	
	def __neg__(self):
		return Vect(-self.x,-self.y)
		
	def __div__(self,scal):
		return Vect(self.x / scal, self.y / scal)
		
	def __idiv__(self,scal):
		self.x /= scal
		self.y /= scal
					
		return self
		
	def __eq__(self,vect):
		return self.x == vect.x and self.y == vect.y
		
	@staticmethod
	def Dot(vect1,vect2):
		return vect1.x * vect2.x + vect1.y * vect2.y

	@staticmethod
	def Cross(*args):
		if isinstance(arg[0],Vect): #if first argument is a Vector
			if isinstance(arg[1],Vect): #if second argument is a Vector
				return arg[0].x * arg[1].y - arg[0].y * arg[1].x
				
			elif isinstance(arg[1],(int, float)): #if second argument is a Scalar
				return Vect(arg[1] * arg[0].y, -arg[1] * arg[0].x)
				
		elif isinstance(arg[1],Vect): #if second argument is a Vector
			return Vect(-arg[1] * arg[0].y, arg[1] * arg[0].x)
		print 'complain!'

class Circ:
	def update(self,x,y):
		self.center = Vect(x,y)

	def __init__(self,x,y,r):
		self.update(x,y)
		self.r = r
	def Area(self):
		return math.pi * self.r * self.r

class Rect:
	def update(self,x,y):
		self.center = Vect(x,y)

	def __init__(self,x,y,w,h): #x,y is the center of the Rect
		self.w = w #width
		self.h = h #height
		self.update(x,y)

	def Area(self):
		return float(self.w * self.h)
	
	def pointCollide(self,pos):
		return pos.x > self.center.x - self.w/2 and pos.x < self.center.x + self.w/2 and pos.y > self.center.y - self.h/2 and pos.y < self.center.y + self.h/2
		
	def findMinMax(self):
		corner_vect = Vect(self.w / 2, self.h / 2) #vector from center to top left corner 
		_min = self.center - corner_vect
		_max = self.center + corner_vect
		return _min, _max
		
	def getCorners(self): #returns corners in tuple, CORNER is vector from center to corner
		halfW = self.w/2
		halfH = self.h/2
		return Vect(halfW, halfH), Vect(-halfW, halfH), Vect(halfW, -halfH), Vect(-halfW, -halfH)
	
		
def CIRCvsCIRC(a,b):
	distSqr = (a.center.x - b.center.x)**2 + (a.center.y - b.center.y)**2
	if not (a.r + b.r)**2 > distSqr:
		return False
	else:
		normal = b.center - a.center
		normal.Normalise()
		return normal, (a.r + b.r) - math.sqrt(distSqr)

def AABBvsAABB(a,b): # returns either False or normal and penetration, You can check which is which easily >>> collision = AABBvsAABB(a,b) 
																										#  >>> if collision: 
																										#  >>>		collNormal, penetration = collision
	n = b.center - a.center
	
	a_extent = a.w / 2
	b_extent = b.w / 2
	
	x_overlap = a_extent + b_extent - abs(n.x)
	
	if x_overlap > 0:
		a_extent = a.h / 2
		b_extent = b.h / 2
		
		y_overlap = a_extent + b_extent - abs(n.y)
		
		if y_overlap > 0:
			if x_overlap < y_overlap:
				if n.x < 0:
					normal = Vect(-1,0)
				else:
					normal = Vect(1,0)
				return normal, x_overlap
			else:
				if n.y < 0:
					normal = Vect(0,-1)
				else:
					normal = Vect(0, 1)
				return normal, y_overlap
	#print 'NOPE'
	return False
		
def AABBvsCIRC(a,b): # a = AABB b = CIRCLE 
					 # returns either False or normal and penetration, You can check which is which easily >>> collision = AABBvsCIRC(a,b) 
																										#  >>> if collision: 
																										#  >>>		collNormal, penetration = collision
	
	n = b.center - a.center
	
	x_extent = a.w / 2
	y_extent = a.h / 2
	
	penetrationX = (abs(n.x) - x_extent) - b.r
	penetrationY = (abs(n.y) - y_extent) - b.r
	if penetrationX > 0 or penetrationY > 0:
		return False
	
	if penetrationX > penetrationY:
		if n.x < 0:
			normal = Vect(-1,0)
		else:
			normal = Vect(1,0)
		penetration = penetrationX
	
	else:
		if n.y < 0:
			normal = Vect(0,-1)
		else:
			normal = Vect(0,1)
		penetration = penetrationY
	
	return normal, penetration
	
def CIRCvsAABB(a,b):
	coll = AABBvsCIRC(b,a)
	if coll:
		n,p = coll
		n = -n
		return n,p
	return False
	
def useColourList(colour):
	useColour(*colour)

def drawRect(rect):
	_min, _max = rect.findMinMax()
	drawRectangle(_min.x, _min.y, rect.w, rect.h)

def drawImageRect(image,rect):
	drawImage(image,rect.center.x, rect.center.y, rect.w, rect.h)

def findTrajectory(x,y,tx,ty):
	radians = math.atan2(ty-y,tx-x)
	cosine = math.cos(radians)
	sine   = math.sin(radians)
	return cosine, sine
#Utilities

#Button class
class Button:
	def __init__(self,x,y,width,text,returnValue): #x,y = center of button
		self.rect = Rect(x,y,width,35)
		self.text = text
		self.returnValue = returnValue
		
	def isUnderMouse(self, mousePos): #vector please
		return self.rect.pointCollide(mousePos) #checking if mouse is over button
		
	def draw(self, mousePos): #vector please
		useColour(0,0,0)
		_min, _max = self.rect.findMinMax()
		if isLeftMouseDown() and self.isUnderMouse(mousePos):						
			drawImageRect(buttonDown,self.rect)
			drawString(self.rect.center.x-len(self.text)*6, _min.y+11,self.text)
		else:
			drawImageRect(buttonUp,self.rect)
			drawString(self.rect.center.x-len(self.text)*6, _min.y+13,self.text)
