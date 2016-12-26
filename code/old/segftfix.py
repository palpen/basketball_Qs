#Code to change segment/stint number of free throws to the segment containing the lineup on-court when corresponding foul occurred (both technical and personal fouls). 

import pandas as pd 

years = [2014]
for year in years:
  df = pd.read_csv('playbyplay' + str(year) + 'line.csv')
  df['SEGMENT_FT'] = df['SEGMENT']
  df['SEGMENT_DIFF'] = 0
  df['INDEX_DIFF'] = 0
  
  games = pd.unique(df.GAME_ID.ravel()).tolist()
  for game in games:
    dfft = df[(df['GAME_ID'] == game) & (df['EVENTMSGTYPE'] == 3)]
    for i in dfft.index:
      #correct segment number for technical free throws
      if df.loc[i, 'EVENTMSGACTIONTYPE'] in [16,21]:
        foulind = max(df[(df['GAME_ID'] == game) & (df.index < i) & (df['EVENTMSGTYPE'] == 6) & (df['EVENTMSGACTIONTYPE'].isin([11,12,13,17,18,19,25,30]))].index)
        df.loc[i, 'SEGMENT_FT'] = df.loc[foulind, 'SEGMENT']
        df.loc[i, 'SEGMENT_DIFF'] = df.loc[i, 'SEGMENT'] - df.loc[i, 'SEGMENT_FT']
        df.loc[i, 'INDEX_DIFF'] = i - foulind
      #correct segment number for other free throws  
      if df.loc[i, 'EVENTMSGACTIONTYPE'] not in [16,21]:
        foulind = max(df[(df['GAME_ID'] == game) & (df.index < i) & (df['EVENTMSGTYPE'] == 6) & (df['EVENTMSGACTIONTYPE'].isin([1,2,3,5,6,7,8,9,14,15,27,28,29]))].index)
        df.loc[i, 'SEGMENT_FT'] = df.loc[foulind, 'SEGMENT']
        df.loc[i, 'SEGMENT_DIFF'] = df.loc[i, 'SEGMENT'] - df.loc[i, 'SEGMENT_FT']
        df.loc[i, 'INDEX_DIFF'] = i - foulind
        
  df.to_csv('playbyplay' + str(year) + 'lineft.csv')