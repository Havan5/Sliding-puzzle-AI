# -*- coding: utf-8 -*-
import numpy as np
import queue

class PuzzleState():
    SOLVED_PUZZLE = np.arange(9).reshape((3, 3))

    def __init__(self,conf,g,predState):
        self.puzzle = conf     # Configuration of the state
        self.gcost = g         # Path cost
        self._compute_heuristic_cost()  # Set heuristic cost
        self.fcost = self.gcost + self.hcost
        self.pred = predState  # Predecesor state
        self.zeroloc = np.argwhere(self.puzzle == 0)[0]
        self.action_from_pred = None
    
    def __hash__(self):
        return tuple(self.puzzle.ravel()).__hash__()
    
    def _compute_heuristic_cost(self):
        """ Updates the heuristic function value for use in A* """
        self.hcost = 0
        for num in range(1, 9):
            current_positions = np.argwhere(np.array(self.puzzle) == num)
            goal_positions = np.argwhere(PuzzleState.SOLVED_PUZZLE == num)

            self.hcost += np.abs(current_positions[0][0] - goal_positions[0][0]) + np.abs(current_positions[0][1] - goal_positions[0][1])

    def is_goal(self):
        return np.array_equal(PuzzleState.SOLVED_PUZZLE,self.puzzle)
    
    def __eq__(self, other):
        return np.array_equal(self.puzzle, other.puzzle)
    
    def __lt__(self, other):
        return self.fcost < other.fcost
    
    def __str__(self):
        return np.str(self.puzzle)
    
    move = 0
    
    def show_path(self):
        if self.pred is not None:
            self.pred.show_path()
        
        if PuzzleState.move==0:
            print('START')
        else:
            print('Move',PuzzleState.move, 'ACTION:', self.action_from_pred)
        PuzzleState.move = PuzzleState.move + 1
        print(self)
    
    def can_move(self, direction):
        if direction == 'up':
            return self.zeroloc[0] > 0
        elif direction == 'down':
            return self.zeroloc[0] < 2
        elif direction == 'left':
            return self.zeroloc[1] > 0
        elif direction == 'right':
            return self.zeroloc[1] < 2
        else:
            return False
        
    def gen_next_state(self, direction):
        next_puzzle = self.puzzle.copy()

        if direction == 'up':
            next_puzzle[self.zeroloc[0], self.zeroloc[1]] = self.puzzle[self.zeroloc[0] - 1, self.zeroloc[1]]
            next_puzzle[self.zeroloc[0] - 1, self.zeroloc[1]] = 0

        elif direction == 'down':
            next_puzzle[self.zeroloc[0], self.zeroloc[1]] = self.puzzle[self.zeroloc[0] + 1, self.zeroloc[1]]
            next_puzzle[self.zeroloc[0] + 1, self.zeroloc[1]] = 0

        elif direction == 'left':
            next_puzzle[self.zeroloc[0], self.zeroloc[1]] = self.puzzle[self.zeroloc[0], self.zeroloc[1] - 1]
            next_puzzle[self.zeroloc[0], self.zeroloc[1] - 1] = 0

        elif direction == 'right':
            next_puzzle[self.zeroloc[0], self.zeroloc[1]] = self.puzzle[self.zeroloc[0], self.zeroloc[1] + 1]
            next_puzzle[self.zeroloc[0], self.zeroloc[1] + 1] = 0
        next_state = PuzzleState(next_puzzle, self.gcost+1, self)

        next_state.action_from_pred = direction
        return next_state

print('Artificial Intelligence')
print('MP1: A* for Sliding Puzzle')
print('SEMESTER: CPSC-57100-002, 2023 Fall')
print('NAME: Havan Patel')
print()

# load random start state onto frontier priority queue
frontier = queue.PriorityQueue()
a = np.loadtxt('mp1input.txt', dtype=np.int32)
start_state = PuzzleState(a,0,None)

frontier.put(start_state)

closed_set = set()

num_states = 0
while not frontier.empty():
    #  choose state at front of priority queue
    next_state = frontier.get()
    num_states = num_states + 1

    #  if goal then quit and return path
    if next_state.is_goal():
        next_state.show_path()
        break
    
    # Add state chosen for expansion to closed_set
    closed_set.add(next_state)
    
    # Expand state (up to 4 moves possible)
    possible_moves = ['up','down','left','right']
    for move in possible_moves:
        if next_state.can_move(move):
            neighbor = next_state.gen_next_state(move)
            if neighbor in closed_set:
                continue
            if neighbor not in frontier.queue:                           
                frontier.put(neighbor)
            # If it's already in the frontier, it's gauranteed to have lower cost, so no need to update

print('\nNumber of states visited =',num_states)