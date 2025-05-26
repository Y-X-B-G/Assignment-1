class eight_square:
    def __init__(self):
        self.puzzle = [[0]*3]*3

    def set_state(self, num1: int, num2: int, num3: int, num4: int, num5: int, num6: int, num7: int, num8: int, num9: int):
        self.puzzle[1] = num1