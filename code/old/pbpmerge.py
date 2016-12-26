import pandas as pd

years = [2004,2005,2006,2007,2008,2009,2010,2012,2013,2014]

df_merge = pd.DataFrame()
for year in years:
  df = pd.read_csv('playbyplay' + str(year) +'seg.csv')
  df_merge = df_merge.append(df)
  df_merge.to_csv('playbyplay4101214.csv')
  print year