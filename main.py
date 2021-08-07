from board import *
from tkinter import Canvas, Tk
from PIL import Image, ImageTk
import time

piece = None
# constants
BOARD_LENGTH = 600
PIECE_SIZE = int(BOARD_LENGTH / 10)


# global variables are: piece, window, canvas, board


def game_end():
    # TODO
    print("check mated")
    pass


def promote_pawn(pawn):

    board.active_color = None
    rank, file = pawn.loc
    promotion_canvas = Canvas(window, width=BOARD_LENGTH / 8, height=BOARD_LENGTH / 2)
    promotion_canvas.place(relx=file / 8, rely=0 if pawn.color == WHITE else 4)
    w, h = BOARD_LENGTH / 8, BOARD_LENGTH / 2
    global promotion_choices
    promotion_choices = (Piece(KNIGHT, (w / 2, h / 8), pawn.color),
                         Piece(BISHOP, (w / 2, h / 8 * 3), pawn.color),
                         Piece(ROOK, (w / 2, h / 8 * 5), pawn.color),
                         Piece(QUEEN, (w / 2, h / 8 * 7), pawn.color))
    for p in promotion_choices:
        p.resize_image(PIECE_SIZE, PIECE_SIZE)
        p.id = promotion_canvas.create_image(p.loc, anchor='center', image=p.photo_image)
    promotion_canvas.bind('<Button-1>', lambda event, promotion_canvas = promotion_canvas, pawn=pawn: select_promotion(event, promotion_canvas,pawn))


def select_promotion(event, promotion_canvas, pawn):
    h = BOARD_LENGTH / 2
    if event.y < h / 4:
        promotion_kind = KNIGHT
    elif event.y < h / 2:
        promotion_kind = BISHOP
    elif event.y < h / 4 * 3:
        promotion_kind = ROOK
    else:
        promotion_kind = QUEEN
    print(promotion_kind)
    rank, file = pawn.loc
    promotion_canvas.destroy()
    p = Piece(promotion_kind, (rank, file), pawn.color)
    board.grid[rank][file] =p
    board.active_color = pawn.color
    board.change_active_color()
    p.resize_image(PIECE_SIZE, PIECE_SIZE)
    p.id = canvas.create_image(get_loc_center(p.loc), anchor='center', image=p.photo_image)





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


# return which block on board the mouse is current at
def get_loc_on_board(x, y):
    return int(y / BOARD_LENGTH * 8), int(x / BOARD_LENGTH * 8)  # (rank, file)


# get the center of the block the mouse is currently at
def get_loc_center(loc):
    rank, file = loc
    return file * BOARD_LENGTH / 8 + BOARD_LENGTH / 8 / 2, rank * BOARD_LENGTH / 8 + BOARD_LENGTH / 8 / 2


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

    if piece.kind == PAWN and (piece.loc[0] == 0 or piece.loc[0] == 7):
        promote_pawn(piece)

    if board.check_mate(board.active_color):
        game_end()


def main():
    global window, canvas, board
    window = Tk()
    window.title('Chess!')

    canvas = Canvas(window, width=BOARD_LENGTH, height=BOARD_LENGTH)
    canvas.pack()

    board = Board()
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
    canvas.bind('<Button-1>', on_press)
    canvas.bind('<B1-Motion>', on_hold)
    canvas.bind('<ButtonRelease-1>', on_release)
    """
    promotion_canvas = Canvas(window, width=BOARD_LENGTH / 8, height=BOARD_LENGTH / 2)
    promotion_canvas.place(relx=6 / 8, rely=3/8)
    w, h = BOARD_LENGTH / 8, BOARD_LENGTH / 2
    pp = Piece(KNIGHT, (-1, -1), WHITE)
    pp.resize_image(PIECE_SIZE, PIECE_SIZE)
    promotion_canvas.create_image((w/2,h/8), anchor ='center', image=pp.photo_image)
    """
    window.mainloop()


if __name__ == "__main__":
    main()
