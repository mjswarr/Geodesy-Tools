# Utility Script to Smooth Kinematic Timeseries Using a Backwards Smoothing Algorithm
# Matthew J. Swarr May 30, 2024

import numpy as np

def main(data, window_size):
    """
    Applies backward smoothing using a moving average filter with proper handling of boundaries.

    Args:
      data: A numpy array of your data points.
      window_size: The size of the moving average window.

    Returns:
      A numpy array of the backward smoothed data.
    """
    smoothed_data = np.zeros_like(data)
    # Reverse iteration for backward smoothing
    for i in range(len(data) - 1, -1, -1):
        # Limit window size to avoid exceeding array bounds
        window_start = max(0, i - window_size + 1)  # Ensures window stays within data
        smoothed_data[i] = np.mean(data[window_start:i + 1])
    return smoothed_data
