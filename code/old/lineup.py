#Three part code to get lineups from play-by-play: First, fill on-court and off-court lists for each segment in a quarter using substitutions within a quarter. Second, add players in the play-by-play who aren't subsituted to each lineup in the quarter. Last, for lineups with fewer than five players, calculate play time for each player from the existing lineups, and compare to the box score minutes. Ass the player(s) missing minutes top the appropriate lineups.
import pandas as pd 
import requests

years = [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2012, 2013, 2014]
for year in years:
  df = pd.read_csv('C:/Users/TICCamp/Desktop/NBA/PlaybyPlay/db/playbyplay' + str(year) + 'seg.csv')
  df = df.drop('Unnamed: 0', 1)
  #Create variables in DB for each player on the home and visiting team. Also create dummy variables for lineups with fewer than 5 players prior to checking box score and variables for lineups with more than five players prior to checking box score (6+ player lineups omitted for now)
  for i in range(1,6):
    df['H_PLAYER_' + str(i)] = 0
  for i in range(1,6):
    df['V_PLAYER_' + str(i)] = 0
  df['H_FOURP_BOXE'] = 0
  df['V_FOURP_BOXE'] = 0
  df['H_EXTRAP_MISSINGSUB'] = 0
  df['V_EXTRAP_MISSINGSUB'] = 0

  games = pd.unique(df.GAME_ID.ravel()).tolist()
  for game in games:
    dfg = df.loc[df.GAME_ID == game]
    homelineup = {}
    vislineup = {}
    quarters = pd.unique(dfg.PERIOD.ravel()).tolist()
    for quarter in quarters:
      dfa = dfg.loc[df.PERIOD == quarter]
      homelineup[str(quarter)] = {}
      vislineup[str(quarter)] = {}
      
      segments = pd.unique(dfa.SEGMENT.ravel()).tolist()
      dfsub = dfa.loc[dfa.EVENTMSGTYPE == 8]
      
      #Create dictionaries that hold on- and off-court lists for each teamXsegment 
      onoffhome = {}
      onoffvis = {}
      for segment in segments:
        onoffhome[str(segment)] = {}
        onoffvis[str(segment)] = {}
        onoffhome[str(segment)]['on'] = []
        onoffhome[str(segment)]['off'] = []
        onoffvis[str(segment)]['on'] = []
        onoffvis[str(segment)]['off'] = []

      #Start at the subs to start the second segment, then move sequentially through subs. Add players being subbed on to current on-court list and players being subbed off to current off-court list. Then, add those players to the opposite lists for all previous segments for which those players are in neither list. Finally, add players from only the one previous segments's on- and off-court lists to the same lists for the current segment, provided they aren't already in a list.  
      for segment in segments[1:]:  
        dfseg = dfsub.loc[dfsub.SEGMENT == segment]
        ind = dfseg.index
        for i in ind:
          if dfseg.loc[i, 'PLAYER1_TEAM_ID'] == dfseg.loc[i, 'HOME_ID']:
            onoffhome[str(segment)]['on'].append(dfseg.loc[i, 'PLAYER2_ID'])
            onoffhome[str(segment)]['off'].append(dfseg.loc[i, 'PLAYER1_ID'])
            if dfseg.loc[i, 'PLAYER2_ID'] in onoffhome[str(segment)]['off']:
              onoffhome[str(segment)]['off'].remove(dfseg.loc[i, 'PLAYER2_ID'])
            if dfseg.loc[i, 'PLAYER1_ID'] in onoffhome[str(segment)]['on']:
              onoffhome[str(segment)]['on'].remove(dfseg.loc[i, 'PLAYER1_ID'])
            for t in segments[:segments.index(segment)]:
              if (dfseg.loc[i, 'PLAYER2_ID'] not in onoffhome[str(t)]['on']) & (dfseg.loc[i, 'PLAYER2_ID'] not in onoffhome[str(t)]['off']):
                onoffhome[str(t)]['off'].append(dfseg.loc[i, 'PLAYER2_ID'])
              if (dfseg.loc[i, 'PLAYER1_ID'] not in onoffhome[str(t)]['off']) & (dfseg.loc[i, 'PLAYER1_ID'] not in onoffhome[str(t)]['on']):
                onoffhome[str(t)]['on'].append(dfseg.loc[i, 'PLAYER1_ID'])     
            
          if dfseg.loc[i, 'PLAYER1_TEAM_ID'] == dfseg.loc[i, 'VIS_ID']:
            onoffvis[str(segment)]['on'].append(dfseg.loc[i, 'PLAYER2_ID'])
            onoffvis[str(segment)]['off'].append(dfseg.loc[i, 'PLAYER1_ID'])
            if dfseg.loc[i, 'PLAYER2_ID'] in onoffvis[str(segment)]['off']:
              onoffvis[str(segment)]['off'].remove(dfseg.loc[i, 'PLAYER2_ID'])
            if dfseg.loc[i, 'PLAYER1_ID'] in onoffvis[str(segment)]['on']:
              onoffvis[str(segment)]['on'].remove(dfseg.loc[i, 'PLAYER1_ID'])
            for t in segments[:segments.index(segment)]:
              if (dfseg.loc[i, 'PLAYER2_ID'] not in onoffvis[str(t)]['on']) & (dfseg.loc[i, 'PLAYER2_ID'] not in onoffvis[str(t)]['off']):
                onoffvis[str(t)]['off'].append(dfseg.loc[i, 'PLAYER2_ID'])
              if (dfseg.loc[i, 'PLAYER1_ID'] not in onoffvis[str(t)]['off']) & (dfseg.loc[i, 'PLAYER1_ID'] not in onoffvis[str(t)]['on']):
                onoffvis[str(t)]['on'].append(dfseg.loc[i, 'PLAYER1_ID'])
       
        for player in onoffhome[str(segment - 1)]['on']:
          if (player not in onoffhome[str(segment)]['off']) & (player not in onoffhome[str(segment)]['on']):
            onoffhome[str(segment)]['on'].append(player)
        for player in onoffhome[str(segment - 1)]['off']:
          if (player not in onoffhome[str(segment)]['on']) & (player not in onoffhome[str(segment)]['off']):
            onoffhome[str(segment)]['off'].append(player)
            
        for player in onoffvis[str(segment - 1)]['on']:
          if (player not in onoffvis[str(segment)]['off']) & (player not in onoffvis[str(segment)]['on']):
            onoffvis[str(segment)]['on'].append(player)
        for player in onoffvis[str(segment - 1)]['off']:
          if (player not in onoffvis[str(segment)]['on']) & (player not in onoffvis[str(segment)]['off']):
            onoffvis[str(segment)]['off'].append(player)

      #Because the method above should place every player in a sub in a qarter in either the on- or off-court lists for every segment in the quarter, the concatenated on- and off- lists should look the same (if sorted) for each segment. I create this list, and then use it to check against other payers who are in the play-by-play.      
      homelist = []    
      homelist.extend(onoffhome['1']['on'])
      homelist.extend(onoffhome['1']['off'])
      vislist = []
      vislist.extend(onoffvis['1']['on'])
      vislist.extend(onoffvis['1']['off'])

      #print 'Period ' + str(quarter)
      #print 'Home: Subs'
      #for segment in segments:
        #print 'Segment ' + str(segment) + ':', onoffhome[str(segment)]['on']
      #print homelist
      #print ''
      #print 'Visitor: Subs'
      #for segment in segments:
        #print 'Segment ' + str(segment) + ':', onoffvis[str(segment)]['on']
      #print vislist
      #print ''

      inda = dfa.index
      #print inda
      foulexc = [10,11,16,19,25]

      homeaddlist = []
      visaddlist = []
      #Find other players in the play-byplay not in substitutions to add (in homeaddlist and visaddlist) to all lineups in the quarter. Exceptions are made for technical fouls, ejections and timeouts, which may be credited to players on the bench.
      for i in inda:
        if ((dfa.loc[i, 'EVENTMSGTYPE'] != 6) or (dfa.loc[i, 'EVENTMSGACTIONTYPE'] not in foulexc)) & (dfa.loc[i, 'EVENTMSGTYPE'] != 9) & (dfa.loc[i, 'EVENTMSGTYPE'] != 11):
          if (dfa.loc[i, 'PLAYER1_TEAM_ID'] == dfa.loc[i, 'HOME_ID']) & (dfa.loc[i, 'PLAYER1_ID'] not in homelist) & (dfa.loc[i, 'PLAYER1_ID'] not in homeaddlist):
            homeaddlist.append(dfa.loc[i, 'PLAYER1_ID'])
          if (dfa.loc[i, 'PLAYER2_TEAM_ID'] == dfa.loc[i, 'HOME_ID']) & (dfa.loc[i, 'PLAYER2_ID'] not in homelist) & (dfa.loc[i, 'PLAYER2_ID'] not in homeaddlist):
            homeaddlist.append(dfa.loc[i, 'PLAYER2_ID'])
          if (dfa.loc[i, 'PLAYER3_TEAM_ID'] == dfa.loc[i, 'HOME_ID']) & (dfa.loc[i, 'PLAYER3_ID'] not in homelist) & (dfa.loc[i, 'PLAYER3_ID'] not in homeaddlist):
            homeaddlist.append(dfa.loc[i, 'PLAYER3_ID'])
            
          if (dfa.loc[i, 'PLAYER1_TEAM_ID'] == dfa.loc[i, 'VIS_ID']) & (dfa.loc[i, 'PLAYER1_ID'] not in vislist) & (dfa.loc[i, 'PLAYER1_ID'] not in visaddlist):
            visaddlist.append(dfa.loc[i, 'PLAYER1_ID'])
          if (dfa.loc[i, 'PLAYER2_TEAM_ID'] == dfa.loc[i, 'VIS_ID']) & (dfa.loc[i, 'PLAYER2_ID'] not in vislist) & (dfa.loc[i, 'PLAYER2_ID'] not in visaddlist):
            visaddlist.append(dfa.loc[i, 'PLAYER2_ID'])
          if (dfa.loc[i, 'PLAYER3_TEAM_ID'] == dfa.loc[i, 'VIS_ID']) & (dfa.loc[i, 'PLAYER3_ID'] not in vislist) & (dfa.loc[i, 'PLAYER3_ID'] not in visaddlist):
            visaddlist.append(dfa.loc[i, 'PLAYER3_ID'])
            
      #print homeaddlist
      #print visaddlist
      #print ''
      homelist.extend(homeaddlist)
      vislist.extend(visaddlist)

      for segment in segments:
        onoffhome[str(segment)]['on'].extend(homeaddlist)
        onoffvis[str(segment)]['on'].extend(visaddlist)
        homelineup[str(quarter)][str(segment)] = sorted(onoffhome[str(segment)]['on'])
        vislineup[str(quarter)][str(segment)] = sorted(onoffvis[str(segment)]['on'])
              
        
        
      #print 'Home: PBP'  
      #for segment in segments:
        #print 'Segment ' + str(segment) + ':', onoffhome[str(segment)]['on']
      #print homelist
      #print ''
      #print 'Visitor: PBP'
      #for segment in segments:
        #print 'Segment ' + str(segment) + ':', onoffvis[str(segment)]['on']
      #print vislist
      #print ''
      #print ''
      #rint ''
      #print game, quarter
      #if len(onoffhome['1']['on']) != 5:
        #print game, quarter, 'home', len(onoffhome['1']['on'])
        
      #if len(onoffvis['1']['on']) != 5:
        #print game, quarter, 'vis', len(onoffvis['1']['on'])
    
    #If players are still missing from lineups, calculate playing time in seconds of players in the constructed lineups for the whole game. Compare this playing time to the playing time in the box score. Add players to the appropriate lineups. This occurs if a player plays a whole quarter without being subbed or showing up in the play-by-play       
    for quarter in quarters:  
      if len(homelineup[str(quarter)]['1']) == 4:  
        df.loc[(df.GAME_ID == game) & (df.PERIOD == quarter), 'H_FOURP_BOXE'] = 1
        hminp = {}
        periods = pd.unique(dfg.PERIOD.ravel()).tolist()
        for period in periods:
          dfp = dfg.loc[dfg.PERIOD == period]
          segments = pd.unique(dfp.SEGMENT.ravel()).tolist() 
          for segment in segments:
            for player in homelineup[str(period)][str(segment)]:
              if player in hminp.keys():             
                hminp[player] = hminp[player] + df.loc[df.loc[(df.GAME_ID==game) & (df.PERIOD==period) & (df.SEGMENT==segment)].index[0], 'SEGMENT_TIME']      
              if player not in hminp.keys():
                hminp[player] = df.loc[df.loc[(df.GAME_ID==game) & (df.PERIOD==period) & (df.SEGMENT==segment)].index[0], 'SEGMENT_TIME']      
        
        season = str(year) + '-' + str(year-1999)
        url = 'http://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=34800&GameID=00' + str(game) + '&RangeType=0&Season=' + season + '&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
        res = requests.get(url)
        hminb = {}       
        for player in res.json()['resultSets'][0]['rowSet']:
          if (player[1] == df.loc[dfg.index[0], 'HOME_ID']) & (type(player[8]) == unicode):
            hminb[player[4]] = (60*int(player[8].split(':')[0])) + int(player[8].split(':')[1])
        
        hmindiff = {}      
        #homep = [0,0]
        for player in hminb.keys(): 
          hmindiff[player] = hminb[player] - hminp[player]
          #print player, 'Box: ' + str(hminb[player]), 'PBP: ' + str(hminp[player]), 'Diff: ' + str(hmindiff[player])
          #if hmindiff[player] > homep[1]:
            #homep[0] = player
            #homep[1] = hmindiff[player]
         
        #print homep[0] 
           
        dfqh = dfg.loc[dfg.PERIOD == quarter]
        stints = pd.unique(dfqh.SEGMENT.ravel()).tolist()      
        for stint in stints:
          #homelineup[str(quarter)][str(stint)].append(homep[0])
          #homelineup[str(quarter)][str(stint)] = sorted(homelineup[str(quarter)][str(stint)])
          for player in hmindiff.keys():
            if (hmindiff[player] > 200) & (player not in homelineup[str(quarter)][str(stint)]):
              homelineup[str(quarter)][str(stint)].append(player)
              homelineup[str(quarter)][str(stint)] = sorted(homelineup[str(quarter)][str(stint)])             
          
      if len(vislineup[str(quarter)]['1']) == 4:   
        df.loc[(df.GAME_ID == game) & (df.PERIOD == quarter), 'V_FOURP_BOXE'] = 1  
        vminp = {}
        periods = pd.unique(dfg.PERIOD.ravel()).tolist()
        for period in periods:
          dfq = dfg.loc[dfg.PERIOD == period]
          segments = pd.unique(dfq.SEGMENT.ravel()).tolist() 
          for segment in segments:
            for player in vislineup[str(period)][str(segment)]:
              if player in vminp.keys():
                vminp[player] = vminp[player] + df.loc[df.loc[(df.GAME_ID==game) & (df.PERIOD==period) & (df.SEGMENT==segment)].index[0], 'SEGMENT_TIME']      
              if player not in vminp.keys():
                vminp[player] = df.loc[df.loc[(df.GAME_ID==game) & (df.PERIOD==period) & (df.SEGMENT==segment)].index[0], 'SEGMENT_TIME']      

        season = str(year) + '-' + str(year-1999)      
        url = 'http://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=34800&GameID=00' + str(game) + '&RangeType=0&Season=' + season + '&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
        res = requests.get(url)
        vminb = {}       
        for player in res.json()['resultSets'][0]['rowSet']:
          if (player[1] == df.loc[dfg.index[0], 'VIS_ID']) & (type(player[8]) == unicode):
            vminb[player[4]] = (60*int(player[8].split(':')[0])) + int(player[8].split(':')[1])
        
        vmindiff = {}      
        #visp = [0,0]
        for player in vminb.keys(): 
          vmindiff[player] = vminb[player] - vminp[player]
          #print player, 'Box: ' + str(vminb[player]), 'PBP: ' + str(vminp[player]), 'Diff: ' + str(vmindiff[player])
          #if vmindiff[player] > visp[1]:
            #visp[0] = player
            #visp[1] = vmindiff[player]
            
        #print visp[0]    
            
        dfqv = dfg.loc[dfg.PERIOD == quarter]
        stints = pd.unique(dfqv.SEGMENT.ravel()).tolist()      
        for stint in stints:
          #vislineup[str(quarter)][str(stint)].append(visp[0])
          #vislineup[str(quarter)][str(stint)] = sorted(vislineup[str(quarter)][str(stint)])
          for player in vmindiff.keys():
            if (vmindiff[player] > 200) & (player not in vislineup[str(quarter)][str(stint)]):
              vislineup[str(quarter)][str(stint)].append(player)
              vislineup[str(quarter)][str(stint)] = sorted(vislineup[str(quarter)][str(stint)]) 
    
    #for quarter in quarters:
      #dfq = dfg.loc[df.PERIOD == quarter]
      #segments = pd.unique(dfq.SEGMENT.ravel()).tolist()
      #for segment in segments:
        #print 'Q' + str(quarter), 'S' + str(segment), homelineup[str(quarter)][str(segment)]
    
    #for quarter in quarters:
      #dfq = dfg.loc[df.PERIOD == quarter]
      #segments = pd.unique(dfq.SEGMENT.ravel()).tolist()
      #for segment in segments:
        #print 'Q' + str(quarter), 'S' + str(segment), vislineup[str(quarter)][str(segment)]

    
    for quarter in quarters:
      dfq = dfg.loc[df.PERIOD == quarter]
      segments = pd.unique(dfq.SEGMENT.ravel()).tolist()
      for segment in segments:
        if len(homelineup[str(quarter)][str(segment)]) == 5:
          for i in range(0,5):
            df.loc[(df.GAME_ID == game) & (df.PERIOD == quarter) & (df.SEGMENT == segment), 'H_PLAYER_' + str(i+1)] = homelineup[str(quarter)][str(segment)][i]
        if len(homelineup[str(quarter)][str(segment)]) > 5:
          df.loc[(df.GAME_ID == game) & (df.PERIOD == quarter) & (df.SEGMENT == segment), 'H_EXTRAP_MISSINGSUB'] = 1
        
        if len(vislineup[str(quarter)][str(segment)]) == 5:
          for i in range(0,5):
            df.loc[(df.GAME_ID == game) & (df.PERIOD == quarter) & (df.SEGMENT == segment), 'V_PLAYER_' + str(i+1)] = vislineup[str(quarter)][str(segment)][i]  
        if len(vislineup[str(quarter)][str(segment)]) > 5:
          df.loc[(df.GAME_ID == game) & (df.PERIOD == quarter) & (df.SEGMENT == segment), 'V_EXTRAP_MISSINGSUB'] = 1         
                  
        #print 'Q' + str(quarter), 'S' + str(segment), df.loc[df.loc[(df.GAME_ID==game) & (df.PERIOD==quarter) & (df.SEGMENT==segment)].index[0], 'H_PLAYER_1'], df.loc[df.loc[(df.GAME_ID==game) & (df.PERIOD==quarter) & (df.SEGMENT==segment)].index[0], 'H_PLAYER_2'], df.loc[df.loc[(df.GAME_ID==game) & (df.PERIOD==quarter) & (df.SEGMENT==segment)].index[0], 'H_PLAYER_3'], df.loc[df.loc[(df.GAME_ID==game) & (df.PERIOD==quarter) & (df.SEGMENT==segment)].index[0], 'H_PLAYER_4'], df.loc[df.loc[(df.GAME_ID==game) & (df.PERIOD==quarter) & (df.SEGMENT==segment)].index[0], 'H_PLAYER_5']     
        #print 'Q' + str(quarter), 'S' + str(segment), df.loc[df.loc[(df.GAME_ID==game) & (df.PERIOD==quarter) & (df.SEGMENT==segment)].index[0], 'V_PLAYER_1'], df.loc[df.loc[(df.GAME_ID==game) & (df.PERIOD==quarter) & (df.SEGMENT==segment)].index[0], 'V_PLAYER_2'], df.loc[df.loc[(df.GAME_ID==game) & (df.PERIOD==quarter) & (df.SEGMENT==segment)].index[0], 'V_PLAYER_3'], df.loc[df.loc[(df.GAME_ID==game) & (df.PERIOD==quarter) & (df.SEGMENT==segment)].index[0], 'V_PLAYER_4'], df.loc[df.loc[(df.GAME_ID==game) & (df.PERIOD==quarter) & (df.SEGMENT==segment)].index[0], 'V_PLAYER_5']     
    
  df.to_csv('C:/Users/TICCamp/Desktop/NBA/PlaybyPlay/db/playbyplay' + str(year) + 'line.csv')
  
  
  
  
  
  
  
  
  
  