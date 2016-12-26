# Code to check that home and vis team ids are different

import pandas as pd

years = range(1996,2015)
for year in years:
  print year
  df = pd.read_csv('playbyplay_reg_{}_stint.csv'.format(year))
  for game in pd.unique(df['GAME_ID']):
    if df.loc[df[df['GAME_ID']==game].index[0], 'HOME_ID'] == df.loc[df[df['GAME_ID']==game].index[0], 'VIS_ID']:
      print year, game
  print ''
  print ''  