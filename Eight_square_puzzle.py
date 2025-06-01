import random
import heapq
import copy
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
                print(self.puzzle[rows][columns])
        self.zero = [0,0]

    def randomize(self):
        """Create a random permutation of the puzzle by checking the order of each orbit
           odd orbits take an even number of swaps and even orbits take an odd number of swaps
           odd + odd = even, even + even is even, odd + even  = odd"""
        visited: list = [0,0,0,0,0,0,0,0,0]
        permutation: list = [0,1,2,3,4,5,6,7,8]
        random.shuffle(permutation)
        count: int = 0
        for i in range(9):
            initial: int = permutation[i] 
            current: int = permutation[i]
            if (visited[current] != 1): #Check if this was part of a pervious cycle
                visited[current] = 1
                while permutation[current] != initial:
                    current = permutation[current]
                    visited[current] = 1
                    count += 1

        if (permutation.index(0)%2 == 0 and count%2 != 0) or (permutation.index(0)%2 == 1 and count%2 != 1):
            permutation[7], permutation[8] = permutation[8], permutation[7]

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
                if array[rows][columns] == 0:
                    sum_of_distance = sum_of_distance + abs(rows - 0) + abs(columns - 0)
                elif array[rows][columns] == 1:
                    sum_of_distance = sum_of_distance + abs(rows - 0) + abs(columns - 1)
                elif array[rows][columns] == 2:
                    sum_of_distance = sum_of_distance + abs(rows - 0) + abs(columns - 2)
                elif array[rows][columns] == 3:
                    sum_of_distance = sum_of_distance + abs(rows - 1) + abs(columns - 0)
                elif array[rows][columns] == 4:
                    sum_of_distance = sum_of_distance + abs(rows - 1) + abs(columns - 1)
                elif array[rows][columns] == 5:
                    sum_of_distance = sum_of_distance + abs(rows - 1) + abs(columns - 2)
                elif array[rows][columns] == 6:
                    sum_of_distance = sum_of_distance + abs(rows - 2) + abs(columns - 0)
                elif array[rows][columns] == 7:
                    sum_of_distance = sum_of_distance + abs(rows - 2) + abs(columns - 1)
                elif array[rows][columns] == 8:
                    sum_of_distance = sum_of_distance + abs(rows - 2) + abs(columns - 2)

        return sum_of_distance

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
    
    def solve_eight(self, heuristic: Callable['EightSquare', 'EightSquare']) -> int:
        """Counts the number of steps it takes to solve the current square puzzle"""
        steps: int = 0
        heap: list[tuple[int, 'EightSquare']] = []
        visited = set()
        heapq.heappush(heap, (heuristic(self, self), self)) 

        while not heap:
            front: tuple[int, 'EightSquare'] = heapq.heappop(heap)
            visited.add(front)
            steps += 1

            if self.check_if_goal(front[1]):
                return steps

            for neighbor in self.get_neighbors(front[1]):
                if neighbor not in visited and neighbor not in heap:
                    heapq.heappush(heap, (heuristic(self, neighbor), neighbor))

        return steps

    def __str__ (self) -> str:
        return f'{self.puzzle[0][0]}|{self.puzzle[0][1]}|{self.puzzle[0][2]}\n{self.puzzle[1][0]}|{self.puzzle[1][1]}|{self.puzzle[1][2]}\n{self.puzzle[2][0]}|{self.puzzle[2][1]}|{self.puzzle[2][2]}\n{self.zero}\n'



def main():
    #single test
    single: EightSquare = EightSquare()
    single.set_state(1,0,2,3,4,5,6,7,8,[0,0])
    print(single)
    single.solve_eight(EightSquare.calculate_heuristic_one)

main()