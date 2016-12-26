import pandas as pd

years = range(1996,2015)
for year in years:
  df = pd.read_csv('playbyplay' + str(year) + 'seg.csv')
  df = df.drop('Unnamed: 0', 1)
  
  games = pd.unique(df.GAME_ID.ravel())
  for game in games:
    dfg = df[df['GAME_ID'] == game]
    
    quarters = pd.unique(dfg.PERIOD.ravel())
    for quarter in quarters:
      dfp = dfg[dfg['PERIOD'] == quarter]
      
      startseg = dfp.loc[dfp.index[0], 'SEGMENT']
      minseg = min(pd.unique(dfp.SEGMENT.ravel()))
      if (startseg != 1) or (minseg != 1):
        print year, game, quarter, 'start: ' + str(startseg), 'min: ' + str(minseg)