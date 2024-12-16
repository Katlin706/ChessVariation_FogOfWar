# Author: Katlin Hopkins
# GitHub username: katlin706
# Date: 12/8/2024
# Description: The code defines a variation of a chess game, the Fog of War variation. Users will input various
# attempted moves, and they will either return False or return True and will be counted as a valid move. The players
# take turns until one of the Kings is captured.


class ChessVar:
    """the ChessVar class represents the actual game of Chess, the Fog of War variation. The ChessVar game will have
    two players, a board, a game state, and a current turn. Turn defaults to the white player. No parameters are needed
    to create a ChessVar object"""

    def __init__(self):
        self._players = {"white": Player('white'), "black": Player('black')}
        self._board = Board()
        self._game_state = 'UNFINISHED'
        self._moves = 0
        self._turn = "white"

    def get_game_state(self):
        """returns the current game_state from the ChessVar class object. valid options
        are 'UNFINISHED', 'WHITE_WON' and 'BLACK_WON'. """
        return self._game_state

    def set_game_state(self, new_game_state):
        """takes a new game state as the parameter and sets the game_state of a ChessVar object. Valid options are
        'UNFINISHED', 'WHITE_WON' and 'BLACK_WON'."""
        self._game_state = new_game_state

    def get_turn(self):
        """returns the current turn from the ChessVar class object. valid options
        are ‘white’ or ‘black.’  """
        return self._turn

    def set_turn(self, next_player):
        """takes the next player as the parameter and sets the turn to that player. Valid options are ‘white’
        or ‘black.’"""
        self._turn = next_player

    def get_board(self, viewpoint):
        """takes a viewpoint as a parameter and provides the current game board. valid viewpoints are 'white', 'black'
        and 'audience', which would provide the view from the white player's viewpoint, the black player's viewpoint,
        and the audience's viewpoint, respectively. Calls out to a Board object and method"""
        return self._board.get_board_view(viewpoint)

    def make_move(self, starting_pos, ending_pos):
        """takes the starting position and the ending position as parameters. the method attempts to make the move as
        indicated by the two position parameters. Checks if the starting position contains a piece of a player whose
        turn it is. Checks that the game is not won yet. It calls out to the Pieces class and/or subclasses to see if
        that specific object can make the move that was requested. Once it is determined the move is  valid, will
        update the Board class object with the current_board layout, will update the Piece subclass object’s position
        data member, will update the number of moves of that Piece object,  will change the turn to the other player
        (by calling set_turn), will iterate the turns forward by 1, will verify if we need to update the game_state,
        and will update any Player class object pieces_captured list if necessary"""
        # if the game is won, return false
        if self._game_state == 'WHITE_WON' or self._game_state == "BLACK_WON":
            return False

        # establish variables
        valid_positions = ["a8", "a7", "a6", "a5", "a4", "a3", "a2", "a1",
                           "b8", "b7", "b6", "b5", "b4", "b3", "b2", "b1",
                           "c8", "c7", "c6", "c5", "c4", "c3", "c2", "c1",
                           "d8", "d7", "d6", "d5", "d4", "d3", "d2", "d1",
                           "e8", "e7", "e6", "e5", "e4", "e3", "e2", "e1",
                           "f8", "f7", "f6", "f5", "f4", "f3", "f2", "f1",
                           "g8", "g7", "g6", "g5", "g4", "g3", "g2", "g1",
                           "h8", "h7", "h6", "h5", "h4", "h3", "h2", "h1", ]

        # if not starting with a valid spot on the board
        if starting_pos not in valid_positions:
            return False

        # if not ending with a valid spot on the board
        if ending_pos not in valid_positions:
            return False

        # if starting and ending at the same spot
        if starting_pos == ending_pos:
            return False

        starting_pos_row = starting_pos[1:]
        ending_pos_row = ending_pos[1:]
        starting_pos_piece = self._board.get_current_board()[starting_pos_row][starting_pos]
        ending_pos_piece = self._board.get_current_board()[ending_pos_row][ending_pos]

        # if starting position is empty, return false
        if starting_pos_piece == " ":
            return False

        # if piece at starting position is the opposite color, return False
        starting_pos_piece_color = starting_pos_piece.get_player_color()
        if starting_pos_piece_color != self._turn:
            return False

        # if piece at ending pos is the same clor as the player taking a turn, return False.
        if ending_pos_piece != " ":  # make sure the spot isn't empty before asking for color
            ending_pos_piece_color = ending_pos_piece.get_player_color()
            if ending_pos_piece_color == self._turn:
                return False

        # checks if move is valid based on type of Piece subclass.
        if not starting_pos_piece.is_valid_move(starting_pos, ending_pos, self._board):
            return False

        else:
            if ending_pos_piece != " ":  # if ending pos has a piece that is being captured, run is captured method
                ending_pos_piece.set_is_captured(True, self)  # King capture handles a "win" scenario
            starting_pos_piece.update_moves_made()  # update piece's moves made
            starting_pos_piece.set_position(ending_pos)  # update piece's position on the board
            self._board.update_board_from_move(starting_pos, ending_pos)  # update layout of board

            # update the turn
            if self._turn == "white":
                self._turn = "black"
            elif self._turn == "black":
                self._turn = "white"
            # increase the number of moves of the whole game
            self._moves += 1
            return True  # valid move returns True


class Player:
    """The Player class represents the players of the game. The two players will always be 'white' and 'black' to
    match the color of the standard Chess pieces. Player objects will be created when a ChessVar object is created."""

    def __init__(self, player_type):
        self._player_type = player_type
        self._pieces = []

    def get_player_type(self):
        """returns the Player object’s player_type which should be ‘white’ or ‘black.’"""
        return self._player_type


class Board:
    """The Board class represents the physical board the game is played on. A board object will always be created when
    a ChessVar object is created, as ChessVar initialized a Board object in its default data members. A board object
    will contain the layout/structure of the current board, and will also generate all the board_pieces by calling out
    to the individual pieces classes (Rook, Knight, etc.) that are subclassed to the Pieces class. The Rook, Knight,
    Queen, King, Bishop, and Pawn objects will be placed in their default starting position on the board."""

    def __init__(self):
        self._black_rook_1 = Rook("black", "r", "a8")
        self._black_knight_1 = Knight("black", "n", "b8")
        self._black_bishop_1 = Bishop("black", "b", "c8")
        self._black_queen = Queen("black", "q", "d8")
        self._black_king = King("black", "k", "e8")
        self._black_bishop_2 = Bishop("black", "b", "f8")
        self._black_knight_2 = Knight("black", "n", "g8")
        self._black_rook_2 = Rook("black", "r", "h8")
        self._black_pawn_1 = Pawn("black", "p", "a7")
        self._black_pawn_2 = Pawn("black", "p", "b7")
        self._black_pawn_3 = Pawn("black", "p", "c7")
        self._black_pawn_4 = Pawn("black", "p", "d7")
        self._black_pawn_5 = Pawn("black", "p", "e7")
        self._black_pawn_6 = Pawn("black", "p", "f7")
        self._black_pawn_7 = Pawn("black", "p", "g7")
        self._black_pawn_8 = Pawn("black", "p", "h7")
        self._white_pawn_1 = Pawn("white", "P", "a2")
        self._white_pawn_2 = Pawn("white", "P", "b2")
        self._white_pawn_3 = Pawn("white", "P", "c2")
        self._white_pawn_4 = Pawn("white", "P", "d2")
        self._white_pawn_5 = Pawn("white", "P", "e2")
        self._white_pawn_6 = Pawn("white", "P", "f2")
        self._white_pawn_7 = Pawn("white", "P", "g2")
        self._white_pawn_8 = Pawn("white", "P", "h2")
        self._white_rook_1 = Rook("white", "R", "a1")
        self._white_knight_1 = Knight("white", "N", "b1")
        self._white_bishop_1 = Bishop("white", "B", "c1")
        self._white_queen = Queen("white", "Q", "d1")
        self._white_king = King("white", "K", "e1")
        self._white_bishop_2 = Bishop("white", "B", "f1")
        self._white_knight_2 = Knight("white", "N", "g1")
        self._white_rook_2 = Rook("white", "R", "h1")
        self._current_board = {
            "8": {"a8": self._black_rook_1, "b8": self._black_knight_1, "c8": self._black_bishop_1,
                  "d8": self._black_queen,
                  "e8": self._black_king, "f8": self._black_bishop_2, "g8": self._black_knight_2,
                  "h8": self._black_rook_2},
            "7": {"a7": self._black_pawn_1, "b7": self._black_pawn_2, "c7": self._black_pawn_3,
                  "d7": self._black_pawn_4,
                  "e7": self._black_pawn_5, "f7": self._black_pawn_6, "g7": self._black_pawn_7,
                  "h7": self._black_pawn_8},
            "6": {"a6": " ", "b6": " ", "c6": " ", "d6": " ", "e6": " ", "f6": " ", "g6": " ", "h6": " "},
            "5": {"a5": " ", "b5": " ", "c5": " ", "d5": " ", "e5": " ", "f5": " ", "g5": " ", "h5": " "},
            "4": {"a4": " ", "b4": " ", "c4": " ", "d4": " ", "e4": " ", "f4": " ", "g4": " ", "h4": " "},
            "3": {"a3": " ", "b3": " ", "c3": " ", "d3": " ", "e3": " ", "f3": " ", "g3": " ", "h3": " "},
            "2": {"a2": self._white_pawn_1, "b2": self._white_pawn_2, "c2": self._white_pawn_3,
                  "d2": self._white_pawn_4,
                  "e2": self._white_pawn_5, "f2": self._white_pawn_6, "g2": self._white_pawn_7,
                  "h2": self._white_pawn_8},
            "1": {"a1": self._white_rook_1, "b1": self._white_knight_1, "c1": self._white_bishop_1,
                  "d1": self._white_queen,
                  "e1": self._white_king, "f1": self._white_bishop_2, "g1": self._white_knight_2,
                  "h1": self._white_rook_2}
        }
        self._column_guide = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8}

    def get_column_guide(self):
        """returns the column_guide data member for a board object. used for determining column letter vs number"""
        return self._column_guide

    def get_current_board(self):
        """returns the current_board data member for a board object. Will be a nested dictionary when returning"""
        return self._current_board

    def get_board_view(self, viewpoint, index=0):
        """returns a user-friendly version of the game board, using letters for game pieces (capital letters for
        White, lowercase for black), and returns a nested list instead of a nested dictionary. The viewpoint parameter
        will determine if the returned board will be displayed from the audience perspective, where all pieces are
        visible, or from the white or black player’s perspective, where the black or the white pieces are obfuscated,
        respectively"""
        nested_list = [[], [], [], [], [], [], [], []]
        if viewpoint == "audience":
            for key in self._current_board:
                for nested_key in self._current_board[key]:
                    if self._current_board[key][nested_key] != " ":
                        nested_list[index].append(self._current_board[key][nested_key].get_display_letter())
                    else:
                        nested_list[index].append(" ")
                index += 1
            return nested_list
        else:
            for key in self._current_board:
                for nested_key in self._current_board[key]:
                    if self._current_board[key][nested_key] != " ":
                        if self._current_board[key][nested_key].get_player_color() != viewpoint:
                            nested_list[index].append(
                                self._current_board[key][nested_key].board_display_assist(nested_key, self, viewpoint))
                        elif self._current_board[key][nested_key].get_player_color() == viewpoint:
                            nested_list[index].append(self._current_board[key][nested_key].get_display_letter())
                    elif self._current_board[key][nested_key] == " ":
                        nested_list[index].append(" ")
                index += 1
            return nested_list

    def update_board_from_move(self, starting_pos, ending_pos):
        """updates the nested dictionary version of the board, the one in the current_board data member. This will only
        get called if the move is deemed valid from the ChessVar class method of make_move."""
        starting_row = starting_pos[1:]
        ending_row = ending_pos[1:]
        temp_piece = self._current_board[starting_row][starting_pos]
        self._current_board[starting_row][starting_pos] = " "
        self._current_board[ending_row][ending_pos] = temp_piece
        return


class Pieces:
    """The Pieces class is a Parent class for Rook, Pawn, Knight, Bishop, Queen, and King subclasses. The Pieces classes
     has methods and data members that will be share across the subclasses. To generate a Piece object (or one of its
     subclasses), you need to pass the color of the piece, its display letter, and its current position on the board.
     When initialized, will default to zero moves_made, and will set ‘is_captured’ to False in order to indicate it has
     not been captured yet."""

    def __init__(self, player_color, display_letter, position):
        self._moves_made = 0
        self._player_color = player_color
        self._display_letter = display_letter
        self._position = position
        self._is_captured = False

    def update_moves_made(self):
        """this method iterates forward the number of moves a piece has made. It will get called by the ChessVar class
        if the make_move method determines the player’s move is valid. The purpose is to track if a Pawn has made its
        first move yet, but could also be an interesting statistic for other pieces"""
        self._moves_made += 1
        return

    def get_moves_made(self):
        """returns the number of moves a Piece (or one of its subclasses) has made. Will be called to determine if a
        Pawn has made its first move yet"""
        return self._moves_made

    def get_player_color(self):
        """returns the player_color of the Piece (or its subclasses) object. It will be called by the Board class
        method get_board_view so that we can know which pieces to show for which users"""
        return self._player_color

    def get_display_letter(self):
        """returns the display_letter of the Piece (or its subclasses) object. It will be called by the Board class
        method get_board_view to make a user-friendly version of the board from various perspectives"""
        return self._display_letter

    def get_position(self):
        """will return the current position of the Piece object or one of the Piece subclass objects"""
        return self._position

    def set_position(self, new_position):
        """will only get called by the ChessVar class by the make_move method if the move is considered valid. Will
        set the Piece object (or an object of its subclasses) position to its new location on the board"""
        self._position = new_position

    def get_is_captured(self):
        """will return the current value of the ‘is_captured’ data member of the Piece object or one of the Piece
        subclass objects"""
        return self._is_captured

    def set_is_captured(self, new_value, game_object):
        """will be called by the make_move method from the ChessVar class if the move is valid and the move causes
        a Piece (or subclass) object to get captured. will mark a piece as captured. will also help determine if a
        game has been won, as king being is_captured = True means the game has been one by one player. The King
        subclass overrides this to add additional logic to handle the game winning aspect"""
        self._is_captured = new_value

    def board_display_assist(self, original_cell_ref, board_object, viewpoint):
        """function will allow for display view of 'white' or 'black' viewpoint. will run through all the pieces that
        belong to the viewpoint player. Will see if there are any valid moves to the opposite player's pieces. if yes,
        will display the color. if no, will display an asterisk"""
        for row in board_object.get_current_board():
            for nested_cell_ref in board_object.get_current_board()[row]:
                if board_object.get_current_board()[row][nested_cell_ref] != " ":
                    if board_object.get_current_board()[row][nested_cell_ref].get_player_color() == viewpoint:
                        if board_object.get_current_board()[row][nested_cell_ref].is_valid_move(
                                nested_cell_ref, original_cell_ref, board_object) is True:
                            return self.get_display_letter()
        return "*"


class Pawn(Pieces):
    """the Pawn class is a subclass of the Pieces class. It represents the Pawn pieces on the game board. It
    inherits the player_color, display_letter, and position from the pieces class, and it’ll be required to generate
    a Pawn object. Will contain a method to detail valid moves for Pawn pieces"""

    def __init__(self, player_color, display_letter, position):
        super().__init__(player_color, display_letter, position)

    def is_valid_move(self, starting_pos, ending_pos, board_object):
        """this method determines if a Pawn move is valid. Will allow moving two squares forward on the first move,
        one move forward on other moves, and capturing objects diagonally forward. Cannot jump over pieces. Cannot
        move forward if blocked by a piece from the other player that is not in position to be captured"""
        starting_col_numeric = int(board_object.get_column_guide()[starting_pos[0:1]])
        starting_row_numeric = int(starting_pos[1:])
        ending_col_numeric = int(board_object.get_column_guide()[ending_pos[0:1]])
        ending_row_numeric = int(ending_pos[1:])
        ending_pos_value = board_object.get_current_board()[ending_pos[1:]][ending_pos]
        row_change = ending_row_numeric - starting_row_numeric
        column_change = ending_col_numeric - starting_col_numeric

        if (self.get_moves_made() == 0 and self.get_player_color() == "white" and row_change == 2 and
                column_change == 0 and ending_pos_value == " "):  # when white, and pawn has no moves yet, can move up 2
            middle_cell = starting_pos[0:1] + str(starting_row_numeric + 1)
            if board_object.get_current_board()[middle_cell[1:]][middle_cell] != " ":
                return False
            else:
                return True
        elif (self.get_moves_made() == 0 and self.get_player_color() == "black" and row_change == -2 and
              column_change == 0 and ending_pos_value == " "):  # when black, no moves yet, can move down 2
            middle_cell = starting_pos[0:1] + str(starting_row_numeric - 1)
            if board_object.get_current_board()[middle_cell[1:]][middle_cell] != " ":
                return False
            else:
                return True
        elif self.get_player_color() == "white" and row_change == 1 and column_change == 0 and ending_pos_value == " ":
            return True
        elif self.get_player_color() == "black" and row_change == -1 and column_change == 0 and ending_pos_value == " ":
            return True
        elif self.get_player_color() == "white" and row_change == 1 and column_change in [-1, 1] and ending_pos_value != " ":
            if ending_pos_value.get_player_color() == "black":
                return True
            else:
                return False
        elif (self.get_player_color() == "black" and row_change == -1 and column_change in
              [-1, 1] and ending_pos_value != " "):
            if ending_pos_value.get_player_color() == "white":
                return True
            else:
                return False
        else:
            return False


class Rook(Pieces):
    """ the Rook class is a subclass of the Pieces class. It represents the Rook pieces on the game board.
    It inherits the player_color, display_letter, and position from the pieces class, and it’ll be required to generate
     a Rook object. Will contain a method to detail valid moves for Rook pieces"""

    def __init__(self, player_color, display_letter, position):
        super().__init__(player_color, display_letter, position)

    def is_valid_move(self, starting_pos, ending_pos, board_object):
        """This method determines if a Rook object move is valid. Will allow moving forward, backwards, or side to
        side in straight lines. Cannot jump over pieces."""
        starting_col_numeric = int(board_object.get_column_guide()[starting_pos[0:1]])
        starting_row_numeric = int(starting_pos[1:])
        ending_col_numeric = int(board_object.get_column_guide()[ending_pos[0:1]])
        ending_row_numeric = int(ending_pos[1:])
        row_change = ending_row_numeric - starting_row_numeric
        column_change = ending_col_numeric - starting_col_numeric

        if abs(row_change) > 0 and column_change == 0:  # move up or down board. row change.
            if ending_row_numeric > starting_row_numeric:  # moving up
                for row_number in range(starting_row_numeric + 1, ending_row_numeric):
                    if board_object.get_current_board()[str(row_number)][ending_pos[0:1] + str(row_number)] != " ":
                        return False
                return True
            if starting_row_numeric > ending_row_numeric:  # moving down
                for row_number in range(ending_row_numeric + 1, starting_row_numeric):
                    if board_object.get_current_board()[str(row_number)][starting_pos[0:1] + str(row_number)] != " ":
                        return False
                return True
        if abs(column_change) > 0 and row_change == 0:  # move left or right. column change.
            if ending_col_numeric > starting_col_numeric:  # moving right
                for col_number in range(starting_col_numeric + 1, ending_col_numeric):
                    for key in board_object.get_column_guide():
                        if board_object.get_column_guide()[key] == col_number:
                            if board_object.get_current_board()[str(starting_row_numeric)][
                                key + str(starting_row_numeric)] != " ":
                                return False
                return True
            if starting_col_numeric > ending_col_numeric:  # moving left
                for col_number in range(ending_col_numeric + 1, starting_col_numeric):
                    for key in board_object.get_column_guide():
                        if board_object.get_column_guide()[key] == col_number:
                            if board_object.get_current_board()[str(starting_row_numeric)][key + str(starting_row_numeric)] != " ":
                                return False
                return True
        else:
            return False


class Knight(Pieces):
    """the Knight class is a subclass of the Pieces class. It represents the Knight pieces on the game board.
    It inherits the player_color, display_letter, and position from the pieces class, and it’ll be required to
    generate a Knight object. Will contain a method to detail valid moves for Knight pieces"""

    def __init__(self, player_color, display_letter, position):
        super().__init__(player_color, display_letter, position)

    def is_valid_move(self, starting_pos, ending_pos, board_object):
        """determines if a Knight object move is valid. Will allow moving two squares vertically and one square
        horizontally, or two squares horizontally and one square vertically. Can ‘jump over’ other pieces."""
        starting_col_numeric = int(board_object.get_column_guide()[starting_pos[0:1]])
        starting_row_numeric = int(starting_pos[1:])
        ending_col_numeric = int(board_object.get_column_guide()[ending_pos[0:1]])
        ending_row_numeric = int(ending_pos[1:])
        row_change = ending_row_numeric - starting_row_numeric
        column_change = ending_col_numeric - starting_col_numeric

        if abs(row_change) == 2 and abs(column_change) == 1:
            return True
        if abs(column_change) == 2 and abs(row_change) == 1:
            return True
        else:
            return False


class Bishop(Pieces):
    """ the Bishop class is a subclass of the Pieces class. It represents the Bishop pieces on the game board. It
    inherits the player_color, display_letter, and position from the pieces class, and it’ll be required to generate
    a Bishop object. Will contain a method to detail valid moves for Bishop pieces"""

    def __init__(self, player_color, display_letter, position):
        super().__init__(player_color, display_letter, position)

    def is_valid_move(self, starting_pos, ending_pos, board_object):
        """determines if a Bishop object move is valid. Can move diagonally in any direction (forward and backward)
        but cannot jump over another piece"""
        starting_col_numeric = int(board_object.get_column_guide()[starting_pos[0:1]])
        starting_row_numeric = int(starting_pos[1:])
        ending_col_numeric = int(board_object.get_column_guide()[ending_pos[0:1]])
        ending_row_numeric = int(ending_pos[1:])
        row_change = ending_row_numeric - starting_row_numeric
        column_change = ending_col_numeric - starting_col_numeric

        if abs(row_change) == abs(column_change):  # if row change = col change, move is diagonal
            if row_change in [-1, 1]:
                return True
            if row_change > 1 and column_change > 1:
                # moving up and to the right. if moving 1, final position already checked in make_move logic
                running_row = starting_row_numeric + 1
                running_col = starting_col_numeric + 1
                for key in board_object.get_column_guide():  # for all the keys in the dict column_guide
                    if board_object.get_column_guide()[key] == running_col and running_row < ending_row_numeric:
                        if board_object.get_current_board()[str(running_row)][key + str(running_row)] != " ":
                            return False
                        running_col += 1
                        running_row += 1
                return True

            if row_change < -1 and column_change < -1:
                # moving down and to the left. if moving 1, final position already checked in make_move logic
                running_row = ending_row_numeric + 1
                running_col = ending_col_numeric + 1
                for key in board_object.get_column_guide():  # for all the keys in the dict column_guide
                    if board_object.get_column_guide()[key] == running_col and running_row < starting_row_numeric:
                        if board_object.get_current_board()[str(running_row)][key + str(running_row)] != " ":
                            return False
                        running_col += 1
                        running_row += 1
                return True

            if row_change > 1 and column_change < -1:
                # moving up and to the left. if moving 1, final position already checked in make_move logic
                running_row = ending_row_numeric - 1
                running_col = ending_col_numeric + 1
                for key in board_object.get_column_guide():  # for all the keys in the dict column_guide
                    if board_object.get_column_guide()[key] == running_col and running_row > starting_row_numeric:
                        if board_object.get_current_board()[str(running_row)][key + str(running_row)] != " ":
                            return False
                        running_col += 1
                        running_row -= 1
                return True

            if row_change < -1 and column_change > 1:
                # moving down and to the right. if moving 1, final position already checked in make_move logic
                running_row = starting_row_numeric - 1
                running_col = starting_col_numeric + 1
                for key in board_object.get_column_guide():  # for all the keys in the dict column_guide
                    if board_object.get_column_guide()[key] == running_col and running_row > ending_row_numeric:
                        if board_object.get_current_board()[str(running_row)][key + str(running_row)] != " ":
                            return False
                        running_col += 1
                        running_row -= 1
                return True
        else:
            return False


class Queen(Pieces):
    """ the Queen  class is a subclass of the Pieces class. It represents the Queen pieces on the game board. It
    inherits the player_color, display_letter, and position from the pieces class, and it’ll be required to generate a
    Queen object. Will contain a method to detail valid moves for Queen pieces"""

    def __init__(self, player_color, display_letter, position):
        super().__init__(player_color, display_letter, position)

    def is_valid_move(self, starting_pos, ending_pos, board_object):
        """determines if a Queen object move is valid. Will allow forward, backward, side to side, or diagonally
        (both forward and backward). Cannot jump over pieces."""
        starting_col_numeric = int(board_object.get_column_guide()[starting_pos[0:1]])
        starting_row_numeric = int(starting_pos[1:])
        ending_col_numeric = int(board_object.get_column_guide()[ending_pos[0:1]])
        ending_row_numeric = int(ending_pos[1:])
        row_change = ending_row_numeric - starting_row_numeric
        column_change = ending_col_numeric - starting_col_numeric

        if abs(row_change) > 0 and column_change == 0:  # move up or down board. row change.
            if ending_row_numeric > starting_row_numeric:  # moving up
                for row_number in range(starting_row_numeric + 1, ending_row_numeric):
                    if board_object.get_current_board()[str(row_number)][ending_pos[0:1] + str(row_number)] != " ":
                        return False
                return True
            if starting_row_numeric > ending_row_numeric:   # moving down
                for row_number in range(ending_row_numeric + 1, starting_row_numeric):
                    if board_object.get_current_board()[str(row_number)][starting_pos[0:1] + str(row_number)] != " ":
                        return False
                return True
        if abs(column_change) > 0 and row_change == 0:  # move left or right. column change.
            if ending_col_numeric > starting_col_numeric:  # moving right
                for col_number in range(starting_col_numeric + 1, ending_col_numeric):
                    for key in board_object.get_column_guide():
                        if board_object.get_column_guide()[key] == col_number:
                            if board_object.get_current_board()[str(starting_row_numeric)][key + str(starting_row_numeric)] != " ":
                                return False
                return True
            if starting_col_numeric > ending_col_numeric:  # moving left
                for col_number in range(ending_col_numeric + 1, starting_col_numeric):
                    for key in board_object.get_column_guide():
                        if board_object.get_column_guide()[key] == col_number:
                            if board_object.get_current_board()[str(starting_row_numeric)][key + str(starting_row_numeric)] != " ":
                                return False
                return True

        if abs(row_change) == abs(column_change):  # if row change = col change, move is diagonal
            if row_change in [-1, 1]:
                return True
            if row_change > 1 and column_change > 1:
                # moving up and to the right. if moving 1, final position already checked in make_move logic
                running_row = starting_row_numeric + 1
                running_col = starting_col_numeric + 1
                for key in board_object.get_column_guide():  # for all the keys in the dict column_guide
                    if board_object.get_column_guide()[key] == running_col and running_row < ending_row_numeric:
                        if board_object.get_current_board()[str(running_row)][key + str(running_row)] != " ":
                            return False
                        running_col += 1
                        running_row += 1
                return True

            if row_change < -1 and column_change < -1:
                # moving down and to the left. if moving 1, final position already checked in make_move logic
                running_row = ending_row_numeric + 1
                running_col = ending_col_numeric + 1
                for key in board_object.get_column_guide():  # for all the keys in the dict column_guide
                    if board_object.get_column_guide()[key] == running_col and running_row < starting_row_numeric:
                        if board_object.get_current_board()[str(running_row)][key + str(running_row)] != " ":
                            return False
                        running_col += 1
                        running_row += 1
                return True

            if row_change > 1 and column_change < -1:
                # moving up and to the left. if moving 1, final position already checked in make_move logic
                running_row = ending_row_numeric - 1
                running_col = ending_col_numeric + 1
                for key in board_object.get_column_guide():  # for all the keys in the dict column_guide
                    if board_object.get_column_guide()[key] == running_col and running_row > starting_row_numeric:
                        if board_object.get_current_board()[str(running_row)][key + str(running_row)] != " ":
                            return False
                        running_col += 1
                        running_row -= 1
                return True

            if row_change < -1 and column_change > 1:
                # moving down and to the right. if moving 1, final position already checked in make_move logic
                running_row = starting_row_numeric - 1
                running_col = starting_col_numeric + 1
                for key in board_object.get_column_guide():  # for all the keys in the dict column_guide
                    if board_object.get_column_guide()[key] == running_col and running_row > ending_row_numeric:
                        if board_object.get_current_board()[str(running_row)][key + str(running_row)] != " ":
                            return False
                        running_col += 1
                        running_row -= 1
                return True
        else:
            return False


class King(Pieces):
    """ the King class is a subclass of the Pieces class. It represents the King pieces on the game board. It
    inherits the player_color, display_letter, and position from the pieces class, and it’ll be required to generate a
     King object. Will contain a method to detail valid moves for King pieces"""

    def __init__(self, player_color, display_letter, position):
        super().__init__(player_color, display_letter, position)

    def is_valid_move(self, starting_pos, ending_pos, board_object):
        """determines if a King object move is valid. Will allow a move of one square in any direction – forward,
        backward, side to side, or diagonally, but cannot jump over pieces."""
        starting_col_numeric = int(board_object.get_column_guide()[starting_pos[0:1]])
        starting_row_numeric = int(starting_pos[1:])
        ending_col_numeric = int(board_object.get_column_guide()[ending_pos[0:1]])
        ending_row_numeric = int(ending_pos[1:])
        row_change = ending_row_numeric - starting_row_numeric
        column_change = ending_col_numeric - starting_col_numeric

        # if there is a piece in the way, will be checked by make_move logic
        if row_change in [1, -1] and column_change == 0:  # forwards or backwards
            return True
        if row_change == 0 and column_change in [-1, 1]:  # side to side
            return True
        if row_change in [-1, 1] and column_change in [-1, 1]:  # diagonal
            return True

    def set_is_captured(self, new_value, game_object):
        """will set the is_captured data member of the King object to True. Since this means a King is captured,
    that also means it will set the ChessVar object’s game_status to WHITE_WON or BLACK_WON depending on the color
    of the King being captured."""
        self._is_captured = new_value
        if self.get_player_color() == "white":
            game_object.set_game_state("BLACK_WON")
        elif self.get_player_color() == "black":
            game_object.set_game_state("WHITE_WON")
        return

