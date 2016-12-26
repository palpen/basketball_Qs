import pandas as pd 
import requests

df = pd.read_csv('playbyplay2006seg.csv')
df = df.drop('Unnamed: 0', 1)

for i in range(1,6):
  df['H_PLAYER_' + str(i)] = 0
for i in range(1,6):
  df['V_PLAYER_' + str(i)] = 0

#games = pd.unique(df.GAME_ID.ravel()).tolist()
games = [20600431,20600887]
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
    
    onoffhome = {}
    onoffvis = {}
    for segment in segments:
      onoffhome[str(segment)] = {}
      onoffvis[str(segment)] = {}
      onoffhome[str(segment)]['on'] = []
      onoffhome[str(segment)]['off'] = []
      onoffvis[str(segment)]['on'] = []
      onoffvis[str(segment)]['off'] = []

    for segment in segments[1:]:  
      dfseg = dfsub.loc[dfsub.SEGMENT == segment]
      ind = dfseg.index
      for i in ind:
        if dfseg.loc[i, 'PLAYER1_TEAM_ID'] == dfseg.loc[i, 'HOME_ID']:
          onoffhome[str(segment)]['on'].append(dfseg.loc[i, 'PLAYER2_ID'])
          onoffhome[str(segment)]['off'].append(dfseg.loc[i, 'PLAYER1_ID'])
          for t in segments[:segments.index(segment)]:
            if (dfseg.loc[i, 'PLAYER2_ID'] not in onoffhome[str(t)]['on']) & (dfseg.loc[i, 'PLAYER2_ID'] not in onoffhome[str(t)]['off']):
              onoffhome[str(t)]['off'].append(dfseg.loc[i, 'PLAYER2_ID'])
            if (dfseg.loc[i, 'PLAYER1_ID'] not in onoffhome[str(t)]['off']) & (dfseg.loc[i, 'PLAYER1_ID'] not in onoffhome[str(t)]['on']):
              onoffhome[str(t)]['on'].append(dfseg.loc[i, 'PLAYER1_ID'])     
          
        if dfseg.loc[i, 'PLAYER1_TEAM_ID'] == dfseg.loc[i, 'VIS_ID']:
          onoffvis[str(segment)]['on'].append(dfseg.loc[i, 'PLAYER2_ID'])
          onoffvis[str(segment)]['off'].append(dfseg.loc[i, 'PLAYER1_ID'])
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
  
         
  for quarter in quarters:  
    if len(homelineup[str(quarter)]['1']) != 5:     
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

      url = 'http://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=34800&GameID=00' + str(game) + '&RangeType=0&Season=2006-07&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
      res = requests.get(url)
      hminb = {}       
      for player in res.json()['resultSets'][0]['rowSet']:
        if (player[1] == df.loc[dfg.index[0], 'HOME_ID']) & (type(player[8]) == unicode):
          hminb[player[4]] = (60*int(player[8].split(':')[0])) + int(player[8].split(':')[1])
      
      hmindiff = {}      
      homep = [0,0]
      print game, quarter, 'vis'
      for player in hminb.keys(): 
        hmindiff[player] = hminb[player] - hminp[player]
        print player, 'Box: ' + str(hminb[player]), 'PBP: ' + str(hminp[player]), 'Diff: ' + str(hmindiff[player])

        
    if len(vislineup[str(quarter)]['1']) != 5:     
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

      url = 'http://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=34800&GameID=00' + str(game) + '&RangeType=0&Season=2006-07&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
      res = requests.get(url)
      vminb = {}       
      for player in res.json()['resultSets'][0]['rowSet']:
        if (player[1] == df.loc[dfg.index[0], 'VIS_ID']) & (type(player[8]) == unicode):
          vminb[player[4]] = (60*int(player[8].split(':')[0])) + int(player[8].split(':')[1])
      
      vmindiff = {}      
      visp = [0,0]
      print game, quarter, 'vis'
      for player in vminb.keys(): 
        vmindiff[player] = vminb[player] - vminp[player]
        print player, 'Box: ' + str(vminb[player]), 'PBP: ' + str(vminp[player]), 'Diff: ' + str(vmindiff[player])
       
 
  
  