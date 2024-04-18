import pandas as pd

# Read the data
data = pd.read_csv("workout_data.csv", header=None, sep=",")

# Convert to list
data_list = data.values.tolist()
header = data_list[0]
data_list.pop(0)

# Display the list
print(f"Header: {header}")
print(f"Data: {data_list[10]}")