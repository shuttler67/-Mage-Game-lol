#!/usr/home/thomas/git/-Mage-Game-lol/PixelToy\ 1.4

class AStar:
	@staticmethod
	def estimateHeuristicTo(goal, node):
		deltaX = abs(goal.worldx - node.worldx)
		deltaY = abs(goal.worldy - node.worldy)
		return min(deltaX, deltaY) * 1.4 + max(deltaX, deltaY) - min(deltaX, deltaY)
		
	class Node:
		def __init__(self, worldx, worldy, cameFromPos = None):
			self.worldx, self.worldy = worldx, worldy
			self.cameFromPos = cameFromPos
		def calculateScores(self, distanceFromStart, goal):
			self.g_score = distanceFromStart
			self.f_score = AStar.estimateHeuristicTo(goal, self)+self.g_score
			
		def __eq__(self, node2):
			return self.worldx == node2.worldx and self.worldy == node2.worldy
			
		def neighbourNodes(self, goal):
			neighbours =[]
			for worldx in range(-1,2):
				for worldy in range(-1,2):
					distance = 1
					if abs(worldx)+abs(worldy) == 2:
						distance = 1.4
					if not worldx == worldy == 0:
						neighbours.append(AStar.Node(self.worldx+worldx,self.worldy+worldy,(self.worldx,self.worldy)))
			for neighbour in neighbours:
				neighbour.calculateScores(self.g_score+distance, goal)
	    		return neighbours
	
	def __init__(self, start, goal):
		self.start = AStar.Node(*start)
		self.goal = AStar.Node(*goal)
		self.start.calculateScores(0, self.goal)
		self.openNodes = [self.start]
		self.closedNodes = []
		
	def recoverPath(self):
		nodePath = [self.goal]
		path = []
		
		while not nodePath[0] == self.start:
			nodePath.insert(0,self.closedNodes[self.closedNodes.index(AStar.Node(*path.cameFrom))])
		
		for node in nodePath:
			path.append((node.x, node.y))
		
		return path

	def findPath(self, canMoveTo):
		foundGoal = False
		fail = False
		while not foundGoal and not fail:
			if len(self.openNodes) != 0:
				min_f_score = self.openNodes[0].f_score
				bestNodeIndex = 0
				for n in range(len(self.openNodes)):
					if self.openNodes[n].f_score < min_f_score:
						bestNodeIndex = n
				currentNode = self.openNodes[bestNodeIndex]
				self.openNodes.pop(bestNodeIndex)
				if currentNode == self.goal:
					foundGoal = True
					continue
				currentNeighbours = currentNode.neighbourNodes(self.goal)
				
				for neighbour in currentNeighbours:
					if neighbour in self.closedNodes:
						currentNeighbours.remove(neighbour)
							
					if neighbour in self.openNodes:
						open_index = self.openNodes.index(neighbour)
						if neighbour.g_score < self.openNodes[open_index].g_score:
							self.openNodes.pop(open_index)
						else:
							currentNeighbours.remove(neighbour)
							
					if not canMoveTo():
						currentNeighbours.remove(neighbour)
				
				self.openNodes += currentNeighbours
							
				self.closedNodes.append(currentNode)
			else:
				fail = True

		if fail:
			return
		else:
			return self.recoverPath()

def canMoveTo():
	return True
 
a = AStar((0,0),(1,1))
a.findPath(canMoveTo)
while True:
	newFrame()
	for o_node in a.openNodes:
		useColour(255,0,0,255)
		drawPoint(o_node.worldx, o_node.worldy)
	for c_node in a.closedNodes:
		useColour(0, 0, 255, 255)
		drawPoint(c_node.worldx, c_node.worldy)
