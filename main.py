from board import *
from tkinter import Canvas, Tk
from PIL import Image, ImageTk

global piece  # global variable for deciding which piece is currently being moved

# constants
BOARD_LENGTH = 600
PIECE_SIZE = int(BOARD_LENGTH / 10)


# return which block on board the mouse is current at
def get_loc_on_board(x, y):
    return int(y / BOARD_LENGTH * 8), int(x / BOARD_LENGTH * 8)  # (rank, file)


# get the center of the block the mouse is currently at
def get_loc_center(loc):
    rank, file = loc
    return file * BOARD_LENGTH / 8 + BOARD_LENGTH / 8 / 2, rank * BOARD_LENGTH / 8 + BOARD_LENGTH / 8 / 2


window = Tk()
window.title('Chess!')
canvas = Canvas(window, width=BOARD_LENGTH, height=BOARD_LENGTH)
canvas.pack()
# draw the lines
color = "white"
for i in range(9):
    for j in range(9):

        canvas.create_rectangle(i * BOARD_LENGTH / 8, j * BOARD_LENGTH / 8, i * BOARD_LENGTH / 8 + BOARD_LENGTH / 8,
                                j * BOARD_LENGTH / 8 + BOARD_LENGTH / 8, fill=color)
        if color == "green":
            color = "white"
        else:
            color = "green"

board = Board()

for rank in board.grid:
    for block in rank:
        if block is not None:
            block.resize_image(PIECE_SIZE, PIECE_SIZE)
            block.id = canvas.create_image(get_loc_center(block.loc), anchor='center', image=block.photo_image)


def stick_piece_on_cursor(event):
    global piece
    canvas.delete(piece.id)
    piece.id = canvas.create_image((event.x - PIECE_SIZE / 2, event.y - PIECE_SIZE / 2), anchor='nw',
                                   image=piece.photo_image)


def move(piece, loc):
    canvas.delete(piece.id)
    pieces = board.move(piece, loc)
    for p in pieces:
        canvas.delete(p.id)
        p.id = canvas.create_image(get_loc_center(p.loc), anchor='center', image=p.photo_image)

    if board.check_mate(board.active_color):
        game_end()


def game_end():
    # TODO
    print("check mated")
    pass


def promote_pawn(pawn):
    # TODO
    pass


def on_press(event):
    rank, file = get_loc_on_board(event.x, event.y)
    global piece
    piece = board.grid[rank][file]
    if piece is not None and board.active_color != piece.color:
        piece = None


def on_hold(event):
    if piece is not None:
        stick_piece_on_cursor(event)


def on_release(event):
    global piece
    if piece is not None:
        move(piece, get_loc_on_board(event.x, event.y))
    piece = None


canvas.bind('<Button-1>', on_press)
canvas.bind('<B1-Motion>', on_hold)
canvas.bind('<ButtonRelease-1>', on_release)

window.mainloop()
