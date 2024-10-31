# Perfect Performance Ratings (PPR) Calculator

## Overview

The **Perfect Performance Ratings (PPR) Calculator** is a Python script designed to compute a Performance Rating Equilibrium for players in a chess tournament based on PGN files. PPRs are a vector of hypothetical ratings for each player such that, after scoring their points in the tournament, every player's initial rating remains unchanged. In other words, all players' initial ratings perfectly predict their actual scores in the tournament. This property, however, does not hold for the well-known Tournament Performance Rating (TPR) because is calculated using a player's opponents' pre-tournament ratings. A vector of PPRs is a fixed point of the rating function. Numerically, the PPRs can be calculated iteratively starting from some vector of ratings and updating initial ratings after each iteration. Here, the main implementation uses the uniform vector with tournament average rating to select a performance rating equilibrium. 

## Features

- **PGN Processing**: Reads multiple PGN files to extract game results and player ratings.
- **Performance Rating Calculations**: Supports calculation of **Tournament Performance Rating (TPR)** and **Linear Performance Rating**.
- **Iterative Computation**: Iteratively computes PPRs until convergence or until a maximum number of iterations is reached.
- **Missing Ratings Handling**: Handles missing player ratings by substituting the tournament average rating.
- **CSV Export**: Exports the final performance ratings to a CSV file for easy analysis.

## Requirements

- Python 3.x
- [pandas](https://pandas.pydata.org/)
- [numpy](https://numpy.org/)
- [scipy](https://www.scipy.org/)
- [python-chess](https://python-chess.readthedocs.io/en/latest/)

## Installation

Install the required Python packages using pip:

```bash
pip install pandas numpy scipy python-chess
```

## Usage

1. **Prepare PGN Files**: Place your PGN files in a directory.

2. **Configure Parameters**: Modify the script parameters as needed:

   ```python
   # Set performance rating type ('TPR' or 'linear')
   performance_rating_type = 'TPR'
   
   # Set maximum number of iterations for convergence
   max_iterations = 1000
   
   # Set initial ratings to 'average_rating' or 'pre_tournament_ratings'
   initial_ratings = 'average_rating'
   
   # Set tournament average rating if ratings are unavailable (None if ratings are available)
   tar = None
   
   # Path to the directory containing PGN files
   pgn_input_dir = '/path/to/pgn/files'
   ```

3. **Run the Script**:

   ```bash
   python pre_calculator.py
   ```

4. **Output**: The script will generate a `PPRs.csv` file containing the performance ratings.

## CSV Output Format

The CSV file includes the following columns:

- **Rank**: Player's rank based on points.
- **Name**: Player's name.
- **Rating**: Player's initial rating.
- **Points**: Total points scored in the tournament.
- **TPR**: Tournament Performance Rating.
- **PPR**: Perfect Performance Ratings after convergence.

## Notes

- If player ratings are missing in the PGN files, the script uses the provided `tar` value.
- The script removes players with no games from the calculations.
- Convergence is determined when the rounded PPR values do not change across iterations.
- The script handles both standard result notation (e.g., `1-0`, `0-1`, `1/2-1/2`) and Unicode half symbols (e.g., `½-½`).

## License

This project is licensed under the GPL License.

## Reference
- For more information, see https://kclpure.kcl.ac.uk/portal/en/publications/performance-rating-equilibrium
- For other performance ratings, including the Estimated Performance Rating, see https://github.com/drmehmetismail/Estimated-Performance-Rating

## Citation
Please cite the following paper if you find this helpful.
```
@article{ismail2024,
  title={Performance Rating Equilibrium},
  author={Ismail, Mehmet S},
  journal={arXiv preprint arXiv:2410.19006},
  year={2024}
}
```
