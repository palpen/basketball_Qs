import pandas as pd
import pickle
import lusubspkl

# Loads lineups from subs, then adds other players from play-by-play, and saves as pickle
def lupbp(year, type = 'reg', games = 'ALL', periods = 'ALL', datapath = ''):
  # Open pickle of lusubs for specified type and year
  with open('{}lusubs_{}_{}.pkl'.format(datapath, type, year), 'rb') as f:
    lupbp = pickle.load(f)
  f.close()
  # Create pandas dataframe for specified year, type, games and periods
  df = lusubspkl.create_dfseg(year, type, games, periods, datapath)
  # Create vector of eventmsgactiontype for (technical) fouls that can be credited to players on bench, and removing rows with ejections, timeouts, substitutions and technical fouls (all of which can be credited to players off court)
  foulexc = [10,11,16,19,25]
  df = df[(df['EVENTMSGTYPE'] != 9) & (df['EVENTMSGTYPE'] != 11) & ((df['EVENTMSGTYPE'] != 6) | (~df['EVENTMSGACTIONTYPE'].isin(foulexc)))]
  # Addinng players in pbp but not in subs to each associated lineup
  for game in pd.unique(df['GAME_ID']):
    for period in pd.unique(df.loc[df['GAME_ID']==game, 'PERIOD']):
      print game, period
      for stint in pd.unique(df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period), 'STINT']):
        for team in ['HOME', 'VIS']:
          for number in range(1,4):
            for player in pd.unique(df.loc[(df['GAME_ID'] == game) & (df['PERIOD'] == period) & (df['PLAYER{}_TEAM_ID'.format(number)] == df['{}_ID'.format(team)]), 'PLAYER{}_ID'.format(number)]):
              if (player not in lupbp[year, type, game, period, stint, team, 'list']) & (player != 0):
                lupbp[year, type, game, period, stint, team, 'on'].append(player)
                lupbp[year, type, game, period, stint, team, 'list'].append(player)
          # Sorting 'on' and 'list' lists      
          lupbp[year, type, game, period, stint, team, 'on'].sort() 
          lupbp[year, type, game, period, stint, team, 'list'].sort()
  # Saving pbp lineups as pickle        
  with open('{}lupbp_{}_{}.pkl'.format(datapath, type, year), 'wb') as f:
    pickle.dump(lupbp, f, pickle.HIGHEST_PROTOCOL)    
  f.close()
  
  
if __name__ == '__main__':
  
  years = range(1996, 2015)
  for year in years:
    print year
    lupbp(year)  