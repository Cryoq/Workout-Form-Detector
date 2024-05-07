import numpy as np
import csv
from metric_learn import LMNN
#from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
data = []
with open('3PointsWorkout_data.csv', 'r') as file:
  reader = csv.reader(file)
  # Skip the header row (optional)
  next(reader, None)
  for row in reader:
    # Assuming each row has 3 data points (LeftShoulder, Wrist, Elbow)
    data_row = []
    for value in row:
      # Convert each value within double quotes to a list of floats (assuming numerical data)
      data_row.append(eval(value.replace("[", "").replace("]", "")))
    data.append(data_row)

X1 = np.array(data)

print(X1)
#Y1 = np.ones(len(X1))


x,y = X1.T 

plt.scatter(x,y)
plt.xlabel("X coordinate")
plt.ylabel("Y coordiante")
plt.show()

lmnn = LMNN(random_state=42)
lmnn.fit(x,y)
