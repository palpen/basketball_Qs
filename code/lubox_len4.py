# Check and print lineups longer than 5, shorter than 4 or of uneven length

import pandas as pd
import pickle
import lusubspkl

def lubox_len4(year, type = 'reg', games = 'ALL', periods = 'ALL', datapath = ''):
  # Open pickle of lusubs for specified type and year
  with open('{}lubox_{}_{}.pkl'.format(datapath, type, year), 'rb') as f:
    lupbp = pickle.load(f)
  f.close()
  # Create pandas dataframe for specified year, type, games and periods
  df = lusubspkl.create_dfseg(year, type, games, periods, datapath)
  
  for game in pd.unique(df['GAME_ID']):
    for team in ['HOME', 'VIS']:
      for period in pd.unique(df.loc[df['GAME_ID']==game, 'PERIOD']):
        if len(lupbp[year, type, game, period, 1, team, 'on']) == 4:
          print ''
          print year, game, team, 'q' + str(period)
          for stint in pd.unique(df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period), 'STINT']):
            print stint, len(lupbp[year, type, game, period, stint, team, 'on']), lupbp[year, type, game, period, stint, team, 'on']


if __name__ == '__main__':
  
  years = [1996, 1998, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014]
  for year in years:
    print ''
    print ''
    print year
    lubox_len4(year)