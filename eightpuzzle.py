import search
import random

# Module Classes

class EightPuzzleState:
    """
    This class defines the mechanics of the puzzle
    The task of recasting this puzzle as a search problem is left to
    the EightPuzzleSearchProblem class.
    """

    def __init__( self, numbers ):
        """
        Constructs a new eight puzzle from an ordering of numbers.
        the list
            [1, 0, 2, 3, 4, 5, 6, 7, 8]
          represents the eight puzzle:
            -------------
            | 1 |   | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            ------------

        The configuration of the puzzle is stored in a 2-dimensional
        list 'cells'.
        """
        
        self.cells = []
        numbers = numbers[:] # Make a copy so as not to cause side-effects.
        numbers.reverse()
        for row in range( 3 ):
            self.cells.append( [] )
            for col in range( 3 ):
                self.cells[row].append( numbers.pop() )
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col

    def isGoal( self ):
        """
          Goal state:
            -------------
            |   | 1 | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            -------------
        """
        current = 0
        for row in range( 3 ):
            for col in range( 3 ):
                if current != self.cells[row][col]:
                    return False
                current += 1
        return True


    def findIndex(self, number):
        """
            Finds indeces of the element equal to 'number' in the puzzle cells
        """
        for row in range( 3 ):
            for column in range( 3 ):
                if self.cells[row][column] == number:
                    return [row,column]
           

    def heuristic(self):
        """
            h = sum of manhatan distance for every tile
        """
        h = 0
        current = 0
        for row in range( 3 ):
            for column in range( 3 ):
                #current is the value of goal[row][column]
                [cell_row , cell_column] = self.findIndex(current)
                h += abs(cell_row - row) + abs(cell_column - column)
            current += 1
        #print('heuristic = ',h)
        return h

    """
    def heuristic( self ):
        
            #h = tiles out of place
            #this heuristic didn't work well
        
        h = 0;
        current = 0
        for row in range( 3 ):
            for col in range( 3 ):
                if current == self.cells[row][col]:
                    h = h + 1
                current += 1
        return h
    """

 
    
    def legalMoves( self ):
        """
          Returns a list of legal moves from the current state.
        """
        moves = []
        row, col = self.blankLocation
        if(row != 0):
            moves.append('up')
        if(row != 2):
            moves.append('down')
        if(col != 0):
            moves.append('left')
        if(col != 2):
            moves.append('right')
        return moves

    def result(self, move):
        """
          Returns a new eightPuzzle with the current state and blankLocation
        updated based on the provided move.
        """
        row, col = self.blankLocation
        if(move == 'up'):
            newrow = row - 1
            newcol = col
        elif(move == 'down'):
            newrow = row + 1
            newcol = col
        elif(move == 'left'):
            newrow = row
            newcol = col - 1
        elif(move == 'right'):
            newrow = row
            newcol = col + 1
        else:
            raise "Illegal Move"

        # Create a copy of the current eightPuzzle
        newPuzzle = EightPuzzleState([0, 0, 0, 0, 0, 0, 0, 0, 0])
        newPuzzle.cells = [values[:] for values in self.cells]
        # And update it to reflect the move
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '==' such that two eightPuzzles with the same configuration
          are equal.
        """
        for row in range( 3 ):
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        lines = []
        horizontalLine = ('-' * (13))
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()


class EightPuzzleSearchProblem(search.SearchProblem):
    """
      Implementation of a SearchProblem for the  Eight Puzzle domain

      Each state is represented by an instance of an eightPuzzle.
    """
    def __init__(self,puzzle):
        "Creates a new EightPuzzleSearchProblem which stores search information."
        self.puzzle = puzzle

    def getStartState(self):
        return puzzle

    def isGoalState(self,state):
        return state.isGoal()

    def getSuccessors(self,state):
        """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)
    

EIGHT_PUZZLE_DATA = [[1, 0, 2, 3, 4, 5, 6, 7, 8],
                     [1, 7, 8, 2, 3, 4, 5, 6, 0],
                     [4, 3, 2, 7, 0, 5, 1, 6, 8],
                     [5, 1, 3, 4, 0, 2, 6, 7, 8],
                     [1, 2, 5, 7, 6, 8, 0, 4, 3],
                     [0, 3, 1, 6, 8, 2, 7, 5, 4]]

def loadEightPuzzle(puzzleNumber):
    """
      puzzleNumber: The number of the eight puzzle to load.

      Returns an eight puzzle object generated from one of the
      provided puzzles in EIGHT_PUZZLE_DATA.

      puzzleNumber can range from 0 to 5.

      >>> print loadEightPuzzle(0)
      -------------
      | 1 |   | 2 |
      -------------
      | 3 | 4 | 5 |
      -------------
      | 6 | 7 | 8 |
      -------------
    """
    return EightPuzzleState(EIGHT_PUZZLE_DATA[puzzleNumber])

def createRandomEightPuzzle(moves=100):
    """
      moves: number of random moves to apply

      Creates a random eight puzzle by applying
      a series of 'moves' random moves to a solved
      puzzle.
    """
    puzzle = EightPuzzleState([0,1,2,3,4,5,6,7,8])
    for i in range(moves):
        # Execute a random legal move
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle

if __name__ == '__main__':

	for i in range(1,13):
	    puzzle = createRandomEightPuzzle(25)
	    print('random puzzle number %d :' % i)
	    print(puzzle)

	    problem = EightPuzzleSearchProblem(puzzle)
	    path1 = search.aStarSearch(problem)
	    path2 = search.hillClimbing(problem)
	    path3 = search.simulatedAnnealing(problem)
	    print('A* found a path of %d moves: %s' % (len(path1), str(path1)))
	    print('hill climbing found a path of %d moves: %s' % (len(path2), str(path2)))
	    print('simulated Annealing found a path of %d moves: %s' % (len(path3), str(path3)))
	    print('\n\n\n')
	"""this was for seeing puzzle for every move, not needed anymore
	    curr = puzzle
	    i = 1
	    for a in path2:
	        curr = curr.result(a)
	        print('After %d move%s: %s' % (i, ("", "s")[i>1], a))
	        print(curr)

	        raw_input("Press return for the next state...")   # wait for key stroke
	        i += 1
	
	"""

