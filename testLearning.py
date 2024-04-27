import numpy as np


X_train = np.load("data/3PointsWorkout_data.npy")

#X_train = np.array(a)

new_data_point = np.array([0.45, 0.62, 0.55, 0.48, 0.49, 0.35])

print(new_data_point)
distances = np.linalg.norm(X_train - new_data_point, axis=1)

nearest_neighbor_idx = np.argmin(distances)
print(nearest_neighbor_idx)

distance_to_nearest_neighbor = distances[nearest_neighbor_idx]
print("Distance to nearest trained data point:", distance_to_nearest_neighbor)
