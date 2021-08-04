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
    rank, file = loc
    canvas.delete(piece.id)
    if board.is_legal_move(piece, (rank, file)):  # if it is a legal move
        loc = piece.loc
        # check if the move is en passant
        if piece.kind == PAWN and (rank, file) == board.en_passant:
            if piece.color == WHITE:
                board.grid[rank + 1][file] = None
            else:  # if black
                board.grid[rank - 1][file] = None

        # check if the move would create possibility for en passant
        board.en_passant = None
        if piece.kind == PAWN:
            if piece.loc[0] == 1 and rank == 3:
                board.en_passant = (2, file)
            elif piece.loc[0] == 6 and rank == 4:
                board.en_passant = (5, file)

        # move the peace
        piece.id = canvas.create_image(get_loc_center((rank, file)), anchor='center', image=piece.photo_image)
        board.grid[rank][file] = piece
        piece.loc = (rank, file)
        if board.in_check(piece.color):
            canvas.delete(piece.id)
            rank, file = loc
            piece.id = canvas.create_image(get_loc_center((rank, file)), anchor='center', image=piece.photo_image)
            board.grid[rank][file] = piece
            piece.loc = (rank, file)
            pass
        else:
            # check if just castle, if so, move the rook to the correct position
            if piece.kind == KING:
                if loc == (7, 4):
                    if piece.loc == (7, 6):
                        board.grid[7][5] = board.grid[7][7]
                        board.grid[7][7] = None
                        canvas.delete(board.grid[7][5].id)
                        board.grid[7][5].id = canvas.create_image(get_loc_center((7, 5)), anchor='center',
                                                                  image=board.grid[7][5].photo_image)
                    if piece.loc == (7, 2):
                        board.grid[7][3] = board.grid[7][3]
                        board.grid[7][0] = None
                        canvas.delete(board.grid[7][3].id)
                        board.grid[7][3].id = canvas.create_image(get_loc_center((7, 3)), anchor='center',
                                                                  image=board.grid[7][3].photo_image)

                if loc == (0, 4):
                    if piece.loc == (0, 6):
                        board.grid[0][5] = board.grid[0][7]
                        board.grid[0][7] = None
                        canvas.delete(board.grid[0][5].id)
                        board.grid[0][5].id = canvas.create_image(get_loc_center((0, 5)), anchor='center',
                                                                  image=board.grid[0][5].photo_image)
                    if piece.loc == (0, 2):
                        board.grid[0][3] = board.grid[0][3]
                        board.grid[0][0] = None
                        canvas.delete(board.grid[0][3].id)
                        board.grid[0][3].id = canvas.create_image(get_loc_center((0, 3)), anchor='center',
                                                                  image=board.grid[0][3].photo_image)

            # change castle availability
            if piece.kind == KING:
                if piece.color == WHITE:
                    board.w_castle = [False, False]
                else:
                    board.b_castle = [False, False]
            elif piece.color == WHITE:
                if loc == (7, 0):
                    board.w_castle[1] = False
                elif loc == (7, 7):
                    board.w_castle[0] = False
            else:
                if loc == (0, 0):
                    board.b_castle[1] = False
                elif loc == (0, 7):
                    board.b_castle[0] = False

            # pawn promotion
            if piece.kind == PAWN and piece.loc[0] == 0 or piece.loc[0] == 7:
                promote_pawn(piece)
            board.change_active_color()




    else:  # move it back to the original position
        piece.id = canvas.create_image(get_loc_center(piece.loc), anchor='center',
                                       image=piece.photo_image)
        board.grid[piece.loc[0]][piece.loc[1]] = piece

def promote_pawn(pawn):
    pass

def on_press(event):
    rank, file = get_loc_on_board(event.x, event.y)
    global piece
    piece = board.grid[rank][file]
    if piece is not None and board.active_color == piece.color:
        board.grid[rank][file] = None
    else:
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
