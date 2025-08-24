
import math

X = "X"
O = "O"
EMPTY = None
# board = [[EMPTY, EMPTY, EMPTY],
#          [EMPTY, EMPTY, X],
#          [EMPTY, EMPTY, EMPTY]]

def graphical_board(board):
    for row in board:
        print('')
        for cell in row:
            if cell == EMPTY:
                print(f' - |', end='')
            else:
                print(f' {cell} |', end='')
    print('')


graphical_board(board)




