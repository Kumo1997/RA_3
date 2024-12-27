# RA_3

## Overview
RA_3 is a project that implements the HyperLogLog (HLL) algorithm for estimating cardinality and the Recordinality (REC) algorithm for accurate cardinality estimation. This project is designed to efficiently handle large datasets and provide statistical insights.

## Features
- **HyperLogLog (HLL)**: Estimates the number of unique elements in a dataset with low memory usage.
- **Recordinality (REC)**: Provides accurate cardinality estimates with varying parameters.
- **Performance Metrics**: Includes execution time, standard deviation, and theoretical standard error for results.

## Installation
To get started with this project, clone the repository and install the required dependencies.

## Usage
To run the project, ensure you have Python installed. You can execute the main script as follows:
run.bash:
  - HLL.py:implementation of hyperloglog algorithm
  - REC.py:implementation of Recordinality algorithm
  - main.py: read the datasets and execute with these 2 algorithm, collecting the results and execution time.
run_experiments.bash :
  - HLL.py:implementation of hyperloglog algorithm
  - REC.py:implementation of Recordinality algorithm
  - gen_data.py: generate synthetic data stream according to the zip's distribution formula.
  - main.py: read the datasets and execute with these 2 algorithm, collecting the results and execution time.

