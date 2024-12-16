The goal of this code was to create a class called ChessVar that would implement an abstract version of the chess variant Fog of War. 
The game will start with the standard chess set up. White will always move first. Pieces move the same was as standard Chess and 
pieces are also captured in the same way. However, there are no checks, checkmates, castling, en passant, or pawn promotion. 
The game ends when a player's king is captured, and that player loses. 

In this particular version of Fog of War, the players can see any open spaces, all of their pieces (that are not captured), 
and any of the other player's pieces that are within a valid move. 

The objective of the game is not to checkmate, but to capture the king. Players are not told their king is in check, and they 
are not required to move their king out of check. 

Project requirements included the following:
-get_game_state method to return UNFINISHED, WHITE_WON, or BLACK_WON
-get_board method that takes the parameter of the perspective of the board. Can display the view from the audience or either player 
-make_move method that takes the start locatoin and the end location of the move. The locations will be in the algebraic notation
on the board, such as "a8" and "b2". If the move is valid, the method returns True. If the move is invalid, the method returns False. 
It should check if the game is already won, if the square being moved from does not belong to the player whose turn it is, or if the
requested move is not legal. Any of those would result in a False. 

The auto-testing of this code required the board to be displayed as a nested list, like so: 

[ ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], 
  ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], 
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
  ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
  ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'] ]

The lowercase letters are the black pieces and the uppercase letters are the white pieces. The empty spaces are " ". 
If the spaces are not visible based on the board perspecive, they will be respresented by a "*". 
