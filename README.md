# Plastic Pollution Language Simulation

This project predicts missing language labels in a marine debris dataset using gear type and color as predictors. The simulation is based on observed proportions from a cleaned subset of data.

The script `main.py` filters the hand-curated subset (`HPU Subset Data.csv`) to include only relevant and valid entries. It also generates plots to visualize distributions by gear type, color, and inferred country of origin.

The script `find_proportions.py` analyzes the filtered subset to compute the conditional probabilities of Language given Gear Type and Color. These probabilities are saved in `language_proportions.csv`.

The script `simulate_missing.py` applies these probabilities to fill in missing Language values in the master dataset (`HPU Master Data.csv`). It outputs a cleaned version of the master data (`HPU Master Data Filtered.csv`) and a final simulated dataset (`HPU Simulated Data.csv`) where Language values are either retained or filled in probabilistically. A `Simulated` column indicates which values were inferred.

Only `HPU Subset Data.csv`, `HPU Master Data.csv`, and the Python scripts should be tracked in Git. All generated CSV files can be reproduced by rerunning the scripts and should be excluded from version control.
