import pandas as pd
import pickle

years = range(1996,2015)

for year in years:
  df = pd.read_csv('playbyplay_reg_{}_seg.csv'.format(year))
  with open('lupbp_reg_{}.pkl'.format(year), 'rb') as f:
    lu = pickle.load(f)
  f.close()
  
  for game in pd.unique(df['GAME_ID']):
    for period in pd.unique(df.loc[df['GAME_ID']==game, 'PERIOD']):
      for team in ['HOME', 'VIS']:
        lencheck = 0
        for segment in pd.unique(df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period), 'SEGMENT']):
          if len(lu[year, 'reg', game, period, segment, team, 'on']) != 5:
            lencheck = 1            
        if lencheck == 1:
          print year, game, team, 'q' + str(period)
          for segment in pd.unique(df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period), 'SEGMENT']):
            print segment, len(lu[year, 'reg', game, period, segment, team, 'on']), lu[year, 'reg', game, period, segment, team, 'on']
          print ''
          print ''