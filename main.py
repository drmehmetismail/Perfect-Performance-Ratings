from perfect_performance_ratings import main_ppr

def main():
    # Enter 'standard' (TPR) or 'linear' for performance rating type
    performance_rating_type = 'standard'
    # Set maximum number of iterations for convergence
    max_iterations = 1000
    # Set initial_ratings to 'average_rating' or 'pre_tournament_rating'. 
    initial_ratings = 'average_rating'
    # Set tournament average rating if ratings are unavailable. Enter None if ratings are available.
    tar = None
    # For PGN input
    pgn_input_dir = '/path/to/pgn/files'
    main_ppr(pgn_input_dir, performance_rating_type, max_iterations, initial_ratings, tar)
