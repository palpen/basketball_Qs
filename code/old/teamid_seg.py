#Script to (1) set home and visitor team ids, (2) break down each quarter into segments/stints between substitutions, and (3) calculate the length in seconds of these stints/segments

import pandas as pd 

years = [1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2011]

# Find home and visitor team ids
for year in years:
  #Create variables for home and visitor ids, segment/stint number, and segment/stint time
  df = pd.read_csv('playbyplay' + str(year) + '.csv')
  df = df.drop('Unnamed: 0', 1)
  df['HOME_ID'] = 0
  df['VIS_ID'] = 0
  df['SEGMENT'] = 0
  df['SEGMENT_TIME'] = 0

  games = pd.unique(df.GAME_ID.ravel())
  #Look at the made shots -- which only contain player ids for the team making the shot -- to get the home and visitor team ids
  for game in games:
    dfhome = df.loc[(df.HOMEDESCRIPTION.notnull()) & (df.EVENTMSGTYPE==1) & (df.GAME_ID==game)]
    homeid = pd.unique(dfhome.PLAYER1_TEAM_ID.ravel())[0]
    df.loc[df.GAME_ID == game, 'HOME_ID'] = homeid
    
    dfvis = df.loc[(df.VISITORDESCRIPTION.notnull()) & (df.EVENTMSGTYPE==1) & (df.GAME_ID==game)]
    visid = pd.unique(dfvis.PLAYER1_TEAM_ID.ravel())[0]
    df.loc[df.GAME_ID == game, 'VIS_ID'] = visid
    print year, game, 'team id'
  df.to_csv('playbyplay' + str(year) + 'seg.csv') 

#Code for segments/stints: Set the first observation to 1 -- Note: in some games, some quarters don't start with a 12, so this code should be altered; For all subsequent rows in the data, if the eventmessage type is a substitution, and the previous row is not, segment number increases by 1  
for year in years:
  
  df = pd.read_csv('playbyplay' + str(year) + 'seg.csv')
  df = df.drop('Unnamed: 0', 1)
  
  games = pd.unique(df.GAME_ID.ravel())
  for game in games:
    dfg = df.loc[df.GAME_ID == game]    
    quarters = pd.unique(dfg.PERIOD.ravel())
    for quarter in quarters:
      dfq = dfg.loc[dfg.PERIOD == quarter]
      ind = dfq.index 
      df.loc[ind[0], 'SEGMENT'] = 1
      for i in ind[1:]:    
        if df.loc[i, 'EVENTMSGTYPE'] == 8 and df.loc[i-1, 'EVENTMSGTYPE'] != 8:
          df.loc[i, 'SEGMENT'] = df.loc[i-1, 'SEGMENT'] + 1
        else:
          df.loc[i, 'SEGMENT'] = df.loc[i-1, 'SEGMENT']
    print year, game, 'segments' 
  df.to_csv('playbyplay' + str(year) + 'seg.csv')

#To get length of segment/stint, subtract the starting time from the next segment from the starting time of the current segment, with consideration for the segment being the last in the quarter.
for year in years:  

  df = pd.read_csv('playbyplay' + str(year) + 'seg.csv')
  df = df.drop('Unnamed: 0', 1)
  
  games = pd.unique(df.GAME_ID.ravel())  
  for game in games:
    dfg = df.loc[df.GAME_ID == game]    
    quarters = pd.unique(dfg.PERIOD.ravel())
    for quarter in quarters:
      dfq = dfg.loc[dfg.PERIOD == quarter]
      segments = pd.unique(dfq.SEGMENT.ravel())
      for segment in segments:
        dfs = dfq.loc[dfq.SEGMENT == segment]
        secstarts = (60*int(df.loc[dfs.index[0], 'PCTIMESTRING'].split(':')[0])) + int(df.loc[dfs.index[0], 'PCTIMESTRING'].split(':')[1])
        if segment == segments[-1]:
          secends = 0
        else:
          dfe = dfq.loc[dfq.SEGMENT == segment+1]
          secends = (60*int(df.loc[dfe.index[0], 'PCTIMESTRING'].split(':')[0])) + int(df.loc[dfe.index[0], 'PCTIMESTRING'].split(':')[1])
                  
        seconds = secstarts - secends
        df.loc[(df.GAME_ID==game) & (df.PERIOD==quarter) & (df.SEGMENT==segment), 'SEGMENT_TIME'] = seconds
    print year, game, 'segment time'  
  df.to_csv('playbyplay' + str(year) + 'seg.csv')
