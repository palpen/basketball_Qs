#Checks play-by-play for reverse scores

import pandas as pd

def pbp_checkscore(year, type = 'reg', datapath = ''):
  #Create pandas dataframe for single year
  df = pd.read_csv('{}playbyplay_{}_{}_stint.csv'.format(datapath, type, year))
  df = df.drop(['Unnamed: 0', 'Unnamed: 0.1'], 1)
  
  for game in pd.unique(df['GAME_ID']):
    if int(df.loc[df[(df['GAME_ID']==game) & (df['PERIOD']==1) & (pd.notnull(df['SCORE']))].index[-1], 'SCORE'].split('-')[0]) > int(df.loc[df[(df['GAME_ID']==game) & (df['PERIOD']==3) & (pd.notnull(df['SCORE']))].index[-1], 'SCORE'].split('-')[0]):
      print year, game
  
  
if __name__ == '__main__':

  years = range(1996, 2015)
  for year in years:
    print ''
    print year
    pbp_checkscore(year)