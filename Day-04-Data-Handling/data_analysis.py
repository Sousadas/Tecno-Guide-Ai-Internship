import pandas as pd

# Example: create small DataFrame and save

df = pd.DataFrame({'name': ['Alice','Bob'], 'score': [85,92]})
df.to_csv('sample_output.csv', index=False)
print(df)
