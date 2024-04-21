#import pandas as pd
#import torch
#import numpy as np

# Read the data
#data = pd.read_csv("3PointsWorkout_data.csv", header=None, sep=",")
#data = np.genfromtxt("3PointsWorkout_data.csv", dtype=None, delimiter=',')
#print(data)

# Convert to list
#data_list = data.values.tolist()
#header = data_list[0]
#data_list.pop(0)

# Display the list
#print(f"Header: {header}")
#print(data)

#z = torch.tensor(data)
#print(z)
import numpy as np
import csv
from metric_learn import LMNN
from sklearn.datasets import load_iris
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

iris_data = load


X_learn,X_train,Y_learn,Y_train = train_test_split(X1,Y1)
nca = LMNN(random_state=42)
nca.fit(X_train,Y_train)
LMNN(init='auto', max_iter=100, n_components=None, preprocessor=None, random_state=42, tol=None, verbose=False)
