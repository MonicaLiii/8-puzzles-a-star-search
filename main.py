# ***********************************************************************************************************
# 8 Puzzle Problem
# Tiles are numbered, 1 thru 8 for the 8-puzzle, so that each tile can be uniquely identified. The aim of
# the puzzle is to achieve a given configuration of tiles from a given (different) configuration by sliding
# the individual tiles around the grid as described above.
# (Reference: Google)
# ***********************************************************************************************************
# Solver: This python program is an AI solver of a 8 Puzzle Game using A* search algorithm,
# written by YM Li, in Fall 2018.
# ***********************************************************************************************************

import heapq, random

goal_board = [[0,1,2], [3,4,5], [6,7,8]]

class Puzzle:
    """
    Initials the 8 puzzle game and the solver using A* algorithm with manhattan distance as heuristic func.
    """
    def __init__(self, board):
        self.board = board # a 2D array input representing the board.
        self.cost = 0 # depth of current board.
        self.h = 0
        self.parent = None

    def print(self):
        """
        Prints out the current board.
        """
        for i in range(0,3):
            for j in range(0,3):
                if self.board[i][j] == 0:
                    print(" ", end=" ")
                else:
                    print(self.board[i][j], end=" ")
            print("\n", end="")

    def isGoal(self):
        """
        Checks the goal states.
        The specific goal state is:
                          1 2
                        3 4 5
                        6 7 8
                                    for this game.
        :return (bool) True - if current board match the goal board,
                 (bool) False - otherwise.
        """
        for i in range(0,3):
            for j in range(0,3):
                # if there is a difference btw current board and goal board, return False.
                if self.board[i][j] != goal_board[i][j]:
                    return False
        # otherwise, return True.
        return True

    def isEqual(self, other_state):
        return self.board == other_state.board

    def getIndex(self, num):
        """
        Get the index to move of a specific number in current board.
        :return: (int tuple) i,j - index of the number waiting for check,
                  (int tuple) 999,999 - if there is no such a number (ERROR msg).
        """
        for i in range(0,3):
            for j in range(0,3):
                if self.board[i][j] == num:
                    return (i,j)
        return (999,999)

    def getLegalMoves(self):
        """
        Get the available items to move according to current blank.
        :return: (tuple array) moves - array of tuples representing indices of legal moves.
        """
        moves = []
        legal_move = self.getIndex(0) # NOTICE: if there is a legal move, it should be 0.

        if legal_move == (0,0):
            moves.append((0,1))
            moves.append((1,0))
        elif legal_move == (0,1):
            moves.append((0,0))
            moves.append((0,2))
            moves.append((1,1))
        elif legal_move == (0,2):
            moves.append((0,1))
            moves.append((1,2))
        elif legal_move == (1,0):
            moves.append((0,0))
            moves.append((1,1))
            moves.append((2,0))
        elif legal_move == (1,1):
            moves.append((0,1))
            moves.append((1,0))
            moves.append((1,2))
            moves.append((2,1))
        elif legal_move == (1,2):
            moves.append((0,2))
            moves.append((1,1))
            moves.append((2,2))
        elif legal_move == (2,0):
            moves.append((1,0))
            moves.append((2,1))
        elif legal_move == (2,1):
            moves.append((1,1))
            moves.append((2,0))
            moves.append((2,2))
        else: #legal_move = (2,2)
            moves.append((1,2))
            moves.append((2,1))

        return moves

    def swapBoard(self, blank_index, legal_move_index):
        """
        Swaps the value at specific index at current board.
        :param (int tuple) blank_index - the index of blank
        :param (int tuple) legal_move_index - the index of variable waiting for swap
        """
        temp = self.board[legal_move_index[0]][legal_move_index[1]]
        #print("temp: "+ str(temp))
        self.board[legal_move_index[0]][legal_move_index[1]] = 0
        self.board[blank_index[0]][blank_index[1]] = temp
        #print("***")
        #self.print()

    def copyBoard(self):
        """
        Copies self.board .
        :return (int array) copy_board - a copy of self.board
        """
        copy_board = [[0,0,0],[0,0,0],[0,0,0]]
        for i in range(0,3):
            for j in range(0,3):
                copy_board[i][j] = self.board[i][j]
        return copy_board

    def heuristicFunction(self):
        """
        Implements a heuristic function h(n) using manhattan distance function.
        Notice that f(n) = g(n) + h(n).
        :return (int) distance - the manhattan distance of current node.
        """
        distance = 0
        for i in range(0,3):
            for j in range(0,3):
                value = self.board[i][j]
                if value != 0:
                    target_row = int(value / 3)
                    target_col = value % 3
                    d_row = i - target_row
                    d_col = j - target_col
                    distance += abs(d_row) + abs(d_col)
        # self.cost += distance
        return distance

    def getChildren(self):
        """
        Gets all children of current board.
        :return (puzzle array) children_states - an array storing all children puzzle objs of current board.
        """
        blank = self.getIndex(0)
        legals = self.getLegalMoves()

        children_num = len(legals)
        children_states = []
        for i in range(0, children_num):
            temp_board = self.copyBoard()
            temp = Puzzle(temp_board)
            temp.swapBoard(blank, legals[i])
            child_board = temp.copyBoard()
            child = Puzzle(child_board)
            child.cost = self.cost + 1
            child.parent = self
            children_states.append(child)

        return children_states

    def AStarSearch(self):
        """
        A* search.
        :return (puzzle array) tracks - the path return
        """
        initial_state = Puzzle(self.board)
        initial_value = initial_state.heuristicFunction()
        frontier = PriorityQueue()
        frontier.push(initial_state, initial_value)
        explored = []
        tracks = []
        moves = 0
        while not frontier.isEmpty():
            state_to_check = frontier.pop()
            if state_to_check.isGoal():
                self.board = state_to_check.board
                while state_to_check.parent != None:
                    #state_to_check.print()
                    tracks.append(state_to_check)
                    state_to_check = state_to_check.parent
                tracks.reverse()
                return tracks
            moves += 1
            if state_to_check.board not in explored:
                explored.append(state_to_check.board)
                childrens = state_to_check.getChildren()
                for state in childrens:
                    frontier.push(state, state.cost + state.heuristicFunction())
        return tracks

    def printSteps(self):
        print("Welcome! Here is the initial board.\nIf you wanna test other boards, dive into the code!")
        self.print()
        tracks = self.AStarSearch()
        for i in range(0, len(tracks)):
            print("This is step "+str(i+1))
            tracks[i].print()
        print("Congratulations! You've solved the board!\n")


class PriorityQueue:
    """
      Applies the priority queue data structure.
      Items inserted is in the order of values related to them.
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


def main():
    #board = [[7,2,4],[5,0,6],[8,3,1]]
    board = [[8,0,6],[5,4,7],[2,3,1]]
    #board = [[1,2,5],[3,0,4],[6,7,8]]
    puzzle = Puzzle(board)
    #puzzle.print()
    # ****************************************
    #   Here are lines to test functions.
    # ****************************************
    #print(puzzle.getIndex(0))
    #for i in puzzle.getLegalMoves():
    #   print(puzzle.board[i[0]][i[1]])
    #childrens = puzzle.getChildren()
    #for i in range(0,4):
    #   childrens[i].print()
    # ****************************************
    #puzzle.AStarSearch()
    puzzle.printSteps()
    #puzzle.print()

if __name__ == "__main__":
    main()

