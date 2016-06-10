"""
Monte Carlo Tic-Tac-Toe Player
"""
import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
NTRIALS = 100 # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
def mc_trial(board, player):
    """
    Plays a game with alternating players, with the parameter
    "player" being the first to go
    """
    progress = board.check_win()
    while progress == None:
        empty_squares = board.get_empty_squares()
        square = random.choice(empty_squares)
        board.move(square[0], square[1], player)
        player = provided.switch_player(player)
        progress = board.check_win()
    

def mc_update_scores(scores, board, player):
    """
    Scores the board after a finished game and updates
    the scores board
    """
    game_condition = board.check_win()
    if game_condition != provided.DRAW and game_condition != None:
        dimension = board.get_dim()
        
        # If the machine player won
        if game_condition == player:
            for row in range(dimension):
                for col in range(dimension):
                    if board.square(row, col) == player:
                        scores[row][col] += MCMATCH
                    if board.square(row, col) != player and board.square(row, col) != provided.EMPTY:
                        scores[row][col] -= MCOTHER
        else:
            for row in range(dimension):
                for col in range(dimension):
                    if board.square(row, col) == player:
                        scores[row][col] -= MCMATCH
                    if board.square(row, col) != player and board.square(row, col) != provided.EMPTY:
                        scores[row][col] += MCOTHER

def get_best_move(board, scores):
    """
    Returns an empty square with the maximum amount of points
    as determined by scores
    """
    empty_squares = board.get_empty_squares()
    best_squares = []
    highest_score = float("-inf")
    for square in empty_squares:
        score = scores[square[0]][square[1]]
        if score == highest_score:
            best_squares.append(square)
        elif score > highest_score:
            highest_score = score
            best_squares = []
            best_squares.append(square)
            
    return random.choice(best_squares)

def mc_move(board, player, trials):
    """
    Uses a Monte Carlo simulation to return a move for the
    machine player
    """
    scores = [[0 for dummy_x in xrange(board.get_dim())] for dummy_y in xrange(board.get_dim())]
    for dummy_trial in range(trials):
        copy = board.clone()
        mc_trial(copy, player)
        mc_update_scores(scores, copy, player)
    return get_best_move(board, scores)



#Uncomment whichever you prefer

#provided.play_game(mc_move, NTRIALS, False)
poc_ttt_gui.run_gui(3, provided.PLAYERO, mc_move, NTRIALS, False)
