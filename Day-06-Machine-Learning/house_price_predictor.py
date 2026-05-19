from sklearn.linear_model import LinearRegression
import pandas as pd
import joblib

# Load small CSV

df = pd.read_csv('dataset.csv')
X = df[['area']]
y = df['price']

model = LinearRegression()
model.fit(X,y)
joblib.dump(model, 'model.pkl')
print('Model trained and saved to model.pkl')
