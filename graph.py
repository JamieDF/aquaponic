#Load in the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
def createGraph():
    # Load in the data
    df = pd.read_csv('data.csv')
    print(df)
    try:
       os.remove("graph.png")
    except Exception as e:
       print(e)
       pass
    #check the head
    df.head()
    df['time'] = pd.to_datetime(df.time)
    print(df['waterTemperature'].mean())
    print(df['temperature'].mean())


    ax = sns.lineplot(x='time', y='value',hue="variable", data=pd.melt(df, ['time'], ["temperature", "waterTemperature"]))
    ax.set(ylim=(10, 30))
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:3], labels[:3])
    plt.savefig("graph.png")
    print("Graph created")
    return round(df['waterTemperature'].mean(),1), round(df['temperature'].mean(),1)
