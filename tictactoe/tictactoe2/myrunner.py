import tictactoe as ttt
import time


# Rules
X = "X"
O = "O"
EMPTY = None
players = [O, X]
acceptable = [1, 2, 3]
yes = ['yes', 'YES', 'y', 'Y']
no = ['no', 'NO', 'n', 'N']
done_moves = []




def main():
    time.sleep(1/2)
    print('Welcome to Tic Tac Toe!')
    time.sleep(1)
    print('To play this game, select your letter at the prompt (X is first!) and input your action!')
    time.sleep(3)
    print('Squares are selected by row then column. For example, the middle right square is 2 3 and the top middle square is 1 2.', '\n')
    time.sleep(2)

    while True:
        human = input("When you're ready, pick your letter -- X or O: ")
        human = human.upper()
        if human == X:
            cpu = O
            break
        elif human == O:
            cpu = X
            break

    time.sleep(1/2)
    print('\nYou will not win!!')
    time.sleep(1/2)

    board = initial_state()

    while True:
        time.sleep(1/2)
        graphical_board(board)
        print('')
        if ttt.terminal(board):
            winner = ttt.winner(board)
            if winner == X:
                time.sleep(1)
                print('X is the winner!')
                print('\n')
                ask_for_another()
            if winner == O:
                time.sleep(1)
                print('O is the winner!')
                print('\n')
                ask_for_another()
            elif winner == None:
                time.sleep(1)
                print("It's a draw!")
                print('\n')
                ask_for_another()
            break

        elif ttt.player(board) == human:

            while True:
                move = get_human_action()
                if move in ttt.actions(board):
                    done_moves.append(move)
                    board = ttt.result(board, move)
                    break
                elif move in done_moves:
                    print('invalid action -- spot may be taken')
                elif move[0] not in acceptable or move[1] not in acceptable:
                    print('invalid action -- Usage: "1 3" (for first row third column)')


        elif ttt.player(board) == cpu:
            time.sleep(1)
            move = ttt.minimax(board)
            done_moves.append(move)
            board = ttt.result(board, move)












def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def graphical_board(board):
    for row in board:
        print('')
        for cell in row:
            if cell == EMPTY:
                print(f' - |', end='')
            else:
                print(f' {cell} |', end='')
    print('')

def get_human_action():
    while True:
        action = input('Action: ')
        action = action.split()
        try:
            move = tuple(int(value) for value in action)
            move = tuple(value - 1 for value in move)
            return move
        except ValueError:
            print('invalid action -- Usage: "1 3" (for first row third column)')

def ask_for_another():
    while True:
        choice = input('Wanna try again? (y/n) ')
        print('')
        if choice in yes:
            main()
            break
        elif choice in no:
            break
        else:
            print("Sorry, I don't understand\n")

main()
