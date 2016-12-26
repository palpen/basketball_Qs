# Check and print lineups longer than 5, shorter than 4 or of uneven length

import pandas as pd
import pickle
import lusubspkl

def lupbp_mult4(year, type = 'reg', games = 'ALL', periods = 'ALL', datapath = ''):
  # Open pickle of lusubs for specified type and year
  with open('{}lupbp_{}_{}.pkl'.format(datapath, type, year), 'rb') as f:
    lupbp = pickle.load(f)
  f.close()
  # Create pandas dataframe for specified year, type, games and periods
  df = lusubspkl.create_dfseg(year, type, games, periods, datapath)
  
  for game in pd.unique(df['GAME_ID']):
    for team in ['HOME', 'VIS']:
      count4 = 0
      for period in pd.unique(df.loc[df['GAME_ID']==game, 'PERIOD']):
        if len(lupbp[year, type, game, period, 1, team, 'on']) == 4:
          count4 = count4 + 1
      if count4 > 1:
        print ''
        print year, game, team
        for p in pd.unique(df.loc[df['GAME_ID']==game, 'PERIOD']):
          print 'q' + str(p), 'len stint 1: ' + str(len(lupbp[year, type, game, p, 1, team, 'on']))


if __name__ == '__main__':
  
  years = range(1996, 2015)
  for year in years:
    print ''
    print ''
    print year
    lupbp_mult4(year)