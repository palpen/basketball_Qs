import pandas as pd 
import requests


years = [1996,1997,1998,1999,2000,2001,2002,2003,2011]
for year in years:

  df = pd.read_csv('playbyplay' + str(year) + 'seg.csv')
  df = df.drop('Unnamed: 0', 1)

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

            
      homelist = []    
      homelist.extend(onoffhome['1']['on'])
      homelist.extend(onoffhome['1']['off'])
      vislist = []
      vislist.extend(onoffvis['1']['on'])
      vislist.extend(onoffvis['1']['off'])

      inda = dfa.index
      #print inda
      foulexc = [10,11,16,19,25]

      homeaddlist = []
      visaddlist = []

      for i in inda:
        if ((dfa.loc[i, 'EVENTMSGTYPE'] != 6) or (dfa.loc[i, 'EVENTMSGACTIONTYPE'] not in foulexc)) & (dfa.loc[i, 'EVENTMSGTYPE'] != 9) & (dfa.loc[i, 'EVENTMSGTYPE'] != 11):
          if (dfa.loc[i, 'PLAYER1_TEAM_ID'] == dfa.loc[i, 'HOME_ID']) & (dfa.loc[i, 'PLAYER1_ID'] not in homelist) & (dfa.loc[i, 'PLAYER1_ID'] not in homeaddlist) & (dfa.loc[i, 'PLAYER1_ID'] != 0):
            homeaddlist.append(dfa.loc[i, 'PLAYER1_ID'])
          if (dfa.loc[i, 'PLAYER2_TEAM_ID'] == dfa.loc[i, 'HOME_ID']) & (dfa.loc[i, 'PLAYER2_ID'] not in homelist) & (dfa.loc[i, 'PLAYER2_ID'] not in homeaddlist) & (dfa.loc[i, 'PLAYER2_ID'] != 0):
            homeaddlist.append(dfa.loc[i, 'PLAYER2_ID'])
          if (dfa.loc[i, 'PLAYER3_TEAM_ID'] == dfa.loc[i, 'HOME_ID']) & (dfa.loc[i, 'PLAYER3_ID'] not in homelist) & (dfa.loc[i, 'PLAYER3_ID'] not in homeaddlist) & (dfa.loc[i, 'PLAYER3_ID'] != 0):
            homeaddlist.append(dfa.loc[i, 'PLAYER3_ID'])
            
          if (dfa.loc[i, 'PLAYER1_TEAM_ID'] == dfa.loc[i, 'VIS_ID']) & (dfa.loc[i, 'PLAYER1_ID'] not in vislist) & (dfa.loc[i, 'PLAYER1_ID'] not in visaddlist) & (dfa.loc[i, 'PLAYER1_ID'] != 0):
            visaddlist.append(dfa.loc[i, 'PLAYER1_ID'])
          if (dfa.loc[i, 'PLAYER2_TEAM_ID'] == dfa.loc[i, 'VIS_ID']) & (dfa.loc[i, 'PLAYER2_ID'] not in vislist) & (dfa.loc[i, 'PLAYER2_ID'] not in visaddlist) & (dfa.loc[i, 'PLAYER2_ID'] != 0):
            visaddlist.append(dfa.loc[i, 'PLAYER2_ID'])
          if (dfa.loc[i, 'PLAYER3_TEAM_ID'] == dfa.loc[i, 'VIS_ID']) & (dfa.loc[i, 'PLAYER3_ID'] not in vislist) & (dfa.loc[i, 'PLAYER3_ID'] not in visaddlist) & (dfa.loc[i, 'PLAYER3_ID'] != 0):
            visaddlist.append(dfa.loc[i, 'PLAYER3_ID'])
            
      homelist.extend(homeaddlist)
      vislist.extend(visaddlist)
      
      homelen = 0
      vislen = 0
      for segment in segments:
        onoffhome[str(segment)]['on'].extend(homeaddlist)
        onoffvis[str(segment)]['on'].extend(visaddlist)
        homelineup[str(quarter)][str(segment)] = sorted(onoffhome[str(segment)]['on'])
        vislineup[str(quarter)][str(segment)] = sorted(onoffvis[str(segment)]['on'])
        if len(homelineup[str(quarter)][str(segment)]) != 5:
          homelen = len(homelineup[str(quarter)][str(segment)]) 
        if len(vislineup[str(quarter)][str(segment)]) != 5:
          vislen = len(vislineup[str(quarter)][str(segment)])
          
      if homelen != 0:
        print year, game, 'home', 'q' + str(quarter), 'len: ' + str(len(homelineup[str(quarter)][str(segment)]))      
        for segment in segments:
          print segment, len(homelineup[str(quarter)][str(segment)]), homelineup[str(quarter)][str(segment)]
        print ''
        print '' 
      if vislen != 0:
        print year, game, 'vis', 'q' + str(quarter), 'len: ' + str(len(vislineup[str(quarter)][str(segment)]))      
        for segment in segments:
          print segment, len(vislineup[str(quarter)][str(segment)]), vislineup[str(quarter)][str(segment)]
        print ''
        print ''         
          
 