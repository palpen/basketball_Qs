import pandas as pd

def pbp_idstint(year, type = 'reg', datapath = ''):
  # Create pandas dataframe for specified year, type, games and periods 
  df = pd.read_csv('{}playbyplay_{}_{}.csv'.format(datapath, type, year))
  # Create variables for team ids, stint number, and stint length
  df['HOME_ID'] = 0
  df['VIS_ID'] = 0
  df['STINT'] = 0
  df['STINT_TIME'] = 0
  
  # Get team ids
  for game in pd.unique(df['GAME_ID']):
    print 'team id', year, game
    for team in ['HOME', 'VIS']:
      if team == 'VIS':
        df.loc[df['GAME_ID']==game, team + '_ID'] = pd.unique(df.loc[(df['VISITORDESCRIPTION'].notnull()) & (df['EVENTMSGTYPE']==1) & (df['GAME_ID']==game), 'PLAYER1_TEAM_ID'])[0] 
      else:
        df.loc[df['GAME_ID']==game, team + '_ID'] = pd.unique(df.loc[(df[team + 'DESCRIPTION'].notnull()) & (df['EVENTMSGTYPE']==1) & (df['GAME_ID']==game), 'PLAYER1_TEAM_ID'])[0]
        
  # Get stint numbers - adjusted from old to account for change in game clock
  for game in pd.unique(df['GAME_ID']):
    print 'stint', year, game
    for period in pd.unique(df.loc[df['GAME_ID']==game, 'PERIOD']):
      df.loc[df[(df['GAME_ID']==game) & (df['PERIOD']==period)].index[0], 'STINT'] = 1
      for i in df[(df['GAME_ID']==game) & (df['PERIOD']==period)].index[1:]:
        if df.loc[i, 'EVENTMSGTYPE'] == 8 and ((df.loc[i-1, 'EVENTMSGTYPE'] != 8) or (df.loc[i, 'PCTIMESTRING'] != df.loc[i-1, 'PCTIMESTRING'])):
          df.loc[i, 'STINT'] = df.loc[i-1, 'STINT'] + 1
        else:
          df.loc[i, 'STINT'] = df.loc[i-1, 'STINT']
          
  # Get length of stint
  for game in pd.unique(df['GAME_ID']):
    print 'stint time', year, game
    for period in pd.unique(df.loc[df['GAME_ID']==game, 'PERIOD']):
      for stint in pd.unique(df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period), 'STINT']):
        if stint == pd.unique(df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period), 'STINT'])[-1]:
          df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period) & (df['STINT']==stint), 'STINT_TIME'] = (60*int(df.loc[df[(df['GAME_ID']==game) & (df['PERIOD']==period) & (df['STINT']==stint)].index[0], 'PCTIMESTRING'].split(':')[0])) + int(df.loc[df[(df['GAME_ID']==game) & (df['PERIOD']==period) & (df['STINT']==stint)].index[0], 'PCTIMESTRING'].split(':')[1]) 
        else:
          df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period) & (df['STINT']==stint), 'STINT_TIME'] = ((60*int(df.loc[df[(df['GAME_ID']==game) & (df['PERIOD']==period) & (df['STINT']==stint)].index[0], 'PCTIMESTRING'].split(':')[0])) + int(df.loc[df[(df['GAME_ID']==game) & (df['PERIOD']==period) & (df['STINT']==stint)].index[0], 'PCTIMESTRING'].split(':')[1])) - ((60*int(df.loc[df[(df['GAME_ID']==game) & (df['PERIOD']==period) & (df['STINT']==stint+1)].index[0], 'PCTIMESTRING'].split(':')[0])) + int(df.loc[df[(df['GAME_ID']==game) & (df['PERIOD']==period) & (df['STINT']==stint+1)].index[0], 'PCTIMESTRING'].split(':')[1]))
  
  # Save to .csv
  df.to_csv('{}playbyplay_{}_{}_stint.csv'.format(datapath, type, year))  
  
  
if __name__ == '__main__':

  years = range(1996, 2015)
  for year in years:
    pbp_idstint(year)