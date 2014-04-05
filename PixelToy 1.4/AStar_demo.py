#!/usr/home/thomas/git/-Mage-Game-lol/PixelToy\ 1.4

class AStar:
	@staticmethod
	def estimateHeuristicTo(goal, node):
		deltaX = abs(goal[0] - node.worldx)
		deltaY = abs(goal[1] - node.worldy)
		return deltaX + deltaY
		#return min(deltaX, deltaY) * 1.4 + max(deltaX, deltaY) - min(deltaX, deltaY)
		
	class Node:
		def __init__(self, worldx, worldy):
			self.worldx, self.worldy = worldx, worldy

		def calculateScores(self, distanceFromStart, goal, cameFromPos):
			self.cameFromPos = cameFromPos
			self.g_score = distanceFromStart
			self.f_score = AStar.estimateHeuristicTo(goal, self) + self.g_score
			
		def __eq__(self, node2):
			return self.worldx == node2.worldx and self.worldy == node2.worldy
			
		def neighbourNodes(self, goal):
			neighbours =[]
			for worldx in range(-1,2):
				for worldy in range(-1,2):
					distance = 1.0
					if abs(worldx)+abs(worldy) == 2:
						distance = 1.4
					if not worldx == worldy == 0:
						neighbours.append(AStar.Node(self.worldx+worldx,self.worldy+worldy))
						neighbours[-1].calculateScores(self.g_score+distance, goal, (self.worldx,self.worldy))
	    		return neighbours
	
	def __init__(self, start, goal):
		self.start = AStar.Node(*start)
		self.goal = AStar.Node(*goal)
		self.start.calculateScores(0, goal, None)
		self.openNodes = [self.start]
		self.closedNodes = []
		
	def recoverPath(self):
		nodePath = [self.goal]
		path = []
		
		while not nodePath[0] == self.start:
			print nodePath[0].worldx, nodePath[0].worldy
			nodePath.insert(0,self.closedNodes[self.closedNodes.index(AStar.Node(*nodePath[0].cameFromPos))])
		
		for node in nodePath:
			path.append((node.worldx, node.worldy))
		
		return path

	def findPath(self, canMoveTo):
		if not canMoveTo(self.goal):
			return
		foundGoal = False
		fail = False
		iteration = 0
		while not foundGoal and not fail:
			iteration += 0
			if iteration % 5 == 0:
				newFrame()
			
			for c_node in self.closedNodes:
				useColour(0, 0, 255, 255)
				drawCircle(c_node.worldx*15+100, c_node.worldy*15+100,5)
			for o_node in self.openNodes:
				useColour(255,0,0,255)
				drawCircle(o_node.worldx*15+100, o_node.worldy*15+100,5)
			useColour(0,255,0,255)
			drawCircle(self.goal.worldx*15+100, self.goal.worldy*15+100, 5)

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
				del self.openNodes[bestIndex]
				#print "F", currentNode.f_score
				#print "G", currentNode.g_score
				if currentNode == self.goal:
					foundGoal = True
					self.goal = currentNode
					continue
				currentNeighbours = currentNode.neighbourNodes((self.goal.worldx, self.goal.worldy))
				#print "Before", len(currentNeighbours)
				for i in range(len(currentNeighbours)-1,-1,-1):
					if currentNeighbours[i] in self.closedNodes:
						del currentNeighbours[i]
							
					elif not canMoveTo(currentNeighbours[i]):
						del currentNeighbours[i]

					elif currentNeighbours[i] in self.openNodes:
						open_index = self.openNodes.index(currentNeighbours[i])
						if currentNeighbours[i].g_score < self.openNodes[open_index].g_score:	
							self.openNodes[open_index].calculateScores(currentNeighbours[i].g_score,(self.goal.worldx, self.goal.worldy),currentNeighbours[i].cameFromPos)
						del currentNeighbours[i]
							
					
				#print "After", len(currentNeighbours)
				self.openNodes += currentNeighbours
				#print len(self.closedNodes)
				#print len(self.openNodes)

			else:
				fail = True

		if not fail:
			return self.recoverPath()

def canMoveTo(node):
	return node.worldx < -13 or node.worldx > 20 or node.worldy != 8
 
a = AStar((0,0),(10,40))
path = a.findPath(canMoveTo)
while True:
	newFrame()
	useColour(0, 0, 0, 255)
	drawString(0 , 0, str((_mouseX-100) / 15) + ',' + str((_mouseY-100) / 15))
	for c_node in a.closedNodes:
		useColour(0, 0, 255, 255)
		drawCircle(c_node.worldx*15+100, c_node.worldy*15+100,5)
	for o_node in a.openNodes:
		useColour(255,0,0,255)
		drawCircle(o_node.worldx*15+100, o_node.worldy*15+100,5)
	if path != None:
		for p in path:
			useColour(0,255,0,255)
			drawCircle(p[0]*15+100, p[1]*15+100,5)
	else:
		useColour(0, 0, 0, 255)
		drawString(_screenWidth, _screenHeight, "NO SOLUTION")
