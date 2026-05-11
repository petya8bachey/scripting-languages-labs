import pandas as pd
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
df = pd.read_csv(url)

print(df.head())

plt.scatter(df['sepal_length'], df['sepal_width'], c=df['species'].astype('category').cat.codes)
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Sepal Width (cm)')
plt.title('Iris: Sepal Dimensions')
plt.grid(True, alpha=0.3)
plt.show()