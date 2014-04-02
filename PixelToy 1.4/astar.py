
class AStar:
	def estimateHeuristicTo(self, node):
		deltaX = abs(self.goal.worldx - node.worldx)
		deltaY = abs(self.goal.worldy - node.worldy)
		return min(deltaX, deltaY) * 1.4 + max(deltaX, deltaY) - min(deltaX, deltaY)
		
	class Node:
		def init(self, worldx, worldy, cameFromPos = None, distanceFromStart = 0):
			self.worldx, self.worldy = worldx, worldy
			self.cameFromPos = cameFromPos
			self.g_score = distanceFromStart
			self.f_score = estimateHeuristicTo(self)+self.g_score
			
		def __eq__(self, node2):
			return self.worldx == node2.worldx and self.worldy == node2.worldy
			
		def neighbourNodes(self):
			neighbours =[]
			for worldx in range(-1,2):
				for worldy in range(-1,2):
					distance = 1
					if abs(worldx)+abs(worldy) == 2:
						distance = 1.4
					if not worldx == worldy == 0:
						neighbours.append(Node(self.worldx+worldx,self.worldy+worldy,(self.worldx,self.worldy),self.g_score+distance))
	    		return neighbours
				
	def __init__(self, start, goal):
		self.start = Node(*start,'none')
		self.goal = Node(*goal,'none')
		self.openNodes = [self.start]
		self.closedNodes = []
		
	def recoverPath(self):
		nodePath = [self.goal]
		path = []
		
		while not nodePath[0] == self.start:
			nodePath.insert(0,self.closedNodes[self.closedNodes.index(Node(*path.cameFrom))])
		
		for node in nodePath:
			path.append((node.x, node.y))
		
		return path

	def findPath(self, canMoveTo):
		foundGoal = False
		fail = False
		while not foundGoal and not fail:
			if len(self.openNodes) != 0:
				min_f_score = self.openNodes[0].f_score
				for n in len(self.openNodes):
					if self.openNodes[n].f_score < min_f_score
						bestNodeIndex = n
				currentNode = self.openNodes[bestNodeIndex]
				self.openNodes.pop(bestNodeIndex)
				if currentNode.compareNodePos(self.goal):
					foundGoal = True
					continue
				currentNeighbours = currentNode.neighbourNodes()
				
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
				
				openNodes += currentNeighbours
							
				self.closedNodes.append(currentNode)
			else:
				fail = True

		if fail:
			return
		else:
			return self.recoverPath()
