
from PIL import Image, ImageTk

BLACK = 99
WHITE = 88

PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6


class Piece:
    def __init__(self, kind, loc, color=None):
        self.loc = loc  # (rank, file)
        if type(kind) is str:
            self.color = BLACK
            if kind == 'r':
                self.kind = ROOK
            elif kind == 'n':
                self.kind = KNIGHT
            elif kind == 'b':
                self.kind = BISHOP
            elif kind == 'q':
                self.kind = QUEEN
            elif kind == 'k':
                self.kind = KING
            elif kind == 'p':
                self.kind = PAWN
            else:
                self.color = WHITE
                if kind == 'R':
                    self.kind = ROOK
                elif kind == 'N':
                    self.kind = KNIGHT
                elif kind == 'B':
                    self.kind = BISHOP
                elif kind == 'Q':
                    self.kind = QUEEN
                elif kind == 'K':
                    self.kind = KING
                elif kind == 'P':
                    self.kind = PAWN

        else:
            self.kind = kind
            self.color = color
        image_name = "./asset/images/" + ('b' if self.color == BLACK else 'w') + "_"
        if self.kind == BISHOP:
            image_name += "bishop"
        elif self.kind == KING:
            image_name += "king"
        elif self.kind == KNIGHT:
            image_name += "knight"
        elif self.kind == PAWN:
            image_name += "pawn"
        elif self.kind == QUEEN:
            image_name += "queen"
        elif self.kind == ROOK:
            image_name += "rook"
        image_name += "_image.png"
        self.image = Image.open(image_name)
        self.image = self.image.convert('RGBA')
        self.photo_image = None
        self.id = None  # this is for the id of the picture on the canvas

    # Resize and create the photo image for the piece
    def resize_image(self, w, h):
        self.image = self.image.resize((w, h), Image.ANTIALIAS)
        self.photo_image = ImageTk.PhotoImage(self.image)

    def __str__(self):
        return "P,"
        return str(self.kind) + " " + str(self.color) + " " + str(self.loc)
