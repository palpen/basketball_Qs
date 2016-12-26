import pandas as pd
import pickle

# Returns a pandas dataframe 
def create_dfseg(year, type = 'reg', games = 'ALL', periods = 'ALL', datapath = ''):
  df = pd.read_csv('{}playbyplay_{}_{}_stint.csv'.format(datapath, type, year))
  df = df.drop(['Unnamed: 0', 'Unnamed: 0.1'], 1)
  if games != 'ALL':
    df = df[df['GAME_ID'].isin(games)]
  if periods != 'ALL':
    df = df[df['PERIOD'].isin(periods)]
  return df

# Saves lineups from substitutions -- on, quarter off, quarter list -- for home and away teams for each stint  
def lusubs(year, type = 'reg', games = 'ALL', periods = 'ALL', datapath = ''):
  # Use create_dfseg function to create dataframe, and create dictionary to hold lineups
  df = create_dfseg(year, type, games, periods, datapath)
  lusubs = {}
  lusubs['format'] = '[year, type: reg/po/pre, game, period, stint, team: HOME/VIS, lineup: on/off/list]'
  # Nested loops to create empty lists for lineups and to iterate through the substitution rows in play-by-play
  for game in pd.unique(df['GAME_ID']):
    print year, game
    for period in pd.unique(df.loc[df['GAME_ID']==game, 'PERIOD']):
      for stint in pd.unique(df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period), 'STINT']):
        for team in ['HOME', 'VIS']:
          for lineup in ['on', 'off', 'list']:
            lusubs[year, type, game, period, stint, team, lineup] = []          
      # First place players subbing on and off in associated 'on' and 'off' lists -- with correction if players are subbed both on and off in a stint. Second, add those players to opposite list in previous stints if those players aren;t already in either the associated stint's 'on' or 'off' list
      for stint in pd.unique(df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period), 'STINT'])[1:]:
        for team in ['HOME', 'VIS']:
          for i in df[(df['GAME_ID']==game) & (df['PERIOD']==period) & (df['STINT']==stint) & (df['EVENTMSGTYPE']==8)].index:
            if df.loc[i, 'PLAYER1_TEAM_ID'] == df.loc[i, team + '_ID']:
              lusubs[year, type, game, period, stint, team, 'on'].append(df.loc[i, 'PLAYER2_ID'])
              lusubs[year, type, game, period, stint, team, 'off'].append(df.loc[i, 'PLAYER1_ID'])
              if df.loc[i, 'PLAYER2_ID'] in lusubs[year, type, game, period, stint, team, 'off']:
                lusubs[year, type, game, period, stint, team, 'off'].remove(df.loc[i, 'PLAYER2_ID'])
              if df.loc[i, 'PLAYER1_ID'] in lusubs[year, type, game, period, stint, team, 'on']:
                lusubs[year, type, game, period, stint, team, 'on'].remove(df.loc[i, 'PLAYER1_ID'])
              for t in range(pd.unique(df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period), 'STINT'])[0], stint):
                if (df.loc[i, 'PLAYER2_ID'] not in lusubs[year, type, game, period, t, team, 'on']) & (df.loc[i, 'PLAYER2_ID'] not in lusubs[year, type, game, period, t, team, 'off']):
                  lusubs[year, type, game, period, t, team, 'off'].append(df.loc[i, 'PLAYER2_ID'])
                if (df.loc[i, 'PLAYER1_ID'] not in lusubs[year, type, game, period, t, team, 'off']) & (df.loc[i, 'PLAYER1_ID'] not in lusubs[year, type, game, period, t, team, 'on']):
                  lusubs[year, type, game, period, t, team, 'on'].append(df.loc[i, 'PLAYER1_ID'])
          
          # Add players from previous 'on' and 'off' lists to current 'on' and 'off' lists if not already in an 'on' or 'off' list 
          for lineup in ['on', 'off']:
            for player in lusubs[year, type, game, period, stint-1, team, lineup]:
              if (player not in lusubs[year, type, game, period, stint, team, 'on']) & (player not in lusubs[year, type, game, period, stint, team, 'off']):
                lusubs[year, type, game, period, stint, team, lineup].append(player)
  
      # Sorting 'on' and 'off' lists, and adding 'list' list (which contains the list of players who were subbed on and/or off in a quarter -- should be the same for every stint in a quarter)
      for stint in pd.unique(df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period), 'STINT']):
        for team in ['HOME', 'VIS']:
          lusubs[year, type, game, period, stint, team, 'on'].sort()
          lusubs[year, type, game, period, stint, team, 'off'].sort()
          
          lusubs[year, type, game, period, stint, team, 'list'].extend(lusubs[year, type, game, period, stint, team, 'on'])
          lusubs[year, type, game, period, stint, team, 'list'].extend(lusubs[year, type, game, period, stint, team, 'off'])
          lusubs[year, type, game, period, stint, team, 'list'].sort()
 
  with open('{}lusubs_{}_{}.pkl'.format(datapath, type, year), 'wb') as f:
    pickle.dump(lusubs, f, pickle.HIGHEST_PROTOCOL)
    
  f.close()
  
    
if __name__ == '__main__':

  years = range(1996, 2015)
  for year in years:
    print year
    lusubs(year)