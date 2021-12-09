from typing import List, Tuple


RAW = """\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""


class Board:
    def _parse_str_board(self, board: str) -> List[List[int]]:
        """
        Parse a string representation of a board into a list of lists.
        """
        board = board.strip().split("\n")
        board = [list(map(int, row.split())) for row in board]
        return board

    def __init__(self, board: str):
        self.board = self._parse_str_board(board)
        self.n = len(self.board)
        self.m = len(self.board[0])
        self.board_mask = [
            [False for _ in range(self.m)] for _ in range(self.n)
        ]

    def __repr__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.board])

    def check_wining_condition(self, i: int, j: int) -> bool:
        """
        Check if the board has a winning condition.
        """
        # Check row
        if all(self.board_mask[i]):
            return True

        # Check column
        if all([x[j] for x in self.board_mask]):
            return True

        return False

    def mark_number(self, number: int) -> bool:
        """
        Check if a number is present in the board and mark it if so.
        """
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] == number:
                    self.board_mask[i][j] = True
                    return self.check_wining_condition(i, j)
        return False

    def get_sum_unmasked(self) -> int:
        """
        Get the sum of all unmasked numbers.
        """
        s = 0
        for i in range(self.n):
            for j in range(self.m):
                if not self.board_mask[i][j]:
                    s += self.board[i][j]
        return s


def parse(raw: str) -> Tuple[List[int], List[Board]]:
    data = raw.strip().split("\n\n")
    numbers = list(map(int, data[0].split(",")))
    boards = [Board(x) for x in data[1:]]

    return numbers, boards


def find_winning_board(
    numbers: List[int], boards: List[Board]
) -> Tuple[int, Board]:
    for number in numbers:
        for board in boards:
            if board.mark_number(number):
                return number, board
    return None, None


if __name__ == "__main__":
    numbers, boards = parse(RAW)
    number, winner_board = find_winning_board(numbers, boards)
    assert (winner_board.get_sum_unmasked() * number) == 4512

    with open("data/04.txt") as f:
        numbers, boards = parse(f.read())
    number, winner_board = find_winning_board(numbers, boards)
    print(winner_board.get_sum_unmasked() * number)
