# Check and print lineups longer than 5, shorter than 4 or of uneven length

import pandas as pd
import pickle
import lusubspkl

def lubox_badlen(year, type = 'reg', games = 'ALL', periods = 'ALL', datapath = ''):
  # Open pickle of lusubs for specified type and year
  with open('{}lubox_{}_{}.pkl'.format(datapath, type, year), 'rb') as f:
    lupbp = pickle.load(f)
  f.close()
  # Create pandas dataframe for specified year, type, games and periods
  df = lusubspkl.create_dfseg(year, type, games, periods, datapath)
  
  for game in pd.unique(df['GAME_ID']):
    for period in pd.unique(df.loc[df['GAME_ID']==game, 'PERIOD']):
      for team in ['HOME', 'VIS']:
        badlen = 0
        unevenlen = 0
        if len(lupbp[year, type, game, period, 1, team, 'on']) not in [4,5]:
          badlen = 1
        for stint in pd.unique(df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period), 'STINT'])[1:]:
          if len(lupbp[year, type, game, period, stint, team, 'on']) != len(lupbp[year, type, game, period, stint-1, team, 'on']):
            unevenlen = 1
        if (badlen == 1) or (unevenlen == 1):
          print ''
          print year, game, team, 'q' + str(period)
          for stint in pd.unique(df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period), 'STINT']):
            print stint, len(lupbp[year, type, game, period, stint, team, 'on']), lupbp[year, type, game, period, stint, team, 'on'] 
          for p in pd.unique(df.loc[df['GAME_ID']==game, 'PERIOD']):
            print 'q' + str(p), 'len stint 1: ' + str(len(lupbp[year, type, game, p, 1, team, 'on']))

if __name__ == '__main__':
  
  years = range(2000, 2015)
  for year in years:
    print ''
    print ''
    print year
    lubox_badlen(year)