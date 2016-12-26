# Adds missing scores, and creates home and vis score columns

import pandas as pd

def pbp_addscore(year, type = 'reg', datapath = ''):
  #Create pandas dataframe for single year
  df = pd.read_csv('{}playbyplay_{}_{}_stint.csv'.format(datapath, type, year))
  df = df.drop(['Unnamed: 0', 'Unnamed: 0.1'], 1)
  
  #Create HOME_SCORE and VIS_SCORE variables
  df['HOME_SCORE'] = 0
  df['VIS_SCORE'] = 0
  
  #Adding missing scores to existing 'SCORE' variable, and then filling HOME_SCORE and VIS_SCORE columns
  for game in pd.unique(df['GAME_ID']): 
    print year, game
    df.loc[df[df['GAME_ID']==game].index[0], 'SCORE'] = '0 - 0'
    for i in df[df['GAME_ID']==game].index[1:]:
      if pd.isnull(df.loc[i, 'SCORE']):
        df.loc[i, 'SCORE'] = df.loc[i-1, 'SCORE']
        
      df.loc[i, 'HOME_SCORE'] = int(df.loc[i, 'SCORE'].split('-')[1])
      df.loc[i, 'VIS_SCORE'] = int(df.loc[i, 'SCORE'].split('-')[0])
      
  #Save to .csv
  df.to_csv('{}playbyplay_{}_{}_stsc.csv'.format(datapath, type, year))
  
  
if __name__ == '__main__':

  years = range(1996, 2015)
  for year in years:
    print year
    print ''
    pbp_addscore(year)