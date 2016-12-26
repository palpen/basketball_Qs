import pandas as pd
import pickle
import lusubspkl
import requests
import json

# Loads lineups from pbp, then adds player to 4-man lineups whose calculated minutes are less than box score minutes
def lubox(year, type = 'reg', games = 'ALL', periods = 'ALL', datapath = ''):
  # Open pickle of lusubs for specified type and year
  with open('{}lupbp_{}_{}.pkl'.format(datapath, type, year), 'rb') as f:
    lubox = pickle.load(f)
  f.close()
  # Create pandas dataframe for specified year, type, games and periods
  df = lusubspkl.create_dfseg(year, type, games, periods, datapath)

  for game in pd.unique(df['GAME_ID']):
    for team in ['HOME', 'VIS']:
      teamid = team + '_ID'
      linew4 = 0
      for period in pd.unique(df.loc[df['GAME_ID']==game, 'PERIOD']):
        if len(lubox[year, type, game, period, 1, team, 'on']) == 4:
          linew4 = 1
      if linew4 ==1:
        print game
        hminp = {}
        for period in pd.unique(df.loc[df['GAME_ID']==game, 'PERIOD']):
          for stint in pd.unique(df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period), 'STINT']):
            for player in lubox[year, type, game, period, stint, team, 'on']:
              if player in hminp.keys():             
                hminp[player] = hminp[player] + df.loc[df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period) & (df['STINT']==stint)].index[0], 'STINT_TIME']      
              if player not in hminp.keys():
                hminp[player] = df.loc[df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period) & (df['STINT']==stint)].index[0], 'STINT_TIME']
        
        with open('{}_{}'.format(year, game), 'r') as f:
          res = json.load(f)
        f.close()
        hminb = {}
        for player in res['resultSets'][0]['rowSet']:
          if isinstance(player[8], unicode):
            hminb[player[4]] = (60*int(player[8].split(':')[0])) + int(player[8].split(':')[1])
            
        hmindiff = {}
        for player in hminp.keys():
          hmindiff[player] = hminb[player] - hminp[player]
          
        for period in pd.unique(df.loc[df['GAME_ID']==game, 'PERIOD']):
          if len(lubox[year, type, game, period, 1, team, 'on']) == 4:
            for stint in pd.unique(df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period), 'STINT']):
              for player in hmindiff.keys():
                if (hmindiff[player] > 200) & (player not in lubox[year, type, game, period, stint, team, 'list']):
                  lubox[year, type, game, period, stint, team, 'on'].append(player)
                  lubox[year, type, game, period, stint, team, 'on'].sort()
                  lubox[year, type, game, period, stint, team, 'list'].append(player)
                  lubox[year, type, game, period, stint, team, 'list'].sort()
                  
  with open('{}lubox_{}_{}.pkl'.format(datapath, type, year), 'wb') as f:
    pickle.dump(lubox, f, pickle.HIGHEST_PROTOCOL)    
  f.close()
  
  
if __name__ == '__main__':
  
  years = range(2000, 2015)
  for year in years:
    print year
    lubox(year)      