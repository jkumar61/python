import json

from flask import Flask, render_template

from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

board = [
    ["__", "__", "__"],
    ["__", "__", "__"],
    ["__", "__", "__"]
]
user = True  # when user is true it means it is X otherwise it is 0
turns = 0


@app.route('/games', methods=['POST', 'GET'])
def print_board(board):
    for row in board:
        for slot in row:
            print(f"{slot} ", end="")
        print()


def quit(user_input):
    if user_input.lower() == "q":
        print("Thanks for playing")
        return True
    else:
        return False


def check_input(user_input):
    # check if it is a number?
    if not is_num(user_input):
        return False
    user_input = int(user_input)
    # checking if it is 1 - 9
    if not bounds(user_input):
        return False
    return True


def is_num(user_input):
    if not user_input.isnumeric():
        print("This is not a valid number")
        return False
    else:
        return True


def bounds(user_input):
    if user_input > 9 or user_input < 1:
        print("This number is out of required range.")
        return False
    else:
        return True


def space_taken(coords, board):
    row = coords[0]
    col = coords[1]
    if board[row][col] != "__":
        print("This postion is already taken.")
        return True
    else:
        return False


def coordinates(user_input):
    row = int(user_input / 3)
    col = user_input
    if col > 2:
        col = int(col % 3)
    return row, col


def add_to_board(coords, board, active_user):
    row = coords[0]
    col = coords[1]
    board[row][col] = active_user


def current_user(user):
    if user:
        return "X"
    else:
        return "0"


def iswin(user, board):
    if check_row(user, board):
        return True
    if check_col(user, board):
        return True
    if check_diagonal(user, board):
        return True
    return False


def check_row(user, board):
    for row in board:
        complete_row = True
        for slot in row:
            if slot != user:
                complete_row = False
                break
        if complete_row:
            return True
    return False


def check_col(user, board):
    for col in range(3):
        complete_col = True
        for row in range(3):
            if board[row][col] != user:
                complete_col = False
                break
        if complete_col:
            return True
    return False


def check_diagonal(user, board):
    if board[0][0] == user and board[1][1] == user and board[2][2] == user:
        return True
    elif board[0][2] == user and board[1][1] == user and board[2][0] == user:
        return True
    else:
        return False


while turns < 9:
    active_user = current_user(user)
    print_board(board)
    user_input = input("Please enter a position 1 through 9 or enter \"q\"to quit: ")
    if quit(user_input):
        break
    if not check_input(user_input):
        print("Please try again")
        continue
    # We have to do it to make the number same as index, index is 0-8 and we are
    # getting the input from 1 - 9
    user_input = int(user_input) - 1
    coords = coordinates(user_input)
    if space_taken(coords, board):
        print("please try again")
        continue
    add_to_board(coords, board, active_user)
    if iswin(active_user, board):
        print(f"{active_user.upper()} Won!")
        break
    turns += 1
    if turns == 9:
        print("Tie!")
    user = not user

if __name__ == '__main__':
    app.run(port=8081)

