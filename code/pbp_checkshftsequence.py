# Checks if there are sequences with a shooting foul, a sub, and then another non-tech foul before a non-tech free throw.

import pandas as pd

def pbp_checkshftsequence(year, type = 'reg', datapath = ''):
  #Create pandas dataframe for single year
  df = pd.read_csv('{}playbyplay_{}_{}_stint.csv'.format(datapath, type, year))
  df = df.drop(['Unnamed: 0', 'Unnamed: 0.1'], 1)
  
  nontechftind = df[(df['EVENTMSGTYPE']==3) & (~df['EVENTMSGACTIONTYPE'].isin([16,21]))].index
  shfoulind = df[(df['EVENTMSGTYPE']==6) & (df['EVENTMSGACTIONTYPE'].isin([2,9,14,15,29]))].index
  nontechfoulind = df[(df['EVENTMSGTYPE']==6) & (~df['EVENTMSGACTIONTYPE'].isin([11,12,13,17,18,19,25,30]))].index
  subind = df[df['EVENTMSGTYPE']==8].index
    
  for i in shfoulind[:-1]:
    try:
      shft = min(x for x in nontechftind if x>i)
      sub = min(y for y in subind if y>i)
      foulpostsub = min(z for z in nontechfoulind if z>sub)
      if foulpostsub < shft:
        print year, df.loc[i, 'GAME_ID'], i
    except ValueError:
      print 'ValueError:', year, df.loc[i, 'GAME_ID'], i
      
      
if __name__ == '__main__':

  years = range(1996, 2015)
  for year in years:
    print ''
    print year
    pbp_checkshftsequence(year)