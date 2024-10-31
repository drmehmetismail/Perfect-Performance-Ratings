# Perfect Performance Ratings (PPR)

## Overview

The **Perfect Performance Ratings (PPR)** is a Python script designed to compute a Performance Rating Equilibrium for players in a chess tournament based on PGN files. PPRs are a vector of hypothetical ratings for each player such that, after scoring their points in the tournament, every player's initial rating remains unchanged. In other words, all players' initial ratings perfectly predict their actual scores in the tournament. This property, however, does not hold for the well-known Tournament Performance Rating (TPR) because is calculated using a player's opponents' pre-tournament ratings. A vector of PPRs is a fixed point of the rating function. Numerically, the PPRs can be calculated iteratively starting from some vector of ratings and updating initial ratings after each iteration. Here, the main implementation uses the uniform vector with tournament average rating to select a performance rating equilibrium. 

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

Table shows the PPRs from the 1970 Palma de Mallorca Interzonal Tournament. The Interzonal events were part of the World Chess Championship cycle and are similar to the current Chess World Cup. Since the first official FIDE Elo list was not published until 1971, players in this tournament did not have official ratings. However, based on the first published ratings for the players, it is possible to estimate the tournament's average rating at approximately 2557. The resulting PPRs are presented in the table.

| Rank | Name        | Points | PPR  | Rank | Name      | Points | PPR  |
|------|-------------|--------|------|------|-----------|--------|------|
| 1    | Fischer     | 18.5   | 2805 | 13   | Hort      | 11.5   | 2556 |
| 2    | Larsen      | 15     | 2669 | 14   | Ivkov     | 10.5   | 2525 |
| 3    | Geller      | 15     | 2669 | 15   | Suttles   | 10     | 2509 |
| 4    | Huebner     | 15     | 2669 | 16   | Minic     | 10     | 2509 |
| 5    | Taimanov    | 14     | 2636 | 17   | Reshevsky | 9.5    | 2493 |
| 6    | Uhlmann     | 14     | 2636 | 18   | Matulovic | 9      | 2477 |
| 7    | Portisch    | 13.5   | 2620 | 19   | Addison   | 9      | 2477 |
| 8    | Smyslov     | 13.5   | 2620 | 20   | Filip     | 8.5    | 2460 |
| 9    | Polugaevsky | 13     | 2604 | 21   | Naranja   | 8.5    | 2460 |
| 10   | Gligoric    | 13     | 2604 | 22   | Ujtumen   | 8.5    | 2460 |
| 11   | Panno       | 12.5   | 2588 | 23   | Rubinetti | 5      | 2350 |
| 12   | Mecking     | 12.5   | 2588 | 24   | Jimenez   | 5.5    | 2372 |

For a more recent example, in the 2017 FIDE Grand Prix Palma de Mallorca, Jakovenko was ranked 1st according to the TPR tiebreak, but Aronian's PPR was higher because his opponents performed better in the tournament. For similar reasons, Nakamura's and Svidler's PPRs are also noticeably higher than their TPRs.

| Rk. | Name                   | Rtg  | Pts. | TPR  | PRE  |
| --- | ---------------------- | ---- | ---- | ---- | ---- |
| 1   | Jakovenko Dmitry       | 2721 | 5.5  | 2823 | 2841 |
| 2   | Aronian Levon          | 2801 | 5.5  | 2821 | 2857 |
| 3   | Radjabov Teimour       | 2741 | 5    | 2764 | 2743 |
| 4   | Rapport Richard        | 2692 | 5    | 2762 | 2744 |
| 5   | Tomashevsky Evgeny     | 2702 | 5    | 2791 | 2813 |
| 6   | Nakamura Hikaru        | 2780 | 5    | 2792 | 2830 |
| 7   | Svidler Peter          | 2763 | 5    | 2782 | 2815 |
| 8   | Ding Liren             | 2774 | 5    | 2771 | 2783 |
| 9   | Harikrishna P.         | 2738 | 5    | 2767 | 2789 |
| 10  | Inarkiev Ernesto       | 2683 | 4.5  | 2734 | 2699 |
| 11  | Vachier-Lagrave Maxime | 2796 | 4.5  | 2741 | 2768 |
| 12  | Eljanov Pavel          | 2707 | 4.5  | 2724 | 2706 |
| 13  | Li Chao B              | 2741 | 4    | 2656 | 2624 |
| 14  | Vallejo Pons Francisco | 2705 | 4    | 2679 | 2644 |
| 15  | Giri Anish             | 2762 | 4    | 2693 | 2696 |
| 16  | Riazantsev Alexander   | 2651 | 3.5  | 2640 | 2623 |
| 17  | Gelfand Boris          | 2719 | 3    | 2580 | 2555 |
| 18  | Hammer Jon Ludvig      | 2629 | 3    | 2586 | 2562 |

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
