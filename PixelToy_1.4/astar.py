
class AStar:
	def __init__(self,radius, canMoveTo, isDisliked):
		self.entityRadius = radius
		self.goal = 0
		self.canMoveTo = canMoveTo
		self.isDisliked = isDisliked
		
	@staticmethod
	def estimateHeuristicTo(goal, node):
		deltaX = abs(goal[0] - node.x)
		deltaY = abs(goal[1] - node.y)
		#return deltaX + deltaY
		return min(deltaX, deltaY) * 1.4 + max(deltaX, deltaY) - min(deltaX, deltaY)

	class Node:
		def __init__(self, x, y,isGoal=False):
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

	def findPath(self, start, goal, MAP):
		gx,gy = goal
		self.start = AStar.Node(*start)
		self.goal = AStar.Node(gx,gy,True)
		self.start.calculateScores(0, goal, None)
		self.openNodes = [self.start]
		self.closedNodes = []

		if not self.canMoveTo(self.goal, MAP):
			return
		foundGoal = False
		fail = False
		iteration = 0
		while not foundGoal and not fail:
			if len(self.openNodes) != 0:
				bestIndex = 0
				min_f_score = 100000000

				for i in range(len(self.openNodes)):
						
					if self.openNodes[i].f_score < min_f_score:
						min_f_score = self.openNodes[i].f_score
						bestIndex = i
						
					if self.estimateHeuristicTo((self.goal.x,self.goal.y), self.openNodes[i]) <= 2.8:
						bestIndex = i
						break

				self.closedNodes.append(self.openNodes[bestIndex])
				currentNode = self.openNodes[bestIndex]
				del self.openNodes[bestIndex]
					
				if currentNode == self.goal:
					foundGoal = True
					self.goal = currentNode
					continue
				currentNeighbours = currentNode.neighbourNodes((self.goal.x, self.goal.y))

				for i in range(len(currentNeighbours)-1,-1,-1):
					if currentNeighbours[i] in self.closedNodes:
						del currentNeighbours[i]
							
					elif not self.canMoveTo(currentNeighbours[i], MAP):
						del currentNeighbours[i]

					elif currentNeighbours[i] in self.openNodes:
						open_index = self.openNodes.index(currentNeighbours[i])
						if currentNeighbours[i].g_score < self.openNodes[open_index].g_score:
							self.openNodes[open_index].calculateScores(currentNeighbours[i].g_score,(self.goal.x, self.goal.y),currentNeighbours[i].cameFromPos)
						del currentNeighbours[i]
							
					else:
						if self.isDisliked(currentNeighbours[i],self.entityRadius, MAP):
							currentNeighbours[i].f_score += 100
						
				self.openNodes += currentNeighbours
			else:
				fail = True
				
		if not fail:
			return self.recoverPath(self.goal)
		else:
			'''bestIndex = 0
			min_h_score = 100000000

			for i in range(len(self.closedNodes)):
				h_score = AStar.estimateHeuristicTo((self.goal.x,self.goal.y), self.closedNodes[i])
				if h_score < min_h_score:
					min_h_score = h_score
					bestIndex = i
			
			return self.recoverPath(self.closedNodes[i])'''
			return


	def recoverPath(self,goal):
		nodePath = [goal]
		path = []

		while not nodePath[0] == self.start:
			nodePath.insert(0,self.closedNodes[self.closedNodes.index(AStar.Node(*nodePath[0].cameFromPos))])

		for node in nodePath:
			path.append((node.x, node.y))

		self.closedNodes = []
		self.openNodes = []
		path.reverse()
		return path
