import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(r'data/cities.csv')
plt.rcdefaults()
cols = df.columns
df.columns = [s.lower().replace(' ', '_') for s in cols]
df.head()
plt.style.use('dark_background')

cols = ['max_temp', 'humidity', 'cloudiness', 'wind_speed']
titles = ['Max Temp', 'Humidity', 'Cloudiness', 'Wind Speed']

for col, title in zip(cols, titles):
    fig, ax = plt.subplots(figsize=(10, 7))

    fig = sns.scatterplot(
        x=df['lat'],
        y=df[col],
        color='#FF007F',
        alpha=0.8
    )

    plt.xlabel('Latitude', fontdict={'fontsize': 10})

    plt.ylabel(title, fontdict={'fontsize': 10})

    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)

    plt.title(f'{title} vs Latitude')
    plt.tight_layout()

    plt.savefig(f'{col}_vs_lat.svg')
