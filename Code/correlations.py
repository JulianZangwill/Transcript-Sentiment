import pandas as pd
import numpy as np 
import os
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

path = os.getcwd()

fundamental = 'Assets'

quarterly_df = pd.read_excel(path+f'\\Excel_Sheets\\Quarterly_{fundamental}.xlsx')
score_summary_df = pd.read_csv(path+'\\Dataframes\\No_Q_Lexicon_Scores_summary.csv')

#Clearning up dataframes
score_summary_df.set_index('Labels', inplace=True)
score_summary_df.columns = quarterly_df['Company']
score_summary_df = score_summary_df.T

quarterly_df.index = quarterly_df['Company']
quarterly_df.drop(['Company','Exchange', 'Market Cap 2018'], axis=1, inplace=True)

#Removes all non numbers from both dataframes
mask = score_summary_df.applymap(lambda x: isinstance(x, (int, float)))
score_summary_df = score_summary_df.where(mask)
mask = quarterly_df.applymap(lambda x: isinstance(x, (int, float)))
quarterly_df = quarterly_df.where(mask)

#Return calcultions from the first date
quarterly_change_df = (quarterly_df.sub(quarterly_df['2018 Q1'], axis = 0)).div(quarterly_df['2018 Q1'], axis=0)

#Plotting
title = f'Panel_Correlation_over_time_{fundamental}'
plt.figure(figsize=(16,9))
plt.subplots_adjust(hspace=0.6)
plt.suptitle(title)    

corr_df = pd.DataFrame(index=score_summary_df.columns, columns=quarterly_df.columns)
reg_df = pd.DataFrame(index=score_summary_df.columns, columns=quarterly_df.columns)

for n, column in enumerate(score_summary_df):
    for quarter in quarterly_change_df:
        x = np.array(score_summary_df[column])
        y = np.array(quarterly_change_df[quarter])
        joint1 = np.array([y,x], dtype=np.float64)
        joint = pd.DataFrame(joint1)
        joint = joint.dropna(how='any', axis=1)
        joint = np.array(joint)

        ##Scatter
        # plt.title(f'{fundamental},{column}, {quarter}')
        # plt.scatter(joint[1], joint[0])
        # plt.savefig(f'Graphs\\Scatter\\{fundamental}\\{column}_{quarter}')
        # plt.close()

        ##Correlation   
        #corr_df[quarter][column] = np.corrcoef(joint)[0,1]
        
        corr_df[quarter][column] = spearmanr(joint[0], joint[1])[0]
        

        ##Regression
        ones = np.ones_like(x)
        X = np.array([ones, x], dtype = np.float64).T
        Beta_OLS = (np.linalg.inv(X.T@X))@X.T@y
        reg_df[quarter][column] = Beta_OLS[1]
        


    ax = plt.subplot(3,3,n+1)
    corr_df[corr_df.index == column].T.plot.bar(ax=ax, color='b', width=0.1,ylim=(-1,1),rot = 45)
    ax.set_title(column)
    ax.get_legend().remove()
    ax.grid(True)
    
plt.savefig(f'Graphs\Correlations\Spearman_No_Q_Lexicon_{title}')
plt.show()
print('Done')
