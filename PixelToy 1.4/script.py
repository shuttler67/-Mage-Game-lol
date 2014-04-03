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
			for neighbour in neighbours:
				neighbour.calculateScores(self.g_score+distance, goal, (self.worldx,self.worldy))
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
		foundGoal = False
		fail = False
		iteration = 0
		while not foundGoal and not fail:
			newFrame()
			
			for c_node in self.closedNodes:
				useColour(0, 0, 255, 255)
				drawCircle(c_node.worldx*20, c_node.worldy*20,5)
			for o_node in self.openNodes:
				useColour(255,0,0,255)
				drawCircle(o_node.worldx*20, o_node.worldy*20,5)
			useColour(0,255,0,255)
			drawCircle(self.goal.worldx*20, self.goal.worldy*20,5)

			iteration += 1
			#print iteration
			if len(self.openNodes) != 0:
				min_f_score = self.openNodes[0].f_score
				bestNodeIndex = 0
				for n in range(len(self.openNodes)):
					if self.openNodes[n].f_score < min_f_score:
						bestNodeIndex = n
				currentNode = self.openNodes[bestNodeIndex]
				self.closedNodes.append(currentNode)

				self.openNodes.remove(currentNode)

				print "F", currentNode.f_score
				print "G", currentNode.g_score
				if currentNode == self.goal:
					foundGoal = True
					self.goal = currentNode
					continue
				currentNeighbours = currentNode.neighbourNodes((self.goal.worldx, self.goal.worldy))
				#print "Before", len(currentNeighbours)
				for neighbour in currentNeighbours:
					if neighbour in self.closedNodes:
						currentNeighbours.remove(neighbour)
							
					elif not canMoveTo():
						currentNeighbours.remove(neighbour)

					elif neighbour in self.openNodes:
						open_index = self.openNodes.index(neighbour)
						if neighbour.g_score < self.openNodes[open_index].g_score:
							self.openNodes.pop(open_index)
						else:
							currentNeighbours.remove(neighbour)
							
					
				#print "After", len(currentNeighbours)
				self.openNodes += currentNeighbours

				#print len(self.closedNodes)
				#print len(self.openNodes)

			else:
				fail = True

		if fail:
			return
		else:
			return self.recoverPath()

def canMoveTo():
	return True
 
a = AStar((0,0),(10,7))
a.findPath(canMoveTo)
while True:
	newFrame()
	for c_node in a.closedNodes:
		useColour(0, 0, 255, 255)
		drawCircle(c_node.worldx*20, c_node.worldy*20,5)
	for o_node in a.openNodes:
		useColour(255,0,0,255)
		drawCircle(o_node.worldx*20, o_node.worldy*20,5)
