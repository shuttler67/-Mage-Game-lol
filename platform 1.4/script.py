class Vec:
	def __init__(self,x,y):
		self.x,self.y = x,y
	def findLength(self):
		self.length = math.sqrt(self.x**2+self.y**2)

class OBBrect:
	def __init__(self,x,y,mass):
		self.invMass = 1/mass
		self.position = Vec(x,y)
		self.velocity = Vec(0,0)
		self.force
		
		self.torque = 0
		self.angVelocity = 0
		self.orient = 0
	def move(self):
		self.velocity += self.force*self.invMass
		self.angVelocity += self.torque
		self.position += self.velocity
		self.orient += self.angVelocity
class
		