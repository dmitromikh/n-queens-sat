from satispy import Variable

from make_sat import find_sat, make_cnf

class TestSat:
    def test_board_size(self):
        for i in range(2, 20):
            _, board = find_sat(i)
            assert len(board) == i
            for row in board:
                assert len(row) == i

    def test_small(self):
        for i in range(2, 4):
            solution, _ = find_sat(i)
            assert solution is None

    def test_rows(self):
        for i in range(4, 20):
            solution, board = find_sat(i)
            assert solution is not None
            for row in board:
                assert sum(map(lambda x: int(solution[x]), row)) == 1

    def test_columns(self):
        for i in range(4, 20):
            solution, board = find_sat(i)
            assert solution is not None
            for row in zip(*board):
                assert sum(map(lambda x: int(solution[x]), row)) == 1

    def test_anti_diag(self):
        for i in range(4, 20):
            solution, board = find_sat(i)
            size = len(board)
            for line in range(1, 2 * size):
                start_col = max(0, line - size)
                count = min(line, size - start_col, size)
                num_queens = 0
                for j in range(0, count):
                    num_queens += \
                        int(solution[board[min(size, line) - j - 1][start_col + j]])
    
    def test_main_diag(self):
        for i in range(4, 20):
            solution, board = find_sat(i)
            size = len(board)
            for line in range(1, 2 * size):
                start_col = max(0, line - size)
                count = min(line, size - start_col, size)
                num_queens = 0
                for j in range(0, count):
                    num_queens += \
                        int(solution[board[min(size, line) - j - 1][size - start_col - j - 1]])