import math 
import random
import heapq
import sys
import inspect

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print "*** Method not implemented: %s at line %s of %s" % (method, line, fileName)
    sys.exit(1)




class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (an abstract class).
    """

    def getStartState(self):
        raiseNotDefined()

    def isGoalState(self, state):
        raiseNotDefined()

    def getSuccessors(self, state):
        raiseNotDefined()

    def getCostOfActions(self, actions):
        raiseNotDefined()


def genericSearch(problem, fringe, pushToFringe): 
    """
    This function is used in aStarSearch
    """
    closed = set()
    start = (problem.getStartState(), 0, [])
    pushToFringe(fringe, start, 0)

    while not fringe.isEmpty():
        (node, cost, path) = fringe.pop()

        if problem.isGoalState(node):
            print("optimal cost is %d" %cost)
            return path

        if node not in closed:
            closed.add(node)

            for child_node, child_action, child_cost in problem.getSuccessors(node):
                new_cost = cost + child_cost
                new_path = path + [child_action]
                new_state = (child_node, new_cost, new_path)
                pushToFringe(fringe, new_state, new_cost)



def nullHeuristic(state, problem=None):
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    fringe = PriorityQueue()
    def pushToFringe(fringe, state, cost):
        new_cost = cost + heuristic(state[0], problem)
        fringe.push(state, new_cost)

    path = genericSearch(problem, fringe, pushToFringe)
    return path


def hillClimbing(problem):
    """
    hillClimbing algorithm in its simplest form
    """
    fringe = PriorityQueue()
    def pushToFringe(fringe, state, cost):
        fringe.push(state, cost)

    (current, c_cost, c_path) = (problem.getStartState(), 0, [])

    if current.isGoal():
        return c_path
    
    def getNeighbor(node, cost, path):
        bestH=0
        for child_node, child_action, child_cost in problem.getSuccessors(node):
            if child_node.heuristic() > bestH:
                new_cost = cost + child_cost
                new_path = path + [child_action]
                bestNode = (child_node, new_cost, new_path)
                bestH = child_node.heuristic()
        return bestNode

    while True:
        (neighbor, n_cost, n_path) = getNeighbor(current, c_cost, c_path);
        if neighbor.heuristic() <= current.heuristic():
            return c_path
        (current, c_cost, c_path) = (neighbor, n_cost, n_path)



def simulatedAnnealing(problem):
    """
    simulatedAnnealing algorithm
    """

    (current, cost, path) = (problem.getStartState(), 0, [])

    if current.isGoal():
        return path

    T = 10
    i=100
    while True :
        coolingRate = 0.3
        if i<0:
            return path
        if current.isGoal():
            return path
        successors = problem.getSuccessors(current)
        (child_node, child_action, child_cost) = successors[random.randrange(len(successors))]
        new_cost = cost + child_cost
        new_path = path + [child_action]

        delta_E = child_node.heuristic() - current.heuristic()
        probability = math.exp(delta_E / T)
        if delta_E >0:
            (current, c_cost, c_path) = (child_node, new_cost, new_path)
        elif random.uniform(0, 1) < probability:
            (current, cost, path) = (child_node, new_cost, new_path)
        T = T - T * coolingRate
        i -= 1


    
