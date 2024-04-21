import numpy as np
import csv
from metric_learn import LMNN
a = np.load("3PointsWorkout_data.npy")
# X_train = np.array([[0.47827789187431335, 0.6030411124229431, 0.57664555311203, 0.525347113609314, 0.4774675667285919, 0.29115378856658936],[0.478282630443573, 0.5503517389297485,0.5777660608291626, 0.5291071534156799,0.4798343777656555, 0.29119014739990234],[0.4773612916469574, 0.48503944277763367,0.5782877206802368, 0.5384505391120911,0.48232486844062805, 0.2880226969718933]])
# y_train = np.array([1,2,3])
# lmnn = LMNN(k=1, learn_rate=1e-6)
# lmnn.fit(X_train, y_train)

# new_data_point = np.array([[0.45, 0.62, 0.55, 0.48, 0.49, 0.35]])
# new_data_point_transformed = lmnn.transform(new_data_point)
# print(new_data_point_transformed)
# distances = np.linalg.norm(X_train - new_data_point_transformed, axis=1)
# print(distances)
# nearest_neighbor_idx = np.argmin(distances)
# distance_to_nearest_neighbor = distances[nearest_neighbor_idx]

# print("Distance to nearest trained data point:", distance_to_nearest_neighbor)

X_train = np.array(a)
y_train = np.array([y for x in range(56//4) for y in range(1,5)])
lmnn = LMNN(k=1, learn_rate=1e-6)
lmnn.fit(X_train, y_train)


new_data_point = np.array([[0.45, 0.62, 0.55, 0.48, 0.49, 0.35]])
# new_data_point_transformed = lmnn.transform(new_data_point)
print(new_data_point)
distances = np.linalg.norm(X_train - new_data_point, axis=1)

nearest_neighbor_idx = np.argmin(distances)
print(nearest_neighbor_idx)
distance_to_nearest_neighbor = distances[nearest_neighbor_idx]

print("Distance to nearest trained data point:", distance_to_nearest_neighbor)