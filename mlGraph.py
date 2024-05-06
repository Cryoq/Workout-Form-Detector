import matplotlib.pyplot as plt
import numpy as np

# Your NumPy data
data = np.load("data/MLLeftCurl.npy")

# Flatten the arrays
x_values = data[:, :, 0].flatten()  # Flatten x coordinates
y_values = data[:, :, 1].flatten()  # Flatten y coordinates

# Plot all points in a single graph
plt.figure(figsize=(8, 6))  # Adjust figure size as needed
plt.scatter(x_values, y_values, s=5, color='blue', alpha=0.5)  # Scatter plot of all keypoints
plt.title("All Keypoints in Multiple Frames")  # Set the title of the plot
plt.xlabel("X Coordinate")  # Label for x-axis
plt.ylabel("Y Coordinate")  # Label for y-axis
plt.grid(True)  # Add grid lines
plt.tight_layout()  # Adjust layout to prevent overlapping labels
plt.show()  # Display the plot
