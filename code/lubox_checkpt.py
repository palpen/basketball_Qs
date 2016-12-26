#Calculates (total game) playing time from constructed lineups, compares to official box score playing time, and prints details if at least one player's playing time difference is above a threshold

import pandas as pd
import pickle
import lusubspkl
import requests

#Set threshold (in seconds)
thresh = 10 

def lubox_checkpt(year, type = 'reg', games = 'ALL', periods = 'ALL', datapath = ''):
  #open constructed lineups pickle, and create pandas dataframe using lusubspkl and pbp_stint csv
  with open('{}lubox_{}_{}.pkl'.format(datapath, type, year), 'rb') as f:
    lubox = pickle.load(f)
  f.close()
  df = lusubspkl.create_dfseg(year, type, games, periods, datapath)
  
  #Create variables for the max difference in minutes and the associated game, team and player
  maxdiff = 0
  maxdiffgame = 0
  maxdiffteam = 0
  maxdiffplayer = 0
  for game in pd.unique(df['GAME_ID']):
    #print maxdiff
    #get minutes from box score for each player
    season = str(year) + '-' + str(year+1)
    url = 'http://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=50000&GameID=00{}&RangeType=0&Season={}&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'.format(game, season)
    res = requests.get(url, headers={'USER-AGENT': 'u_a'})
    minb = {}
    for player in res.json()['resultSets'][0]['rowSet']:
      minb[player[4]] = 0
      if isinstance(player[8], unicode):
        minb[player[4]] = (60*int(player[8].split(':')[0])) + int(player[8].split(':')[1])
    
    for team in ['HOME', 'VIS']:
      #print game, team
      #check if gameXteam has lineups of bad length (length > 5) by checking the length of the last stint in each period (all 11 lineups of bad length have bad length in the final stint of the bad period)
      badlen = 0
      for period in pd.unique(df.loc[df['GAME_ID']==game, 'PERIOD']):
        if len(lubox[year, type, game, period, pd.unique(df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period), 'STINT'])[-1], team, 'on' ]) > 5:
          badlen = 1
      
      #Compare minutes in gameXteam if all stints are not of bad length    
      if badlen == 0:
        #Calculate minutes of players in constructed lineups
        minp = {}
        for period in pd.unique(df.loc[df['GAME_ID']==game, 'PERIOD']):
          for stint in pd.unique(df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period), 'STINT']):
            for player in lubox[year, type, game, period, stint, team, 'on']:
              if player in minp.keys():             
                minp[player] = minp[player] + df.loc[df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period) & (df['STINT']==stint)].index[0], 'STINT_TIME']      
              if player not in minp.keys():
                minp[player] = df.loc[df.loc[(df['GAME_ID']==game) & (df['PERIOD']==period) & (df['STINT']==stint)].index[0], 'STINT_TIME']
        
        #For each player, calulate the absolute value of difference between pbp and box minutes. If above threshold, print details. In some cases, player ids in play-by-play not in box score. Create exception, and print relevant details.
        abovethresh = 0
        exceptions = []
        try:
          for player in minp.keys():
            if abs(minp[player] - minb[player]) > thresh:
              abovethresh = 1
            if abs(minp[player] - minb[player]) > maxdiff:
              maxdiff = abs(minp[player] - minb[player])
              maxdiffgame = game
              maxdiffteam = team
              maxdiffplayer = player
          if abovethresh == 1:
            print ''
            print year, game, team
            for player in minp.keys():
              print player, 'box: ' + str(minb[player]), 'pbp: ' + str(minp[player]), 'diff: ' + str(abs(minb[player] - minp[player]))
        except KeyError:
          print ''
          print ''
          print 'Exception: ', year, game, team, 'p' + str(player)
          print ''
          exceptions.append(game)
       
  #Print maxdiff stuff
  print ''
  print 'MaxDiff:', year, maxdiffgame, maxdiffteam, maxdiffplayer
  print 'Exeption Game IDs: ', exceptions
  
  
if __name__ == '__main__':
  
  years = range(1996, 2008)
  for year in reversed(years):
    print ''
    print ''
    print ''
    print year
    lubox_checkpt(year)      