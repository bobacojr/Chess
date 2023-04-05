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
    #Keeps track of current game
    _game = None
    #The image path for the pieces
    #SPRITESHEET = None
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
        #list of all valid moves
        moves = []
        #checks the range of i from 1 to maximum distance
        for i in range(1, distance + 1):
            #multiplies index by the distance traveled plus coordinate to get diagonal
            new_y = y + i * y_d
            new_x = x + i * x_d
            if new_y < 0 or new_y > 7 or new_x < 0 or new_x > 7:
                break
            elif self._game.board[new_y][new_x] is None:
                moves.append((new_y, new_x))
            elif self._game.board[new_y][new_x].color != self._color:
                moves.append((new_y, new_x))
                break
            elif self._game.board[new_y][new_x].color is not None and self._game.board[new_y][new_x].color == self.color:
                break
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
        #list of all valid moves
        moves = []
        #checks the range of i from 1 to max distance
        for i in range(1, distance + 1):
            #the y does not change for horizontal
            new_y = y
            #current coordinate plus index multiplied by distance moved
            new_x = x + i * x_d
            #if x is out of bounds break
            if new_x < 0 or new_x > 7:
                break
            #if location is None add to moves list
            elif self._game.board[new_y][new_x] is None:
                moves.append((new_y, new_x))
            #if location has an opposite color piece add to moves list
            elif self._game.board[new_y][new_x].color != self._color:
                moves.append((new_y, new_x))
                #break because you cannot jump over a piece
                break
            #anything else break
            else:
                break
        #return the moves list
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
        #list of valid moves
        moves = []
        #checks the range of i from 1 to mx distance
        for i in range(1, distance + 1):
            #current coordinate plus index multiplied by distance traveled
            new_y = y + i * y_d
            #x coordinate does not change
            new_x = x
            #if y is out of bounds break
            if new_y < 0 or new_y > 7:
                break
            #if location is None add to moves list
            elif self._game.board[new_y][new_x] is None:
                moves.append((new_y, new_x))
            #if location is a piece of opposite color add to moves list
            elif self._game.board[new_y][new_x].color is not None and self._game.board[new_y][new_x].color != self._color:
                moves.append((new_y, new_x))
                #break because you cannot jump over a piece
                break
            #anything else break
            else:
                break
        #return the moves list
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
        """finds all valid moves for each piece"""
        #moves list
        moves = []
        #returns list of moves
        return moves

    def copy(self):
        """Returns a copy of the piece along with the state of the board."""
        """new_game = Game()
        new_game.board = [[None for _ in range(8)] for _ in range(8)]
        for y in range(8):
            for x in range(8):
                piece = self._game.board[y][x]
                if piece is not None:
                    new_game.board[y][x] = piece.copy()

        new_piece = type(self)(self.color)
        new_piece._game = new_game
        return new_piece"""
        pass

class King(Piece):
    """inherits from the Piece class, defines all moves
    a King is able to make"""
    def __init__(self, color: Color):
        """sets the image of a piece depending on its color"""
        Piece.__init__(self, color)
        #sets the image based on color
        if color == Color.WHITE:
            self.set_image(0, 0)
        else:
            self.set_image(0, 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """lists all valid moves for the King"""
        #list of moves
        moves = []
        #list of diagonal moves
        moves += self._diagonal_moves(y, x, -1, -1, 1)
        moves += self._diagonal_moves(y, x, 1, -1, 1)
        moves += self._diagonal_moves(y, x, -1, 1, 1)
        moves += self._diagonal_moves(y, x, 1, 1, 1)
        #list of horizontal moves
        moves += self._horizontal_moves(y, x, 0, -1, 1)
        moves += self._horizontal_moves(y, x, 0, 1, 1)
        #list of vertical moves
        moves += self._vertical_moves(y, x, -1, 0, 1)
        moves += self._vertical_moves(y, x, 1, 0, 1)
        #returns moves list
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
        Piece.__init__(self, color)
        #sets the image based on color
        if color == Color.WHITE:
            self.set_image(105, 0)
        else:
            self.set_image(105, 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """lists all valid moves for the Queen"""
        #list of moves
        moves = []
        #list of diagonal moves
        moves += self._diagonal_moves(y, x, -1, -1, 8)
        moves += self._diagonal_moves(y, x, 1, -1, 8)
        moves += self._diagonal_moves(y, x, -1, 1, 8)
        moves += self._diagonal_moves(y, x, 1, 1, 8)
        #list of horizontal moves
        moves += self._horizontal_moves(y, x, 0, -1, 8)
        moves += self._horizontal_moves(y, x, 0, 1, 8)
        #list of vertical moves
        moves += self._vertical_moves(y, x, -1, 0, 8)
        moves += self._vertical_moves(y, x, 1, 0, 8)
        #return moves list
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
        Piece.__init__(self, color)
        #sets the image based on color
        if color == Color.WHITE:
            self.set_image(210, 0)
        else:
            self.set_image(210, 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """lists all valid moves for the Bishop"""
        #list of moves
        moves = []
        #diagonal moves
        moves += self._diagonal_moves(y, x, -1, -1, 8)
        moves += self._diagonal_moves(y, x, 1, -1, 8)
        moves += self._diagonal_moves(y, x, -1, 1, 8)
        moves += self._diagonal_moves(y, x, 1, 1, 8)
        #returns list of moves
        return moves

    def copy(self):
        """returns a new Bishop of the same color"""
        new_bishop = Bishop(self.color)
        new_bishop._game = self._game
        return new_bishop

class Knight(Piece):
    """inherits from the Piece class, defines all moves
    a Knight is able to make"""
    def __init__(self, color: Color):
        """sets the image of a piece depending on its color"""
        Piece.__init__(self, color)
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
            else:
                moves.append((new_y, new_x))

        valid_moves = [move for move in moves if move not in bad_moves]
        if self._game.board[y][x] is not None and self._game.board[y][x].color != self.color:
            bad_moves.append((y, x))
        valid_moves.append((y, x))
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
        Piece.__init__(self, color)
        #sets the image based on color
        if color == Color.WHITE:
            self.set_image(420, 0)
        else:
            self.set_image(420, 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """lists all valid moves for the Rook"""
        #moves list
        moves = []
        #horizontal moves
        moves += self._horizontal_moves(y, x, 0, -1, 8)
        moves += self._horizontal_moves(y, x, 0, 1, 8)
        #vertical moves
        moves += self._vertical_moves(y, x, -1, 0, 8)
        moves += self._vertical_moves(y, x, 1, 0, 8)
        #return list of moves
        return moves

    def copy(self):
        """returns a new Rook of the same color"""
        new_rook = Rook(self.color)
        new_rook._game = self._game
        return new_rook

class Pawn(Piece):
    """inherits from the Piece class, defines all moves
    a Pawn is able to make"""
    def __init__(self, color: Color):
        """sets the image of a piece depending on its color"""
        Piece.__init__(self, color)
        #sets the image based on color
        if color == Color.WHITE:
            self.set_image(525, 0)
        else:
            self.set_image(525, 105)
        self.moved = False

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """lists all valid moves for the Pawn"""
        #moves list
        moves = []
        #vertical moves
        if self.color == Color.BLACK:
            moves += self._vertical_moves(y, x, -1, 0, 1)
        if self.color == Color.WHITE:
            moves += self._vertical_moves(y, x, 1, 0, 1)

        #if White Pawn has not moved, can also move forward 2 spaces
        if not self.moved and self.color == Color.WHITE:
            moves += self._vertical_moves(y, x, 1, 0, 2)
        #if Black Pawn has not moved, can also move forward 2 spaces
        if not self.moved and self.color == Color.BLACK:
            moves += self._vertical_moves(y, x, -1, 0, 2)

        #if White Pawn and enemy in diagonal, add to move list
        if self.color == Color.WHITE and self._diagonal_moves(y, x, 1, -1, 1) != self._color and not None:
            moves += self._diagonal_moves(y, x, 1, -1, 1)
        #if White Pawn and enemy in diagonal, add to move list
        if self.color == Color.WHITE and self._diagonal_moves(y, x, 1, 1, 1) != self.color and not None:
            moves += self._diagonal_moves(y, x, 1, 1, 1)
        #if Black Pawn and enemy in diagonal, add to move list
        if self.color == Color.BLACK and self._diagonal_moves(y, x, -1, -1, 1) != self.color and not None:
            moves += self._diagonal_moves(y, x, -1, -1, 1)
        #if Black Pawn and enemy in diagonal, add to move list
        if self.color == Color.BLACK and self._diagonal_moves(y, x, -1, 1, 1) != self.color and not None:
            moves += self._diagonal_moves(y, x, -1, 1, 1)
        #return list of moves
        return moves

    def copy(self):
        """returns a new Pawn of the same color"""
        new_pawn = Pawn(self.color)
        new_pawn._game = self._game
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
        #sets current player
        self.current_player = Color.WHITE
        #initializes the board
        self.board = [[None for _ in range(8)] for _ in range(8)]
        #creates an empty list for prior states
        self.prior_state = []
        #sets up the pieces
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
        self.board[0][7] = Rook(Color.WHITE)
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
        #if the pieces are in the board return them to their position
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
        #checks if list is empty
        if len(self.prior_state) > 0:
            #pops most recent board
            self.prior_state.pop()
            #sets board as the prior board
            self.board = self.prior_state[-1]
            return True
        else:
            return False

    def copy_board(self):
        """copies the entire current game board"""
        new_board = [[None for _ in range(8)] for _ in range(8)]
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece is not None:
                    new_board[y][x] = piece.copy()
        new_game = Game()
        new_game.board = new_board
        return new_game

    def move(self, piece: Piece, y: int, x: int, y2: int, x2: int) -> bool:
        """moves the pieces on the board"""
        #copies the current state of the board
        self.prior_state.append(self.copy_board())

        self.board[y2][x2] = piece
        self.board[y][x] = None

        #if the piece is a pawn, set moved to True
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
                #sets piece equal to a location
                piece = self.get(y, x)
                #if piece is not None and a color add it to locations list
                if piece is not None and piece.color == color:
                    locations.append((y, x))
        #returns locations list
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
        #sets what the opposite color is based on current_player color
        opposite_color = Color.WHITE if color == Color.BLACK else Color.BLACK
        #sets locations equal to a list of all opposite colors pieces
        locations = self.get_piece_locations(opposite_color)
        #finds the kings locations
        king_location = self.find_king(color)
        for loc in locations:
            #looks through moves in locations
            piece = self.get(loc[0], loc[1])
            #checks if it is a piece and is the opposite color
            if piece and piece.color == opposite_color:
                #if the king is in opposite colors valid locations return True
                if king_location in piece.valid_moves(loc[0], loc[1]):
                    return True
        #anything else return False
        return False

    def mate(self, color: Color) -> bool:
        """checks if a player is in check mate"""
        # if not in check cannot be in check mate
        if not self.check(color):
            return False

        # find the king's position
        king_position = self.find_king(color)

        # check if the king can move out of check
        king = self.get(king_position[0], king_position[1])
        for move in king.valid_moves(king_position[0], king_position[1], self):
            # copy the board to see if a move will place player in checkmate or not
            board_copy = self.copy_board()
            board_copy.move(king, king_position[0], king_position[1], move[0], move[1])
            if not board_copy.check(color):
                return False

        # check if any piece can block the check or capture the checking piece
        for loc in self.get_piece_locations(color):
            piece = self.get(loc[0], loc[1])
            possible_moves = piece.valid_moves(loc[0], loc[1], self)
            for move in possible_moves:
                board_copy = self.copy_board()
                board_copy.move(piece, loc[0], loc[1], move[0], move[1])
                if not board_copy.check(color):
                    return False

        return True

    def _computer_move(self) -> bool:
        """Selects a random valid move for the computer player"""
        self.switch_player()
