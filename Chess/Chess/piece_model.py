"""
Project: Creating a working chess game with GUI
Kaleb Maulding
4/18/2023
Python Version: 3.10
"""
import copy
from enum import Enum
from abc import ABC, abstractmethod
import pygame as pg, pygame
import random

class Color(Enum):
    """Creates an enumeration used to define the colors of the pieces"""
    #Creates a White piece
    WHITE = 0
    #Creates a Black piece
    BLACK = 1

class Piece(ABC):
    """Creates an abstract class of how a chess piece acts"""
    _game = None
    SPRITESHEET = pygame.image.load("images/pieces.png")

    @staticmethod
    def set_game(game):
        """All pieces will share this, allows to query
        the current state of the board"""
        if not isinstance(game, Game):
            raise ValueError('You must provide a valid game instance.')
        Piece._game = game

    def __init__(self, color: Color):
        """Create the instance variables

        _color:
            is set equal to Color, WHITE or BLACK
        _image:
            holds the image for each piece
        """
        self._color = color
        self._image = pygame.Surface((105, 105), pg.SRCALPHA)
        #Piece.SPRITESHEET = pygame.image.load("images/pieces.png")

    @property
    def color(self) -> Color:
        """returns an instance of _color"""
        return self._color

    def set_image(self, x: int, y: int) -> None:
        """takes an x and y value and copies image file to
        a 105x105 pixel chunk into the pieces image"""
        self._image.blit(Piece.SPRITESHEET, (0, 0), pygame.rect.Rect(x, y, 105, 105))

    def _diagonal_moves(self, y: int, x: int, y_d: int, x_d: int, distance: int) -> list[tuple[int, int]]:
        """Creates all the possible diagonal moves a piece can make

        Parameters:
        ----------
        y:
            The y coordinate of the current piece.
        x:
            The x coordinate of the current piece.
        y_d:
            The direction vector vertically (-1 up 1 down).
        x_d:
            the direction vector horizontally (-1 left 1 right).
        distance:
            How many spaces the moves are calculated for.
        """
        moves = []
        bad_moves = []
        for i in range(1, distance + 1):
            new_y = y + i * y_d
            new_x = x + i * x_d
            if 0 <= new_y <= 7 and 0 <= new_x <= 7:
                if self._game.board[new_y][new_x] is not None:
                    if self._game.board[new_y][new_x].color != self._color:
                        moves.append((new_y, new_x))
                        break
                    if self._game.board[new_y][new_x].color == self._color:
                        bad_moves.append((new_y, new_x))
                        break
                else:
                    moves.append((new_y, new_x))
            else:
                bad_moves.append((new_y, new_x))
        return moves

    def _horizontal_moves(self, y: int, x: int, y_d: int, x_d: int, distance: int) -> list[tuple[int, int]]:
        """Creates all the possible horizontal moves a piece can make.

        Parameters:
        ----------
        Parameters:
        ----------
        y:
            The y coordinate of the current piece.
        x:
            The x coordinate of the current piece.
        y_d:
            The direction vector vertically (-1 up 1 down).
        x_d:
            the direction vector horizontally (-1 left 1 right).
        distance:
            How many spaces the moves are calculated for.
        """
        moves = []
        bad_moves = []
        for i in range(1, distance + 1):
            new_y = y + i * y_d
            new_x = x + i * x_d
            if 0 <= new_y <= 7 and 0 <= new_x <= 7:
                if self._game.board[new_y][new_x] is not None:
                    if self._game.board[new_y][new_x].color != self._color:
                        moves.append((new_y, new_x))
                        break
                    if self._game.board[new_y][new_x].color == self.color:
                        bad_moves.append((new_y, new_x))
                        break
                else:
                    moves.append((new_y, new_x))
            else:
                bad_moves.append((new_y, new_x))
        return moves

    def _vertical_moves(self, y: int, x: int, y_d: int, x_d: int, distance: int) -> list[tuple[int, int]]:
        """Creates all the possible horizontal moves a piece can make.

        Parameters:
        ----------
        Parameters:
        ----------
        y:
            The y coordinate of the current piece.
        x:
            The x coordinate of the current piece.
        y_d:
            The direction vector vertically (-1 up 1 down).
        x_d:
            the direction vector horizontally (-1 left 1 right).
        distance:
            How many spaces the moves are calculated for.
        """
        moves = []
        bad_moves = []
        for i in range(1, distance + 1):
            new_y = y + i * y_d
            new_x = x + i * x_d
            if 0 <= new_y <= 7 and 0 <= new_x <= 7:
                if self._game.board[new_y][new_x] is not None:
                    if self._game.board[new_y][new_x].color != self._color:
                        moves.append((new_y, new_x))
                        break
                    else:
                        bad_moves.append((new_y, new_x))
                        break
                else:
                    moves.append((new_y, new_x))
            else:
                bad_moves.append((new_y, new_x))
        return moves

    def get_diagonal_moves(self, y: int, x: int, distance: int) -> list[tuple[int, int]]:
        """returns all possible diagonal moves a piece can make"""
        #list of all diagonal moves
        moves = []
        #all possible diagonal moves
        moves += self._diagonal_moves(y, x, -1, -1, distance)
        moves += self._diagonal_moves(y, x, 1, -1, distance)
        moves += self._diagonal_moves(y, x, -1, 1, distance)
        moves += self._diagonal_moves(y, x, 1, 1, distance)
        #return moves list
        return moves

    def get_horizontal_moves(self, y: int, x: int, distance: int) -> list[tuple[int, int]]:
        """returns all possible horizontal moves a piece can make"""
        #list of all possible horizontal moves
        moves = []
        #all possible horizontal moves
        moves += self._horizontal_moves(y, x, 0, -1, distance)
        moves += self._horizontal_moves(y, x, 0, 1, distance)
        #return moves list
        return moves

    def get_vertical_moves(self, y: int, x: int, distance: int) -> list[tuple[int, int]]:
        """returns all possible vertical moves a piece can make"""
        #list of all vertical moves
        moves = []
        #all possible vertical moves
        moves += self._vertical_moves(y, x, -1, 0, distance)
        moves += self._vertical_moves(y, x, 1, 0, distance)
        #returns moves list
        return moves

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        pass

    def copy(self):
        pass

class King(Piece):
    """inherits from the Piece class, defines all moves
    a King is able to make"""
    def __init__(self, color: Color):
        """sets the image of a piece depending on its color"""
        super().__init__(color)
        #sets the image based on color
        if color == Color.WHITE:
            self.set_image(0, 0)
        else:
            self.set_image(0, 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """lists all valid moves for the King"""
        moves = []
        moves += self.get_diagonal_moves(y, x, 1)
        moves += self.get_horizontal_moves(y, x, 1)
        moves += self.get_vertical_moves(y, x, 1)
        return moves

    def copy(self):
        """returns a new King of the same color"""
        new_king = King(self.color)
        return new_king

class Queen(Piece):
    """inherits from the Piece class, defines all moves
    a Queen is able to make"""
    def __init__(self, color: Color):
        """sets the image of a piece depending on its color"""
        super().__init__(color)
        #sets the image based on color
        if color == Color.WHITE:
            self.set_image(105, 0)
        else:
            self.set_image(105, 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """lists all valid moves for the Queen"""
        moves = []
        moves += self.get_diagonal_moves(y, x, 7)
        moves += self.get_horizontal_moves(y, x, 7)
        moves += self.get_vertical_moves(y, x, 7)
        return moves

    def copy(self):
        """returns a new Queen of the same color"""
        new_queen = Queen(self.color)
        return new_queen

class Bishop(Piece):
    """inherits from the Piece class, defines all moves
    a Bishop is able to make"""
    def __init__(self, color: Color):
        """sets the image of a piece depending on its color"""
        super().__init__(color)
        #sets the image based on color
        if color == Color.WHITE:
            self.set_image(210, 0)
        else:
            self.set_image(210, 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """lists all valid moves for the Bishop"""
        moves = []
        moves += self.get_diagonal_moves(y, x, 7)
        return moves

    def copy(self):
        """returns a new Bishop of the same color"""
        new_bishop = Bishop(self.color)
        return new_bishop

class Knight(Piece):
    """inherits from the Piece class, defines all moves
    a Knight is able to make"""
    def __init__(self, color: Color):
        """sets the image of a piece depending on its color"""
        super().__init__(color)
        #sets the image based on color
        if color == Color.WHITE:
            self.set_image(315, 0)
        else:
            self.set_image(315, 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """lists all valid moves for the Knight"""
        #list of moves
        moves = []
        bad_moves = []
        #a list of all possible move formations
        l_shape_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                         (1, -2), (1, 2), (2, -1), (2, 1)]
        #looking in each move formation
        for move in l_shape_moves:
            #move piece to new y coordinate
            new_y = y + move[0]
            #move piece to new x coordinate
            new_x = x + move[1]
            #if piece out of bounds break
            if new_y < 0 or new_y > 7 or new_x < 0 or new_x > 7:
                continue
            #if piece in new coordinate is same color remove location from l_shape_moves
            if self._game.board[new_y][new_x] is not None and self._game.board[new_y][new_x].color == self._color:
                bad_moves.append((new_y, new_x))
            moves.append((new_y, new_x))

        valid_moves = [move for move in moves if move not in bad_moves]
        return valid_moves

    def copy(self):
        """returns a new Knight of the same color"""
        new_knight = Knight(self.color)
        return new_knight

class Rook(Piece):
    """inherits from the Piece class, defines all moves
    a Rook is able to make"""
    def __init__(self, color: Color):
        """sets the image of a piece depending on its color"""
        super().__init__(color)
        if color == Color.WHITE:
            self.set_image(420, 0)
        else:
            self.set_image(420, 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """lists all valid moves for the Rook"""
        moves = []
        moves += self.get_horizontal_moves(y, x, 8)
        moves += self.get_vertical_moves(y, x, 7)
        return moves

    def copy(self):
        """returns a new Rook of the same color"""
        new_rook = Rook(self.color)
        return new_rook

class Pawn(Piece):
    """inherits from the Piece class, defines all moves
    a Pawn is able to make"""
    def __init__(self, color: Color):
        """sets the image of a piece depending on its color"""
        super().__init__(color)
        #sets the image based on color
        if color == Color.WHITE:
            self.set_image(525, 0)
        else:
            self.set_image(525, 105)
        self.moved = False

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """lists all valid moves for the Pawn"""
        moves = []
        if self.color == Color.WHITE:
            if y == 1:
                if self._game.board[y+1][x] is None and self._game.board[y+2][x] is None:
                    moves.append((y+2, x))
            if self._game.board[y+1][x] is None:
                moves.append((y+1, x))
            if x > 0 and self._game.board[y+1][x-1] is not None and self._game.board[y+1][x-1].color != self.color:
                moves.append((y+1, x-1))
            if x < 7 and self._game.board[y+1][x+1] is not None and self._game.board[y+1][x+1].color != self.color:
                moves.append((y+1, x+1))
        else:
            if y == 6:
                if self._game.board[y-1][x] is None and self._game.board[y-2][x] is None:
                    moves.append((y-2, x))
            if self._game.board[y-1][x] is None:
                moves.append((y-1, x))
            if x > 0 and self._game.board[y-1][x-1] is not None and self._game.board[y-1][x-1].color != self.color:
                moves.append((y-1, x-1))
            if x < 7 and self._game.board[y-1][x+1] is not None and self._game.board[y-1][x+1].color != self.color:
                moves.append((y-1, x+1))
        return moves

    def copy(self):
        """returns a new Pawn of the same color"""
        new_pawn = Pawn(self.color)
        new_pawn.moved = True
        return new_pawn

class Game:
    def __init__(self):
        """Creates the instance variables

        board:
            Creates the chess board.
        current_player:
            keeps track of which players turn it is.
        prior_state:
            keeps a copy of the prior state of the board.
        """
        self.current_player = Color.WHITE
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.prior_state = []
        Piece.set_game(self)
        self._setup_pieces()

    def reset(self):
        """resets the board back to the default state"""
        #sets the current player
        self.current_player = Color.WHITE
        #initializes the board
        self.board = [[None for _ in range(8)] for _ in range(8)]
        #creates an empty list for prior states
        self.prior_state = []
        #sets up the pieces
        self._setup_pieces()

    def _setup_pieces(self):
        """sets up all pieces in their default positions
        on the board
        """
        #initializes the board
        self.board = [[None for _ in range(8)] for _ in range(8)]
        #Creating a full row of pawns simultaneously
        for c in range(8):
            #White Pawns
            self.board[1][c] = Pawn(Color.WHITE)
            #Black Pawns
            self.board[6][c] = Pawn(Color.BLACK)

        #White Rooks
        self.board[0][0] = Rook(Color.WHITE)
        print(self.board[0][0])
        self.board[0][7] = Rook(Color.WHITE)
        print(self.board[0][7])
        #Black Rooks
        self.board[7][0] = Rook(Color.BLACK)
        self.board[7][7] = Rook(Color.BLACK)

        #White Knights
        self.board[0][1] = Knight(Color.WHITE)
        self.board[0][6] = Knight(Color.WHITE)
        #Black Knights
        self.board[7][1] = Knight(Color.BLACK)
        self.board[7][6] = Knight(Color.BLACK)

        #White Bishops
        self.board[0][2] = Bishop(Color.WHITE)
        self.board[0][5] = Bishop(Color.WHITE)
        #Black Bishops
        self.board[7][2] = Bishop(Color.BLACK)
        self.board[7][5] = Bishop(Color.BLACK)

        #White Queen
        self.board[0][3] = Queen(Color.WHITE)
        #Black Queen
        self.board[7][3] = Queen(Color.BLACK)

        #White King
        self.board[0][4] = King(Color.WHITE)
        #Black King
        self.board[7][4] = King(Color.BLACK)

    def get(self, y: int, x: int):
        """returns the pieces to their spots, returns None
        if no piece in spot"""
        if y < 0 or y > 7 or x < 0 or x > 7:
            return None
        return self.board[y][x]

    def switch_player(self):
        """switches players after each turn"""
        #if player is white switch player to black
        if self.current_player == Color.WHITE:
            return self.current_player == Color.BLACK
        #if player is black switch player to white
        else:
            return self.current_player == Color.WHITE

    def undo(self):
        """if there is a prior board, reverts to it by using pop"""
        if len(self.prior_state) == 0:
            return False
        self.board = self.prior_state.pop()
        return True

    def copy_board(self):
        """copies the entire current game board"""
        new_board = [[None for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None:
                    new_board[i][j] = self.board[i][j].copy()
        return new_board

    def move(self, piece: Piece, y: int, x: int, y2: int, x2: int) -> bool:
        """moves the pieces on the board"""
        #copies the current state of the board
        self.prior_state.append(self.copy_board())

        self.board[y][x] = None
        self.board[y2][x2] = piece

        if isinstance(piece, Pawn):
            piece.moved = True

        if self.check(self.current_player):
            self.board = self.prior_state.pop()
            return False

        if isinstance(piece, Pawn) and (y2 == 0 or y2 == 7):
            self.board[y2][x2] = Queen(piece.color)

        self.current_player = Color.WHITE if self.current_player == Color.BLACK else Color.BLACK
        return True

    def get_piece_locations(self, color: Color) -> list[tuple[int, int]]:
        """returns the location of all pieces on the board"""
        #list of locations
        locations = []
        for y in range(8):
            for x in range(8):
                if self.get(y, x) is not None and self.get(y, x).color == color:
                    locations.append((y, x))
        return locations

    def find_king(self, color: Color) -> tuple[int, int]:
        """finds the exact location of the king based on color"""
        for y in range(8):
            for x in range(8):
                #sets piece equal to a location
                piece = self.get(y, x)
                #if the piece is a king, return the location
                if isinstance(piece, King) and piece.color == color:
                    return (y, x)

    def check(self, color: Color) -> bool:
        """checks if a player has been put in check"""
        opposite_color = Color.WHITE if color == Color.BLACK else Color.BLACK
        locations = self.get_piece_locations(opposite_color)
        king_location = self.find_king(color)
        for loc in locations:
            piece = self.get(loc[0], loc[1])
            if piece and piece.color == opposite_color:
                if king_location in piece.valid_moves(loc[0], loc[1]):
                    return True
        return False

    def mate(self, color: Color) -> bool:
        """checks if a player is in check mate"""
        if not self.check(color):
            return False

        opposite_color = Color.WHITE if color == Color.BLACK else Color.BLACK
        enemy_pieces = self.get_piece_locations(opposite_color)
        friendly_pieces = self.get_piece_locations(color)
        king = self.find_king(color)

        for loc in enemy_pieces:
            enemy = self.get(loc[0], loc[1])
            if enemy and enemy.color == opposite_color:
                if king not in enemy.valid_moves(loc[0], loc[1]):
                    return False

        for move in friendly_pieces:
            piece, y, x, y2, x2 = move
            captured_piece = self.board[y2][x2]
            self.move(piece, y, x, y2, x2)
            in_check = self.check(color)
            self.undo(captured_piece)

            if not in_check:
                return False

        return True

    def _computer_move(self, color):
        """Selects a random valid move for the computer player"""
        rules = {
            'checkmate': self._checkmate,
            'check': self._check,
            'capture_queen': self._capture_queen,
            'capture_bishop': self._capture_bishop,
            'capture_knight': self._capture_knight,
            'capture_rook': self._capture_rook,
            'capture_pawn': self._capture_pawn,
            'random': self._random_move
        }
