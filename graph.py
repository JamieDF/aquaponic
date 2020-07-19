#Load in the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def createGraph():
    # Load in the data
    df = pd.read_csv('data.csv')
    print(df)
    #check the head
    df.head()
    df['time'] = pd.to_datetime(df.time)
    print(df['waterTemperature'].mean())
    print(df['airTemperature'].mean())


    ax = sns.lineplot(x='time', y='value', hue='variable', 
                data=pd.melt(df, ['time'], ["airTemperature", "waterTemperature"]))

    ax.set(ylim=(10, 30))
    plt.savefig("graph.png")
    print("Graph created")