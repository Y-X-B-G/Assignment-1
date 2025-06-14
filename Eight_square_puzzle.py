import random
import heapq
import copy
import math
from typing import Callable

"""The classic 8 tiles puzzle where we have to figure out how many tiles are in the correct spot"""
class EightSquare:
    def __init__(self):
        self.puzzle: list[int] = [[0 for i in range(3)] for j in range(3)]
        self.zero: list[int, int] = [None, None]

    def set_state(self, num0: int, num1: int, num2: int, num3: int,
                  num4: int, num5: int, num6: int, num7: int, num8: int,
                  zero: list[int]) -> None:
        """ 
        Sets the initial state of the puzzle
        Does not validate that the puzzle is in an valid state 
        The blank tile must be marked 0
        """
        self.puzzle[0][0] = num0
        self.puzzle[0][1] = num1
        self.puzzle[0][2] = num2
        self.puzzle[1][0] = num3
        self.puzzle[1][1] = num4
        self.puzzle[1][2] = num5
        self.puzzle[2][0] = num6
        self.puzzle[2][1] = num7
        self.puzzle[2][2] = num8
        self.zero = zero

    def copy(self) -> 'EightSquare':
        """Creates a deepcopy of the current object"""
        return copy.deepcopy(self)

    def set_goal(self):
        """Sets the puzzle to the goal state"""
        for rows in range(3):
            for columns in range(3):
                #print(3*rows + columns)
                self.puzzle[rows][columns] = (3*rows + columns)
                #print(self.puzzle[rows][columns])
        self.zero = [0,0]

    def randomize(self):
        """Create a random permutation of the puzzle by checking the order of each orbit
           odd orbits take an even number of swaps and even orbits take an odd number of swaps
           odd + odd = even, even + even is even, odd + even  = odd"""
        
        """
        visited: list = [0,0,0,0,0,0,0,0,0]
        permutation: list = [0,1,2,3,4,5,6,7,8]
        random.shuffle(permutation)
        count: int = 0
        for i in range(9):
            initial: int = permutation[i] 
            current: int = permutation[i]
            if (visited[current] != 1): #Check if this was part of a previous cycle
                visited[current] = 1
                while permutation[current] != initial:
                    current = permutation[current]
                    visited[current] = 1
                    count += 1

        if (permutation.index(0)%2 == 0 and count%2 != 0) or (permutation.index(0)%2 == 1 and count%2 != 1):
            permutation[7], permutation[8] = permutation[8], permutation[7]
        """

        permutation: list = [0,1,2,3,4,5,6,7,8]
        random.shuffle(permutation)
        count: int = 0
        for i in range(len(permutation)):
            for j in range (i+1, len(permutation)):
                if permutation[i] != 0 and permutation[j] != 0 and permutation[i] > permutation[j]:
                    count += 1

        if count%2 == 1:
            if permutation[5] == 0 or permutation[4] == 0:
                permutation[7], permutation[8] = permutation[8], permutation[7]
            else:
                permutation[5], permutation[4] = permutation[4], permutation[5]

        for rows in range(3):
            for columns in range(3):
                self.puzzle[rows][columns] = permutation[3*rows + columns]

        where_is_zero: int = permutation.index(0)

        if where_is_zero == 0:
            self.zero = [0,0]
        elif where_is_zero == 1:
            self.zero = [0,1]
        elif where_is_zero == 2:
            self.zero = [0,2]
        elif where_is_zero == 3:
            self.zero = [1,0]
        elif where_is_zero == 4:
            self.zero = [1,1]
        elif where_is_zero == 5:
            self.zero = [1,2]
        elif where_is_zero == 6:
            self.zero = [2,0]
        elif where_is_zero == 7:
            self.zero = [2,1]
        else:
            self.zero = [2,2]


    def calculate_heuristic_one(self, array: 'EightSquare') -> int:
        """Heuristic 1 gets the number of misplaced tiles in the current state"""
        incorrect_tiles: int = 0
        for rows in range(3):
            for columns in range(3):
                if array.puzzle[rows][columns] != 3*rows+columns:
                    incorrect_tiles += 1
        return incorrect_tiles

    def calculate_heuristic_two(self, array: 'EightSquare') -> int:
        """Heruistic 2 gets the Manhattan distance for all times from its correct location"""
        sum_of_distance: int = 0
        for rows in range(3):
            for columns in range(3):
                if array.puzzle[rows][columns] == 0:
                    sum_of_distance = sum_of_distance + abs(rows - 0) + abs(columns - 0)
                elif array.puzzle[rows][columns] == 1:
                    sum_of_distance = sum_of_distance + abs(rows - 0) + abs(columns - 1)
                elif array.puzzle[rows][columns] == 2:
                    sum_of_distance = sum_of_distance + abs(rows - 0) + abs(columns - 2)
                elif array.puzzle[rows][columns] == 3:
                    sum_of_distance = sum_of_distance + abs(rows - 1) + abs(columns - 0)
                elif array.puzzle[rows][columns] == 4:
                    sum_of_distance = sum_of_distance + abs(rows - 1) + abs(columns - 1)
                elif array.puzzle[rows][columns] == 5:
                    sum_of_distance = sum_of_distance + abs(rows - 1) + abs(columns - 2)
                elif array.puzzle[rows][columns] == 6:
                    sum_of_distance = sum_of_distance + abs(rows - 2) + abs(columns - 0)
                elif array.puzzle[rows][columns] == 7:
                    sum_of_distance = sum_of_distance + abs(rows - 2) + abs(columns - 1)
                elif array.puzzle[rows][columns] == 8:
                    sum_of_distance = sum_of_distance + abs(rows - 2) + abs(columns - 2)

        return sum_of_distance
    
    def calculate_heuristic_three(self, array: 'EightSquare') -> int:
        euclidian_distance: int = 0
        for rows in range(3):
            for columns in range(3):
                if array.puzzle[rows][columns] == 0:
                    euclidian_distance = euclidian_distance + math.sqrt(abs(rows - 0)**2 + abs(columns - 0)**2) 
                elif array.puzzle[rows][columns] == 1:
                    euclidian_distance = euclidian_distance + math.sqrt(abs(rows - 0)**2 + abs(columns - 1)**2)
                elif array.puzzle[rows][columns] == 2:
                    euclidian_distance = euclidian_distance + math.sqrt(abs(rows - 0)**2 + abs(columns - 2)**2)
                elif array.puzzle[rows][columns] == 3:
                    euclidian_distance = euclidian_distance + math.sqrt(abs(rows - 1)**2 + abs(columns - 0)**2)
                elif array.puzzle[rows][columns] == 4:
                    euclidian_distance = euclidian_distance + math.sqrt(abs(rows - 1)**2 + abs(columns - 1)**2)
                elif array.puzzle[rows][columns] == 5:
                    euclidian_distance = euclidian_distance + math.sqrt(abs(rows - 1)**2 + abs(columns - 2)**2)
                elif array.puzzle[rows][columns] == 6:
                    euclidian_distance = euclidian_distance + math.sqrt(abs(rows - 2)**2 + abs(columns - 0)**2)
                elif array.puzzle[rows][columns] == 7:
                    euclidian_distance = euclidian_distance + math.sqrt(abs(rows - 2)**2 + abs(columns - 1)**2)
                elif array.puzzle[rows][columns] == 8:
                    euclidian_distance = euclidian_distance + math.sqrt(abs(rows - 2)**2 + abs(columns - 2)**2)

        return euclidian_distance


    def check_if_goal(self, array: 'EightSquare') -> bool:
        """Checks the puzzle to see if we have completed it"""
        reached_goal: bool = True
        for rows in range(3):
            for columns in range(3):
                if array.puzzle[rows][columns] != (3*rows+columns):
                    return False
        return reached_goal
    
    def get_neighbors(self, array: 'EightSquare') -> list['EightSquare']:
        location: list[int] = array.zero
        neighbors: list['EightSquare'] = []
        valid_directions: list[int] = [0,0,0,0] #up, down, left, right

        if location[0] == 0:
            valid_directions[1] = 1
        elif location[0] == 1:
            valid_directions[0] = 1
            valid_directions[1] = 1
        else:
            valid_directions[0] = 1

        if location[1] == 0:
            valid_directions[3] = 1
        elif location[1] == 1:
            valid_directions[2] = 1
            valid_directions[3] = 1
        else:
            valid_directions[2] = 1

        for i, value in enumerate(valid_directions):
            if value == 1:
                new_state: 'EightSquare' = array.copy()
                if i == 0:
                    new_state.puzzle[new_state.zero[0]][new_state.zero[1]], new_state.puzzle[new_state.zero[0]-1][new_state.zero[1]] = \
                        new_state.puzzle[new_state.zero[0]-1][new_state.zero[1]], new_state.puzzle[new_state.zero[0]][new_state.zero[1]]
                    new_state.zero[0] -= 1
                elif i == 1:
                    new_state.puzzle[new_state.zero[0]][new_state.zero[1]], new_state.puzzle[new_state.zero[0]+1][new_state.zero[1]] = \
                        new_state.puzzle[new_state.zero[0]+1][new_state.zero[1]], new_state.puzzle[new_state.zero[0]][new_state.zero[1]]
                    new_state.zero[0] += 1
                elif i == 2:
                    new_state.puzzle[new_state.zero[0]][new_state.zero[1]], new_state.puzzle[new_state.zero[0]][new_state.zero[1]-1] = \
                        new_state.puzzle[new_state.zero[0]][new_state.zero[1]-1], new_state.puzzle[new_state.zero[0]][new_state.zero[1]]
                    new_state.zero[1] -= 1
                else:
                    new_state.puzzle[new_state.zero[0]][new_state.zero[1]], new_state.puzzle[new_state.zero[0]][new_state.zero[1]+1] = \
                        new_state.puzzle[new_state.zero[0]][new_state.zero[1]+1], new_state.puzzle[new_state.zero[0]][new_state.zero[1]]
                    new_state.zero[1] += 1
                neighbors.append(new_state)

        return neighbors
    
    def solve_eight(self, heuristic: Callable[['EightSquare'], list]) -> int:
        """Counts the number of steps it takes to solve the current square puzzle"""
        steps: int = 0
        priority: int = 0 #needed to break ties in the heap
        heap: list[tuple[int, 'EightSquare']] = []
        visited = set()
        heapq.heappush(heap, (heuristic(self, self), priority, self))
        priority += 1
        #print(heap[0][1])

        while len(heap) != 0:
            front: tuple[int, int, 'EightSquare'] = heapq.heappop(heap)
            #print(front[2])
            hashable_array = tuple(tuple(row) for row in front[2].puzzle)
            visited.add(hashable_array)

            if self.check_if_goal(front[2]):
                return steps

            steps += 1

            for neighbor in self.get_neighbors(front[2]):
                hashable_array = tuple(tuple(row) for row in neighbor.puzzle)
                if hashable_array not in visited:
                    heapq.heappush(heap, (heuristic(self, neighbor), priority, neighbor))
                    priority += 1

        return steps

    def __str__ (self) -> str:
        return f'{self.puzzle[0][0]}|{self.puzzle[0][1]}|{self.puzzle[0][2]}\n{self.puzzle[1][0]}|{self.puzzle[1][1]}|{self.puzzle[1][2]}\n{self.puzzle[2][0]}|{self.puzzle[2][1]}|{self.puzzle[2][2]}\n{self.zero}\n'

    def __hash__ (self):
        return hash(f'{self.puzzle[0][0]}|{self.puzzle[0][1]}|{self.puzzle[0][2]}\n{self.puzzle[1][0]}|{self.puzzle[1][1]}|{self.puzzle[1][2]}\n{self.puzzle[2][0]}|{self.puzzle[2][1]}|{self.puzzle[2][2]}\n{self.zero}\n')


def main():
    #Single test passed
    #single test heuristic_one
    """
    print("Single test")
    single: EightSquare = EightSquare()
    single.set_state(0,4,1,7,5,6,8,3,2,[0,0])
    #print(single)
    print(single.solve_eight(EightSquare.calculate_heuristic_one))
    """

    #Random test passed
    #Random test heuristic_one
    """
    print("Random test")
    randomtest: EightSquare = EightSquare()
    randomtest.randomize()
    print(randomtest.solve_eight(EightSquare.calculate_heuristic_one))
    """

    #Random test passed
    #Random test heuristic_two
    """
    print("Random test")
    randomtest: EightSquare = EightSquare()
    randomtest.randomize()
    print(randomtest.solve_eight(EightSquare.calculate_heuristic_two))
    """

    random_puzzles = []
    for i in range(100):
        puzzle: EightSquare = EightSquare()
        puzzle.randomize()
        random_puzzles.append(puzzle)

    heruistic_one_steps = []
    heruistic_two_steps = []
    heruistic_three_steps = []
    for puzzle in random_puzzles:
        heruistic_one_steps.append(puzzle.solve_eight(EightSquare.calculate_heuristic_one))
        heruistic_two_steps.append(puzzle.solve_eight(EightSquare.calculate_heuristic_two))
        heruistic_three_steps.append(puzzle.solve_eight(EightSquare.calculate_heuristic_three))

    print(sum(heruistic_one_steps)/len(heruistic_one_steps))
    print(sum(heruistic_two_steps)/len(heruistic_two_steps))
    print(sum(heruistic_three_steps)/len(heruistic_three_steps))


main()