import os
from sklearn.linear_model import LinearRegression
import pandas as pd
import joblib

# Get directory of current script
base_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(base_dir, 'dataset.csv')
model_path = os.path.join(base_dir, 'model.pkl')

# Load small CSV
df = pd.read_csv(dataset_path)
X = df[['area']]
y = df['price']

model = LinearRegression()
model.fit(X, y)
joblib.dump(model, model_path)
print(f'Model trained and saved to {model_path}')

