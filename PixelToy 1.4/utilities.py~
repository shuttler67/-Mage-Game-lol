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
		useColour(*colour)

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
	def isUnderMouse(self):
		return self.rect.rectCollide(Rect(_mouseX,_mouseY,0,0)) #checking if mouse is over button
	def draw(self):
		useColourList(BLACK)
		if isLeftMouseDown() and self.isUnderMouse():						
			drawImageRect(buttonDown,self.rect)
			drawString(self.rect.x1+self.rect.width/2-len(self.text)*6,self.rect.y1+11,self.text)
		else:
			drawImageRect(buttonUp,self.rect)
			drawString(self.rect.x1+self.rect.width/2-len(self.text)*6,self.rect.y1+13,self.text)