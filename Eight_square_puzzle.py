"""The classic 8 tiles puzzle where we have to figure out how many tiles are in the correct spot"""
class EightSquare:
    def __init__(self):
        self.puzzle = [[0]*3]*3

    def set_state(self, num0: int, num1: int, num2: int, num3: int, 
                  num4: int, num5: int, num6: int, num7: int, num8: int) -> None:
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

    def calculate_heuristic_one(self, array) -> int:
        """Heuristic 1 gets the number of misplaced tiles in the current state"""
        incorrect_tiles: int = 0
        for rows in range(3):
            for columns in range(3):
                if array[rows][columns] != rows+columns:
                    incorrect_tiles += 1
        return incorrect_tiles

    def calculate_heuristic_two(self, array) -> int:
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

    def check_if_goal(self) -> bool:
        """Checks the puzzle to see if we have completed it"""
        reached_goal: bool = True
        while reached_goal:
            for rows in range(3):
                for columns in range(3):
                    reached_goal = self.puzzle[rows][columns] == (rows+columns)

        return reached_goal
                
