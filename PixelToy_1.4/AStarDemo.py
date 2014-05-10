#!/usr/home/thomas/git/-Mage-Game-lol/PixelToy\ 1.4
global drawNodes, scale, walls
def drawNodes(astar):
	useColour(0, 0, 0, 255)
	drawString(0 , 0, str((_mouseX) / scale) + ',' + str((_mouseY) / scale))
	for c_node in astar.closedNodes:
		useColour(0, 0, 255, 255)
		drawRectangle(c_node.x*scale, c_node.y*scale,scale,scale)
	for o_node in astar.openNodes:
		useColour(255,0,0,255)
		drawRectangle(o_node.x*scale, o_node.y*scale,scale,scale)
		
	useColour(100,100,100)
	for i in range(len(walls)):
		for j in range(len(walls[i])):
			if walls[i][j]:
				drawRectangle(i*scale, j*scale,scale,scale)
	

scale = 15

walls = []
for i in range(_screenWidth/scale+1):
	walls.append([])
	for j in range(_screenHeight/scale+1):
		walls[i].append(False)
class AStar:
	@staticmethod
	def estimateHeuristicTo(goal, node):
		deltaX = abs(goal[0] - node.x)
		deltaY = abs(goal[1] - node.y)
		return deltaX + deltaY
		return min(deltaX, deltaY) * 1.4 + max(deltaX, deltaY) - min(deltaX, deltaY)
		
	class Node:
		def __init__(self, x, y, isGoal = False):
			self.x, self.y = x, y
			self.isParentless = isGoal
		def calculateScores(self, distanceFromStart, goal, cameFromPos):
			self.cameFromPos = cameFromPos
			self.g_score = distanceFromStart
			self.f_score = AStar.estimateHeuristicTo(goal, self) + self.g_score
			
		def __eq__(self, node2):
			return self.x == node2.x and self.y == node2.y
			
		def neighbourNodes(self, goal):
			neighbours =[]
			for x in range(-1,2):
				for y in range(-1,2):
					distance = 1.0
					if abs(x)+abs(y) == 2:
						distance = 1.4
					if not x == y == 0:
						neighbours.append(AStar.Node(self.x+x,self.y+y))
						neighbours[-1].calculateScores(self.g_score+distance, goal, (self.x,self.y))
	    		return neighbours
	
	def __init__(self, start, goal):
		self.start = AStar.Node(start[0],start[1],True)
		self.goal = AStar.Node(goal[0],goal[1],True)
		self.start.calculateScores(0, goal, None)
		self.openNodes = [self.start]
		self.closedNodes = []
		
	def recoverPath(self):
		nodePath = [self.goal]
		path = []
		
		while not nodePath[0] == self.start:
			nodePath.insert(0,self.closedNodes[self.closedNodes.index(AStar.Node(*nodePath[0].cameFromPos))])
		
		for node in nodePath:
			path.append((node.x, node.y))
		
		return path

	def findPath(self, canMoveTo):
		if not canMoveTo(self.goal) or not canMoveTo(self.start):
			print 'nope'
			return
		foundGoal = False
		fail = False
		iteration = 0
		while not foundGoal and not fail:

			if iteration % 5 == 0:
				newFrame()
			
			drawNodes(self)
			
			iteration += 1
			#print iteration
			if len(self.openNodes) != 0:
				bestIndex = 0
				min_f_score = 100000000

				for i in range(len(self.openNodes)):
					if self.openNodes[i].f_score < min_f_score:
						min_f_score = self.openNodes[i].f_score
						bestIndex = i

				self.closedNodes.append(self.openNodes[bestIndex])
				currentNode = self.openNodes[bestIndex]

				#print "F", currentNode.f_score
				#print "G", currentNode.g_score
				if currentNode == self.goal:
					foundGoal = True
					self.goal = currentNode
					continue
				currentNeighbours = currentNode.neighbourNodes((self.goal.x, self.goal.y))
				#print "Before", len(currentNeighbours)
				for i in range(len(currentNeighbours)-1,-1,-1):
					if currentNeighbours[i] in self.closedNodes:
						del currentNeighbours[i]
							
					elif not canMoveTo(currentNeighbours[i]):
						del currentNeighbours[i]

					elif currentNeighbours[i] in self.openNodes:
						open_index = self.openNodes.index(currentNeighbours[i])
						if currentNeighbours[i].g_score < self.openNodes[open_index].g_score:	
							self.openNodes[open_index].calculateScores(currentNeighbours[i].g_score,(self.goal.x, self.goal.y),currentNeighbours[i].cameFromPos)
						del currentNeighbours[i]
							
				del self.openNodes[bestIndex]		
				print "After", len(currentNeighbours)
				self.openNodes += currentNeighbours
				#print len(self.closedNodes)
				#print len(self.openNodes)

			else:
				fail = True

		if not fail:
			return self.recoverPath()

def canMoveTo(node):
	cam_node_x = node.x*scale
	cam_node_y = node.y*scale
	isOut = (cam_node_x <= 0 or cam_node_y <= 0 or cam_node_x >= _screenWidth or cam_node_y >= _screenHeight)
	if isOut:
		print 'out'
		return False
	if walls[node.x][node.y]:
		print 'wall'
		return False
	
	if not node.isParentless:
		parent = node.cameFromPos
	
		for i in (-1,1):
			if abs(parent[0]-node.x) + abs(parent[1]-node.y) == 2:
				if walls[ parent[0] + i ][ parent[1] ] or walls[ parent[0] ][ parent[1] + i ]:
					print 'cutting edge'
					return False
	return True
 
a = AStar((1,1),(10,10))
path = a.findPath(canMoveTo)
firstClick = True
start = ()
while True:
	PREVmouse = isLeftMouseDown()
	newFrame()
	if isLeftMouseDown() and not PREVmouse:
		if firstClick:
			start = ((_mouseX) / scale,(_mouseY) / scale)
			firstClick = False
		else:
			a = AStar(start, ((_mouseX) / scale,(_mouseY) / scale))
			path = a.findPath(canMoveTo)
			firstClick = True
			
	if isRightMouseDown():
		if not walls[(_mouseX) / scale][(_mouseY) / scale]:
			walls[(_mouseX) / scale][(_mouseY) / scale] = True
			
	drawNodes(a)
	if path != None:
		for p in path:
			useColour(0,255,0,255)
			drawRectangle(p[0]*scale, p[1]*scale,scale,scale)
	else:
		useColour(0, 0, 0, 255)

		drawString(_screenWidth/2, _screenHeight/2, "NO SOLUTION")

