from board import *
from tkinter import Canvas, Tk, Frame, Label, Entry, Button


class game():
    def __init__(self, fen=None):
        self.piece = None
        self.BOARD_LENGTH = 600
        self.PIECE_SIZE = int(self.BOARD_LENGTH / 10)

        self.window = Tk()
        self.window.title('Chess!')

        self.canvas = Canvas(self.window, width=self.BOARD_LENGTH, height=self.BOARD_LENGTH)
        self.canvas.pack(side='left')
        self.highlight = []
        self.board = Board(fen)

        self.draw_board()
        self.create_user_interface()
        self.canvas.bind('<Button-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_hold)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.window.mainloop()

    def create_user_interface(self):
        # user interface
        self.frame = Frame(self.window, width=self.BOARD_LENGTH / 2, height=self.BOARD_LENGTH)
        self.frame.pack(side='right')
        self.fen_input_entry = Entry(self.frame)
        self.fen_input_entry.grid(row=1)
        self.fen_input_label = Label(self.frame, text="Input fen here").grid(row=0)
        self.fen_input_button = Button(self.frame, text="Enter", command=self.board_from_fen).grid(row=3)

    # load a new board from the given fen. fen is stored in self.fren
    def board_from_fen(self):
        try:
            self.board = Board(self.fen_input_entry.get())
        except:
            print("Invalid fen")
        self.draw_board()

    # draw the chess board with pieces from self.board
    def draw_board(self):
        # draw the lines
        color = "green"
        for i in range(9):
            for j in range(9):

                self.canvas.create_rectangle(i * self.BOARD_LENGTH / 8, j * self.BOARD_LENGTH / 8,
                                             i * self.BOARD_LENGTH / 8 + self.BOARD_LENGTH / 8,
                                             j * self.BOARD_LENGTH / 8 + self.BOARD_LENGTH / 8, fill=color)
                if color == "white":
                    color = "green"
                else:
                    color = "white"

        for rank in self.board.grid:
            for block in rank:
                if block is not None:
                    block.resize_image(self.PIECE_SIZE, self.PIECE_SIZE)
                    block.id = self.canvas.create_image(self.get_loc_center(block.loc), anchor='center',
                                                        image=block.photo_image)

    # what to do when game end!
    def game_end(self):
        self.board.active_color = None
        # TODO
        print("check mated")
        pass

    # The gui for promoting pawn. Also calls the Board.promote pawn with user's selection
    def promote_pawn(self, pawn):
        self.board.active_color = None
        rank, file = pawn.loc
        promotion_canvas = Canvas(self.window, width=self.BOARD_LENGTH / 8, height=self.BOARD_LENGTH / 2)
        promotion_canvas.place(relx=file / 8, rely=0 if pawn.color == WHITE else 4)
        w, h = self.BOARD_LENGTH / 8, self.BOARD_LENGTH / 2
        self.promotion_choices = (Piece(KNIGHT, (w / 2, h / 8), pawn.color),
                                  Piece(BISHOP, (w / 2, h / 8 * 3), pawn.color),
                                  Piece(ROOK, (w / 2, h / 8 * 5), pawn.color),
                                  Piece(QUEEN, (w / 2, h / 8 * 7), pawn.color))
        for p in self.promotion_choices:
            p.resize_image(self.PIECE_SIZE, self.PIECE_SIZE)
            p.id = promotion_canvas.create_image(p.loc, anchor='center', image=p.photo_image)
        promotion_canvas.bind('<Button-1>',
                              lambda event, promotion_canvas=promotion_canvas, pawn=pawn: self.select_promotion(event,
                                                                                                                promotion_canvas,
                                                                                                                pawn))

    # The GUI for pawn promotion selection
    def select_promotion(self, event, promotion_canvas, pawn):
        h = self.BOARD_LENGTH / 2
        if event.y < h / 4:
            promotion_kind = KNIGHT
        elif event.y < h / 2:
            promotion_kind = BISHOP
        elif event.y < h / 4 * 3:
            promotion_kind = ROOK
        else:
            promotion_kind = QUEEN
        rank, file = pawn.loc
        promotion_canvas.destroy()
        p = Piece(promotion_kind, (rank, file), pawn.color)
        self.board.grid[rank][file] = p
        self.board.active_color = pawn.color
        self.board.change_active_color()
        p.resize_image(self.PIECE_SIZE, self.PIECE_SIZE)
        p.id = self.canvas.create_image(self.get_loc_center(p.loc), anchor='center', image=p.photo_image)

    # if pressing on a piece with the correct color, set self.piece to that piece. Else self.piece is None
    def on_press(self, event):
        rank, file = self.get_mouse_loc_on_board(event.x, event.y)
        self.piece = self.board.grid[rank][file]
        if self.piece is not None:
            if self.board.active_color != self.piece.color:
                self.piece = None
            else:
                # show the available moves
                moves = self.board.get_legal_moves(self.piece)
                for move in moves:
                    self.highlight_square(self.get_loc_center(move))

    # highlight the given square
    def highlight_square(self, loc):
        self.highlight.append(
            self.canvas.create_rectangle(loc[0] - self.BOARD_LENGTH / 16, loc[1] - self.BOARD_LENGTH / 16,
                                         loc[0] + self.BOARD_LENGTH / 16, loc[1] + self.BOARD_LENGTH / 16, fill="black",
                                         stipple="gray50"))

    # if there is a piece to be stick to the mouse, call the self. stick_piece_on_cursor
    def on_hold(self, event):
        if self.piece is not None:
            self.stick_piece_on_cursor(event)

    # If it is a valid move, move the piece. Otherwise put the piece back to the original position
    def on_release(self, event):
        if self.piece is not None:
            self.move(self.piece, self.get_mouse_loc_on_board(event.x, event.y))
        self.piece = None
        for h in self.highlight:
            self.canvas.delete(h)
        self.highlight = []

    # return which block on board the mouse is current at
    def get_mouse_loc_on_board(self, x, y):
        return int(y / self.BOARD_LENGTH * 8), int(x / self.BOARD_LENGTH * 8)  # (rank, file)

    # get the center of the block the mouse is currently at
    def get_loc_center(self, loc):
        rank, file = loc
        return file * self.BOARD_LENGTH / 8 + self.BOARD_LENGTH / 8 / 2, rank * self.BOARD_LENGTH / 8 + self.BOARD_LENGTH / 8 / 2

    # Make the given piece stick on the cursor
    def stick_piece_on_cursor(self, event):
        self.canvas.delete(self.piece.id)
        self.piece.id = self.canvas.create_image((event.x - self.PIECE_SIZE / 2, event.y - self.PIECE_SIZE / 2),
                                                 anchor='nw',
                                                 image=self.piece.photo_image)

    # The gui for moving a piece. Also calls the self.Board.move function
    def move(self, piece, loc):
        self.canvas.delete(piece.id)
        pieces = self.board.move(piece, loc)
        for p in pieces:
            self.canvas.delete(p.id)
            p.id = self.canvas.create_image(self.get_loc_center(p.loc), anchor='center', image=p.photo_image)

        if piece.kind == PAWN and (piece.loc[0] == 0 or piece.loc[0] == 7):
            self.promote_pawn(piece)

        if self.board.is_check_mate(self.board.active_color):
            self.game_end()


if __name__ == "__main__":
    game()
