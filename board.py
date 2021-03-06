from pieces import *
import itertools
from copy import deepcopy


class Board:
    def __init__(self, fen=None):
        # initialize an empty board
        self.grid = [[None for x in range(8)] for y in range(8)]  # DON'T do [[None]*8]*8 its SHALLOW COPY!
        # load the board from FEN
        # https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
        if fen is None:
            with open("./asset/starting_position.fen", 'r') as f:
                fen = f.read()
        try:
            placement, self.active_color, self.castle, en_passant, self.half_move_clock, self.full_move_clock = tuple(
                fen.split(" "))
        except:
            raise Exception("Invalid fen")

        self.w_castle = ['K' in self.castle, 'Q' in self.castle]
        self.b_castle = ['K' in self.castle, 'Q' in self.castle]

        if self.active_color == 'w':
            self.active_color = WHITE
        elif self.active_color == 'b':
            self.active_color = BLACK
        else:
            raise Exception("Invalid active color in fen")

        if en_passant == '-':
            self.en_passant = None
        else:
            self.en_passant = [0, 0]
            self.en_passant[0] = en_passant[1]
            self.en_passant[1] = ord(en_passant[0])

        self.moves = []  # the moves players made (piece, orignial position, new position, piece taken)
        # convert the placement string to 8x8 grid
        for rank, line in enumerate(placement.split("/")):
            file = 0
            for c in line:
                if c in ['r', 'n', 'b', 'q', 'p', 'k', 'R', 'N', 'B', 'Q', 'K', 'P']:
                    self.grid[rank][file] = Piece(c, (rank, file))
                    if c == 'K':
                        self.white_king = self.grid[rank][file]
                    if c == 'k':
                        self.black_king = self.grid[rank][file]
                    file += 1

                # number of space
                else:
                    file += int(c)

    # check if a given color and position is in check
    def in_check(self, color):
        piece = self.white_king if color == WHITE else self.black_king
        return self.attacked(color, piece.loc)

    # see if a piece at loc is attacked or not
    def attacked(self, color, loc):
        for rank in self.grid:
            for p in rank:
                if p is not None and p.color != color and loc in self.get_legal_moves(p):
                    return True

        return False

    # str representation of the board in string
    def __str__(self):
        s = ''
        for rank in self.grid:
            s += '|'
            for b in rank:
                if b == None:
                    s += " "
                else:
                    s += str(b)
                s += '|'
            s += '\n'
        return s

    # change the active color from black to white or white to black
    def change_active_color(self):
        self.active_color = BLACK if self.active_color == WHITE else WHITE

    # for a given piece and its future position, determine if it is a legal move
    def is_legal_move(self, piece, move):
        return move in self.get_legal_moves(piece)

    # generate all possibles moves
    def get_legal_moves(self, piece):
        if piece is None:
            return []
        moves = []
        rank, file = piece.loc
        if piece.kind == PAWN:
            if piece.color == WHITE:
                if self.grid[rank - 1][file] is None:
                    moves.append((rank - 1, file))
                    if rank == 6 and self.grid[rank - 2][file] is None:
                        moves.append((rank - 2, file))
                # check for capture
                if file - 1 >= 0 and (self.grid[rank - 1][file - 1] is not None and self.grid[rank - 1][
                    file - 1].color != piece.color) or (rank - 1, file - 1) == self.en_passant:
                    moves.append((rank - 1, file - 1))
                if file + 1 < 8 and (self.grid[rank - 1][file + 1] is not None and self.grid[rank - 1][
                    file + 1].color != piece.color) or (rank - 1, file + 1) == self.en_passant:
                    moves.append((rank - 1, file + 1))
            else:
                if self.grid[rank + 1][file] is None:
                    moves.append((rank + 1, file))
                    if rank == 1 and self.grid[rank + 2][file] is None:
                        moves.append((rank + 2, file))
                # check captures
                if file - 1 >= 0 and (self.grid[rank + 1][file - 1] is not None and self.grid[rank + 1][
                    file - 1].color != piece.color) or (rank + 1, file - 1) == self.en_passant:
                    moves.append((rank + 1, file - 1))
                if file + 1 < 8 and (self.grid[rank + 1][file + 1] is not None and self.grid[rank + 1][
                    file + 1].color != piece.color) or (rank + 1, file + 1) == self.en_passant:
                    moves.append((rank + 1, file + 1))

        elif piece.kind == KNIGHT:
            moves = [(r, f) for r, f in
                     [(rank + 2, file + 1), (rank + 2, file - 1), (rank - 2, file + 1), (rank - 2, file - 1),
                      (rank - 1, file + 2), (rank + 1, file + 2), (rank - 1, file - 2), (rank + 1, file - 2)]
                     if
                     (8 > r >= 0 and 8 > f >= 0) and (self.grid[r][f] is None or self.grid[r][f].color != piece.color)]
        elif piece.kind == KING:
            for r, f in itertools.chain(itertools.permutations(range(-1, 2), 2), ((1, 1), (-1, -1))):
                if 0 <= rank + r < 8 and 0 <= file + f < 8:
                    if self.grid[rank + r][file + f] is None or self.grid[rank + r][file + f].color != piece.color:
                        moves.append((rank + r, file + f))

            if piece.color == WHITE:
                if self.w_castle[0]:  # if king side castle is available:
                    if self.grid[7][5] is None and self.grid[7][6] is None and not self.in_check(
                            WHITE) and not self.attacked(WHITE, (7, 5)) and not self.attacked(WHITE, (7, 6)):
                        moves.append((7, 6))


        else:  # pieces that can move in a ray like fashion
            if piece.kind == ROOK:
                iterator = ((1, 0), (-1, 0), (0, 1), (0, -1))
            if piece.kind == BISHOP:
                iterator = ((1, 1), (-1, -1), (1, -1), (-1, 1))
            if piece.kind == QUEEN:
                iterator = itertools.chain(itertools.permutations(range(-1, 2), 2), [(1, 1), (-1, -1)])
            for r, f in iterator:
                for i in range(1, 8):
                    if rank + i * r < 0 or rank + i * r > 7 or file + i * f < 0 or file + i * f > 7:
                        break
                    if self.grid[rank + i * r][file + i * f] is None:
                        moves.append((rank + i * r, file + i * f))
                    elif self.grid[rank + i * r][file + i * f].color != piece.color:
                        moves.append((rank + i * r, file + i * f))
                        break
                    else:
                        break

        return moves

    # check if it is a check mate
    def is_check_mate(self, color):
        if not self.in_check(color):
            return False
        for rank in self.grid:
            for p in rank:
                if p is not None and p.color == color:

                    moves = self.get_legal_moves(p)
                    for move in moves:
                        piece_at_move = self.grid[move[0]][move[1]]
                        loc = p.loc
                        self.grid[move[0]][move[1]] = p
                        p.loc = move
                        self.grid[loc[0]][loc[1]] = None
                        if not self.in_check(color):
                            p.loc = loc
                            self.grid[move[0]][move[1]] = piece_at_move
                            self.grid[p.loc[0]][p.loc[1]] = p
                            return False
                        self.grid[move[0]][move[1]] = piece_at_move
                        p.loc = loc
                        self.grid[p.loc[0]][p.loc[1]] = p
        return True

    # move a piece to a given location if that move is legal
    def move(self, piece, loc):
        rank, file = loc
        pieces_moved = [piece]
        if self.is_legal_move(piece, loc):  # if it is a legal move
            move = [piece, piece.loc, loc, self.grid[loc[0]][loc[1]], False]
            # check if the move was en passant
            original_loc = piece.loc
            if piece.kind == PAWN and (rank, file) == self.en_passant:
                if piece.color == WHITE:
                    move[3] = self.grid[rank + 1][file]
                    move[4] = True
                    pieces_moved.append(self.grid[rank + 1][file])
                    self.grid[rank + 1][file].loc = None
                    self.grid[rank + 1][file] = None
                else:  # if black
                    pieces_moved.append(self.grid[rank - 1][file])
                    move[3] = self.grid[rank - 1][file]
                    self.grid[rank - 1][file].loc = None
                    self.grid[rank - 1][file] = None
            # check if the move would create possibility for en passant
            self.en_passant = None
            if piece.kind == PAWN:
                if piece.loc[0] == 1 and rank == 3:
                    self.en_passant = (2, file)
                elif piece.loc[0] == 6 and rank == 4:
                    self.en_passant = (5, file)
            piece_taken = self.grid[rank][file]
            self.grid[rank][file] = piece
            self.grid[original_loc[0]][original_loc[1]] = None

            piece.loc = (rank, file)
            if self.in_check(piece.color):
                self.grid[rank][file] = piece_taken
                if piece_taken is not None:
                    pieces_moved.append(piece_taken)
                rank, file = original_loc
                self.grid[rank][file] = piece
                piece.loc = (rank, file)
            else:
                # check if just castle, if so, move the rook to the correct position
                if piece.kind == KING:
                    if original_loc == (7, 4):
                        if piece.loc == (7, 6):
                            pieces_moved.append(self.grid[7][7])
                            self.grid[7][5] = self.grid[7][7]
                            self.grid[7][7] = None
                            self[(7,5)].loc = (7,5)

                        if piece.loc == (7, 2):
                            pieces_moved.append(self.grid[7][0])
                            self.grid[7][3] = self.grid[7][3]
                            self.grid[7][0] = None
                            self[(7,3)].loc = (7,3)

                    if original_loc == (0, 4):
                        if piece.loc == (0, 6):
                            pieces_moved.append(self.grid[0][7])
                            self.grid[0][5] = self.grid[0][7]
                            self.grid[0][7] = None
                            self[(0,5)].loc = (0,5)
                        if piece.loc == (0, 2):
                            pieces_moved.append(self.grid[0][0])
                            self.grid[0][3] = self.grid[0][0]
                            self[(0,3)].loc = (0,3)
                            self.grid[0][0] = None

                # change castle availability
                if piece.kind == KING:
                    if piece.color == WHITE:
                        self.w_castle = [False, False]
                    else:
                        self.b_castle = [False, False]
                elif piece.color == WHITE:
                    if original_loc == (7, 0):
                        self.w_castle[1] = False
                    elif original_loc == (7, 7):
                        self.w_castle[0] = False
                else:
                    if original_loc == (0, 0):
                        self.b_castle[1] = False
                    elif original_loc == (0, 7):
                        self.b_castle[0] = False

                self.change_active_color()
            self.moves.append(tuple(move))  # update the move list
        return pieces_moved

    # promote the pawn to the given kind
    def promote_pawn(self, pawn, kind):
        self.grid[pawn.loc[0]][pawn.loc[1]] = Piece(kind, pawn.loc)
        return self.grid[pawn.loc[0]][pawn.loc[1]]

    # return the perft result for a given depth (for ddebugging
    def perft(self, depth):
        if depth == 0:
            return 1
        nodes = 0
        for rank in self.grid:
            for p in rank:
                if p is not None and p.color == self.active_color:
                    legal_moves = self.get_legal_moves(p)
                    for move in legal_moves:
                        new_board = deepcopy(self)
                        new_board.move(p, move)
                        nodes += new_board.perft(depth - 1)

        return nodes

    # generate the fen representation of the board
    def get_fen(self):
        fen = ""
        for rank in self.grid:
            empty = 0
            for loc in rank:
                if loc is None:
                    empty += 1
                else:
                    if empty != 0:
                        fen += str(empty)
                        empty = 0
                    fen += str(loc)
            if empty != 0:
                fen += str(empty)
            fen += '/'
        fen += ' '
        if self.active_color == WHITE:
            fen += 'w'
        else:
            fen += 'b'
        fen += ' '
        if self.w_castle[0]:
            fen += 'K'
        if self.w_castle[1]:
            fen += 'Q'
        if self.b_castle[0]:
            fen += 'k'
        if self.b_castle[1]:
            fen += 'q'
        fen += ' '
        if self.en_passant is None:
            fen += '-'
        else:
            fen += chr(self.en_passant[1] + ord('a')) + str(self.en_passant[2])

        fen += ' '
        fen += self.half_move_clock
        fen += ' '
        fen += self.full_move_clock
        return fen

    def unmove(self):
        if len(self.moves) == 0:
            return
        piece, original_loc, new_loc, piece_taken, en_passant = self.moves[-1]
        self.moves.pop(-1)
        piece.loc = original_loc

        if en_passant:
            rank, file = new_loc
            if piece_taken.color == WHITE:
                rank = 6
                piece_taken= (rank, file)
                self[(rank, file)] = piece_taken
            else:
                rank = 1
                piece_taken.loc = (rank, file)
                self[(rank, file)] = piece_taken
        else:
            # last move was a castle move
            if piece.kind == KING and abs(original_loc[1] - new_loc[1]) > 1:
                if new_loc == (0, 6):
                    self[(0,7)] = self[(0,5)]
                    self[(0,5)] = None
                    self[(0,7)].loc = (0,7)
                if new_loc == (0,2):
                    self[(0, 0)] = self[(0, 3)]
                    self[(0,3)] = None
                    self[(0,0)].loc = (0,0)
                if new_loc == (7, 6):
                    self[(7,7)] = self[(7,5)]
                    self[(7,5)] = None
                    self[(7,7)].loc = (7,7)
                if new_loc == (0,2):
                    self[(7, 0)] = self[(7, 3)]
                    self[(7,3)] = None
                    self[(7,0)].loc = (7,0)
            if piece_taken is not None:
                piece_taken.loc = new_loc
            self[original_loc] = piece
            self[new_loc] = piece_taken

        self.change_active_color()

    def __getitem__(self, loc):
        return self.grid[loc[0]][loc[1]]

    def __setitem__(self, loc, piece):
        self.grid[loc[0]][loc[1]] = piece


# test
if __name__ == "__main__":
    print(Board().perft(2))
