import pandas as pd
import numpy as np 
import os
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import seaborn
from sklearn.cluster import KMeans


path = os.getcwd()

fundamental = 'Revenue'
clusters = 3

quarterly_df = pd.read_excel(path+f'\\Excel_Sheets\\Quarterly_{fundamental}.xlsx')
quarterly_df.index = quarterly_df['Company']
quarterly_df.drop(['Company','Exchange', 'Market Cap 2018'], axis=1, inplace=True)
mask = quarterly_df.applymap(lambda x: isinstance(x, (int, float)))
quarterly_df = quarterly_df.where(mask)
quarterly_df = quarterly_df.dropna(how='any', axis=1)
quarterly_df = quarterly_df.T

# Initialize the k-means algorithm with 3 clusters
kmeans = KMeans(n_clusters=clusters)

# Fit the algorithm to the data
kmeans.fit(quarterly_df.T)

# Get the cluster labels for each data point
labels = kmeans.labels_

# Get the coordinates of the cluster centers
centers = kmeans.cluster_centers_

# Create a dictionary mapping the cluster label to a list of group members
cluster_dict = {}
for i, label in enumerate(labels):
    if label not in cluster_dict:
        cluster_dict[label] = []
    cluster_dict[label].append(quarterly_df.columns[i])

cluster_text = ''
# Print the members of each cluster
for label, members in cluster_dict.items():
    cluster = f"Cluster {label+1}:"
    print(cluster)
    cluster_text += cluster + '\n'
    for member in members:
        print(member)
        cluster_text += member +'\n'
    print()
    cluster_text += '\n'

output_file = open(f'{fundamental}_{clusters}_clusters.txt', 'w')

output_file.write(cluster_text)
output_file.close()

corr = quarterly_df.corr()

plt.figure(figsize=(16,9))
plt.tight_layout()
plt.subplots_adjust(bottom=0.3, left=0.2)
seaborn.heatmap(corr)  
plt.savefig(f'Graphs\Correlations\Sector_correlation_matrix_{fundamental}')
#plt.show()


print('Done')







 


 
