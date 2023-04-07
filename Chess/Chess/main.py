board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]
def print_board(board):
    for i, row in enumerate(board):
        print('|'.join(row))
        if i < len(board) - 1:
            print('-' * 5)

def make_move(board, row, col, player):
    board[row][col] = player

make_move(board, 0, 0, 'X')
print_board(board)

list1 = [1, 2, 3]
list2 = [4, 5, 6]

# Using the append method
list1.append(list2)
print(list1)  # Output: [1, 2, 3, [4, 5, 6]]

# Using the + operator
list1 = [1, 2, 3]
list1 += [list2]
print(list1)  # Output: [1, 2, 3, [4, 5, 6]]

list1 = [1, 2, 3]
list2 = [4, 5, 6]

# Using the extend method
list1.extend(list2)
print(list1)  # Output: [1, 2, 3, 4, 5, 6]
