from functools import reduce
from itertools import combinations

from satispy import Variable
from satispy.solver import Minisat


def make_cnf(clauses):
    return reduce(lambda x, y: x & y, 
                  [reduce(lambda x, y: x | y, clause)
                        for clause in clauses])


def make_negated_dnf(clauses):
    pairs = [(-fst, -snd) for clause in clauses 
                for (fst, snd) in combinations(clause, 2)]
    return make_cnf(pairs)


def find_sat(n):
    assert n > 1
    board = [[Variable(str(i) + 'v' + str(j)) for i in range(n)]
             for j in range(n)]
    queens = make_cnf(board)
    row_cnf = make_negated_dnf(board)
    col_cnf = make_negated_dnf(zip(*board))
    main_diag = [[board[min(n, line) - j - 1][n - max(0, line - n) - j - 1]
                  for j in range(0, min(line, n, n - max(0, line - n)))]
                      for line in range(1, 2 * n)]
    main_cnf = make_negated_dnf(main_diag)
    anti_diag = [[board[min(n, line) - j - 1][max(0, line - n) + j]
                  for j in range(0, min(line, n, n - max(0, line - n)))]
                      for line in range(1, 2 * n)]
    anti_cnf = make_negated_dnf(anti_diag)
    
    solver = Minisat()
    solution = solver.solve(queens & row_cnf & col_cnf & main_cnf & anti_cnf)

    if solution.success:
        return solution, board
    else:
        return None, board


if __name__=="__main__":
    n = int(input())
    solution, board = find_sat(n)
    
    if solution is not None:
        print('Found a solution:')
        for row in board:
            print(list(map(lambda x: int(solution[x]), row)))
    else:
        print('There is no such an arrangement')
