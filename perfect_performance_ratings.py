"""
Perfect Performance Ratings (PPRs) Numerical Calculator:
PPR is a sequence of hypothetical ratings r_i for every player i in a tournament, 
such that after scoring m_i points in n rounds, every player's initial rating 
r_i remains unchanged. Performance Rating Equilibrium is a fixed point of the rating mapping. 
A player's Performance Rating Equilibrium (PRE) value is called their PPR. Numerically, a PRE can be calculated iteratively starting from some initial ratings
(here it's the tournament average ratings) and  updating initial ratings after each iteration.
"""

import pandas as pd
import numpy as np
from scipy.optimize import root_scalar
import os
import chess.pgn
import math

# Calculate the expected score of a player against a list of opponents
def expected_score(opponent_ratings, own_rating):
    # Filter out None values from opponent_ratings
    opponent_ratings = [r for r in opponent_ratings if r is not None]
    if own_rating is None or not opponent_ratings:
        # Cannot compute expected score without own_rating or opponent_ratings
        return None
    return sum(1 / (1 + 10 ** ((r - own_rating) / 400)) for r in opponent_ratings)

# tournament performance rating
def tournament_performance_rating(opponent_ratings, score, min_max_list):
    opponent_ratings = [r for r in opponent_ratings if r is not None]

    if not opponent_ratings:
        # Cannot compute performance rating without opponent ratings
        return None
    # if score is 0 or perfect score, then ask CPR
    if score == 0 or score == len(opponent_ratings):
        return complete_performance_rating(opponent_ratings, score, min_max_list)
    else:
        try:
            result = root_scalar(
                lambda r: expected_score(opponent_ratings, r) - score,
                bracket=[0, 4000],
                method='brentq'
            )
            tpr = round(result.root, 1) if result.converged else None
            min_rating, max_rating = min_max_list[0], min_max_list[1]
            # return tpr bounded by min and max ratings
            return np.maximum(min_rating, np.minimum(max_rating, tpr)) if result.converged else None
        except ValueError:
            return None

# linear performance rating
def linear_performance_rating(opponent_ratings, score):
    # Calculate the average ratings of the opponents for i, sum x_j's for j != i
    sum_term = np.sum(opponent_ratings)
    k = len(opponent_ratings)
    lpr = sum_term / (k) + 800*(score/(k)) - 400
    return np.maximum(0, lpr)

# complete performance rating
def complete_performance_rating(opponent_ratings, score, min_max_list):
    sum_term = np.sum(opponent_ratings)
    k = len(opponent_ratings)
    average_opponent_rating = sum_term / k
    cpr = average_opponent_rating - ((k+1)/k) * 400 * math.log10((k + 0.5 - score) / (score + 0.5))
    min_rating, max_rating = min_max_list[0], min_max_list[1]
    # return cpr bounded by min and max ratings
    return np.maximum(min_rating, np.minimum(max_rating, cpr))

# Calculate the lower and upper bounds for the performance ratings
def min_max_rating(player_data):
    # Find the highest rated player
    highest_rated_player = max(player_data.values(), key=lambda x: x['Rating'])
    num_rounds = len(highest_rated_player['opponent_ratings'])
    
    # Get top 'num_rounds' rated players
    sorted_players_desc = sorted(player_data.values(), key=lambda x: x['Rating'], reverse=True)
    opponent_ratings_max = [player['Rating'] for player in sorted_players_desc[:num_rounds]]
    
    # Get bottom 'num_rounds' rated players
    sorted_players_asc = sorted(player_data.values(), key=lambda x: x['Rating'])
    opponent_ratings_min = [player['Rating'] for player in sorted_players_asc[:num_rounds]]
    
    def cpr_small(opponent_ratings, score):
        sum_term = np.sum(opponent_ratings)
        k = len(opponent_ratings)
        return sum_term / k - ((k+1)/k) * 400 * math.log10((k + 0.5 - score) / (score + 0.5))

    # Calculate complete performance ratings
    max_rating = cpr_small(opponent_ratings_max, num_rounds)
    min_rating = cpr_small(opponent_ratings_min, 0)
    min_max_list = [min_rating, max_rating]
    return min_max_list


def process_pgn_files(pgn_input_dir, tar):
    player_data = {}
    player_indices = {}
    player_counter = 1  # To assign unique numbers to players
    all_ratings = []

    for dirpath, dirnames, filenames in os.walk(pgn_input_dir):
        for filename in filenames:
            if filename.endswith('.pgn'):
                pgn_file_path = os.path.join(dirpath, filename)
                with open(pgn_file_path) as pgn:
                    while True:
                        game = chess.pgn.read_game(pgn)
                        if game is None:
                            break
                        # Get the headers of the game
                        white_player = game.headers.get('White', 'Unknown')
                        black_player = game.headers.get('Black', 'Unknown')
                        result_str = game.headers.get('Result', '*')
                        white_rating = game.headers.get('WhiteElo', None)
                        black_rating = game.headers.get('BlackElo', None)
                        # Convert ratings to int
                        try:
                            white_rating = int(white_rating)
                        except:
                            white_rating = None
                        try:
                            black_rating = int(black_rating)
                        except:
                            black_rating = None

                        # Collect valid ratings
                        if white_rating > 0:
                            all_ratings.append(white_rating)
                        if black_rating > 0:
                            all_ratings.append(black_rating)

                        # Convert result string to numeric results
                        if result_str == '1-0':
                            white_result = 1.0
                            black_result = 0.0
                        elif result_str == '0-1':
                            white_result = 0.0
                            black_result = 1.0
                        elif result_str == '1/2-1/2' or result_str == '½-½':
                            white_result = 0.5
                            black_result = 0.5
                        else:
                            # In case of unknown result
                            continue

                        # Assign unique numbers to players if not already assigned
                        if white_player not in player_indices:
                            player_indices[white_player] = player_counter
                            player_counter += 1
                        if black_player not in player_indices:
                            player_indices[black_player] = player_counter
                            player_counter += 1

                        # Update white player's data
                        if white_player not in player_data:
                            player_data[white_player] = {
                                'Rank': player_indices[white_player],
                                'Name': white_player,
                                'Rating': white_rating,
                                'Points': 0.0,
                                'opponents': [],
                                'results': [],
                                'opponent_ratings': [],
                                'opponent_nums': [],
                                'PRs': []  # For storing PRs in iterations
                            }
                        player_data[white_player]['Points'] += white_result
                        player_data[white_player]['opponents'].append(black_player)
                        player_data[white_player]['results'].append(white_result)
                        player_data[white_player]['opponent_ratings'].append(black_rating)
                        player_data[white_player]['opponent_nums'].append(player_indices[black_player])

                        # Update black player's data
                        if black_player not in player_data:
                            player_data[black_player] = {
                                'Rank': player_indices[black_player],
                                'Name': black_player,
                                'Rating': black_rating,
                                'Points': 0.0,
                                'opponents': [],
                                'results': [],
                                'opponent_ratings': [],
                                'opponent_nums': [],
                                'PRs': []
                            }
                        player_data[black_player]['Points'] += black_result
                        player_data[black_player]['opponents'].append(white_player)
                        player_data[black_player]['results'].append(black_result)
                        player_data[black_player]['opponent_ratings'].append(white_rating)
                        player_data[black_player]['opponent_nums'].append(player_indices[white_player])

    # After processing all games, compute average rating
    if tar is not None:
        average_rating = tar
    elif all_ratings:
        average_rating = sum(all_ratings) / len(all_ratings)
    else:
        raise ValueError("No valid ratings found to compute average rating.")
    print("Tournament average rating: ", round(average_rating))

    # Now, set missing or None ratings to average_rating
    for player in player_data:
        if not player_data[player]['Rating'] or player_data[player]['Rating'] == 0:
            player_data[player]['Rating'] = average_rating
        # Update opponent ratings where ratings are zero or None
        player_data[player]['opponent_ratings'] = [
            rating if rating else average_rating for rating in player_data[player]['opponent_ratings']
        ]

    return player_data, average_rating

def process_player_data(player_data, average_rating, performance_rating_type, max_iterations, initial_ratings, min_max_list):
    # Remove players with no games
    player_data = {player: data for player, data in player_data.items() if len(data['opponents']) > 0}

    converged = False
    iteration = 1

    while not converged:
        # Create a mapping from player names to their PRs
        if iteration == 1:
            # keep a copy of opponent ratings
            pr_map_initial = {player: data['Rating'] for player, data in player_data.items()}
            if initial_ratings == 'pre_tournament_ratings':
                # First iteration uses pre tournament ratings
                pr_map = pr_map_initial
            else: # initial_ratings == 'average_rating'
                # First iteration uses average rating
                pr_map = {player: average_rating for player in player_data}
        else:
            # Subsequent iterations use the previous iteration's PRs
            pr_map = {player: data['PRs'][-1] if data['PRs'][-1] is not None else data['Rating']
                      for player, data in player_data.items()}

        converged = True  # Assume convergence, check if any PR changes

        # Recalculate PRs for each player
        for player, data in player_data.items():
            opponent_ratings = []
            opponent_ratings_initial = []
            for opp_name in data['opponents']:
                # Get opponent's PR or fallback to their initial rating
                opponent_pr = pr_map.get(opp_name, player_data[opp_name]['Rating'])
                opponent_pr_initial = pr_map_initial.get(opp_name, player_data[opp_name]['Rating'])
                if opponent_pr is None:
                    # If still None, use average_rating
                    opponent_pr = average_rating
                opponent_ratings.append(opponent_pr)
                opponent_ratings_initial.append(opponent_pr_initial)

            m = sum(data['results'])  # Total score

            # Calculate new PR
            if performance_rating_type == 'standard':
                new_pr = tournament_performance_rating(opponent_ratings, m, min_max_list)
            else: # performance_rating_type == 'linear':
                new_pr = linear_performance_rating(opponent_ratings, m)
            # Check for convergence
            if iteration == 1:
                # No previous PR to compare
                data['PRs'].append(new_pr)
                converged = False
                tpr = tournament_performance_rating(opponent_ratings_initial, m, min_max_list)
                # Add a TPR column to the DataFrame
                data['TPR'] = round(tpr) if tpr is not None else None
            elif iteration == 2:
                previous_pr = data['PRs'][-1]
                data['PRs'].append(new_pr)
                converged = False
            else:
                previous_pr = data['PRs'][-1]
                # Update PRs list but do not append.
                data['PRs'][-1] = new_pr
                if new_pr is None or previous_pr is None:
                    converged = False
                else:
                    if round(new_pr) != round(previous_pr):
                        converged = False

        if not converged:
            iteration += 1
            if iteration > max_iterations:
                print("Maximum iterations reached.")
                break

    return player_data

# Export the data to a CSV file
def export_to_csv(player_data):
    # Prepare data for CSV export
    export_data = []
    for player, data in player_data.items():
        # Round the final PPR values
        final_pre = round(data['PRs'][-1]) if data['PRs'][-1] is not None else None

        row = {
            'Rank': data['Rank'],
            'Name': player,
            'Rating': data['Rating'],
            'Points': data['Points'],
            'TPR': data['TPR'],
            'PPR': final_pre,
        }

        export_data.append(row)

    # Convert to DataFrame
    export_df = pd.DataFrame(export_data)

    # Sort by Points
    export_df = export_df.sort_values(by='Points', ascending=False)

    # Export to CSV
    output_csv_path = f'PPRs.csv'
    export_df.to_csv(output_csv_path, index=False)
    print(f"Performance ratings exported to PPRs.csv")
    print(export_df)


# Main function to read CSV or PGN, process data, and export PRs
def main_ppr(pgn_input_dir, performance_rating_type, max_iterations, initial_ratings, tar):
    # Process PGN files
    player_data, average_rating = process_pgn_files(pgn_input_dir, tar)

    # Call the lower and upper bounds for the performance ratings
    min_max_list = min_max_rating(player_data)

    # Process player data with iterative PR calculations until convergence
    player_data = process_player_data(player_data, average_rating, performance_rating_type, max_iterations, initial_ratings, min_max_list)

    # Call export function to save PRs to CSV
    export_to_csv(player_data)


if __name__ == "__main__":
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
