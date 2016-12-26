# Checks if there are sequences with a tech foul, a sub, and then another tech foul before a tech free throw.

import pandas as pd

def pbp_checktechftsequence(year, type = 'reg', datapath = ''):
  #Create pandas dataframe for single year
  df = pd.read_csv('{}playbyplay_{}_{}_stint.csv'.format(datapath, type, year))
  df = df.drop(['Unnamed: 0', 'Unnamed: 0.1'], 1)
  
  techftind = df[(df['EVENTMSGTYPE']==3) & (df['EVENTMSGACTIONTYPE'].isin([16,21]))].index
  techfoulind = df[(df['EVENTMSGTYPE']==6) & (df['EVENTMSGACTIONTYPE'].isin([11,12,13,17,18,19,25,30]))].index
  subind = df[df['EVENTMSGTYPE']==8].index
    
  for i in techfoulind[:-1]:
    try:
      tft = min(x for x in techftind if x>i)
      sub = min(y for y in subind if y>i)
      techpostsub = min(z for z in techfoulind if z>sub)
      if techpostsub < tft:
        print year, df.loc[i, 'GAME_ID'], i
    except ValueError:
      print 'ValueError:', year, df.loc[i, 'GAME_ID'], i    
      
      
if __name__ == '__main__':

  years = range(1996, 2015)
  for year in years:
    print ''
    print year
    pbp_checktechftsequence(year)