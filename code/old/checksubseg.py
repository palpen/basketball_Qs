import pandas as pd

years = range(1996, 2015)

for year in years:
  df = pd.read_csv('playbyplay_reg_{}_seg.csv'.format(year))
  df = df[df['EVENTMSGTYPE']==8]
  
  for game in pd.unique(df['GAME_ID']):
    for period in pd.unique(df.loc[df['GAME_ID']==game, 'PERIOD']):
      for segment in pd.unique(df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period), 'SEGMENT']):
        check = 0
        if len(df[(df['GAME_ID']==game) & (df['PERIOD']==period) & (df['SEGMENT']==segment)].index) > 1:
          for i in df[(df['GAME_ID']==game) & (df['PERIOD']==period) & (df['SEGMENT']==segment)].index[1:]:
            if df.loc[i, 'PCTIMESTRING'] != df.loc[i-1, 'PCTIMESTRING']:
              check = 1
        if check ==1:
          print year, game, period, segment
          print ''
          print ''