
import pandas as pd
import numpy as np

# Load the earthquake dataset
df = pd.read_csv("global_earthquakes_seismic.csv")

# Display the first five rows
print(df.head())

# Check the dataset size
print("Rows and columns:", df.shape)

# Review column names and data types
df.info()
