
class AStar:
	def estimateHeuristicTo(self,node):
		deltaX = abs(goal.x - node.x)
		deltaY = abs(goal.y - node.y)
		return min(deltaX,deltaY)*1.4+max(deltaX,deltaY)-min(deltaX,deltaY)
	class Node:
		def init(self,x,y,cameFrom,distanceFromStart):
			self.x,self.y = x,y
			self.cameFrom = cameFrom
			self.g_score = distanceFromStart
			self.f_score = estimateHeuristicTo(self)+self.g_score
		def compareNodePos(self,node2):
			return self.x == node2.x and self.y == node2.y
		def neighbourNodes(self):
			neighbours =[]
			for x in range(-1,2):
				for y in range(-1,2):
					distance = 1
					if abs(x)+abs(y)==2:
						distance = 1.4
					if not x==y==0:
						neighbours.append(Node(self.x+x,self.y+y,self,self.g_score+distance))
	    		return neighbours
	def __init__(self,start,goal):
		start = Node(*start,'none')
		goal = Node(*goal,'none')
		openNodes = [start]
		closedNodes = []
	def recoverPath(self):
		path = [self.goal]
		while not path[0].compareNodePos(start):
			path.insert(0,path[0].cameFrom)
		return path
	def findPath(self):
		foundGoal = False
		fail = False
		while not foundGoal:
			if len(openNodes) != 0:
				min_f_score = openNodes[0].f_score
				for node in openNodes:
					if node.f_score < min_f_score.
						currentNode = node
				openNodes.remove(currentNode)
				if currentNode.compareNodePos(goal):
					foundGoal = True
				currentNeighbours = currentNode.neighbourNodes()
				for neighbour in currentNeighbours:
				
				closedNodes.append(currentNode)
			else:
				fail = True
				break
		if fail:
			return 'none'
		else:
			return self.recoverPath()
