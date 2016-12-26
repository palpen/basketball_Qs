import requests
import pandas as pd

#Year and game range for scraping NBA Play-by-Play: 82 game seasons (66 games in 2011, 50 games in 1998); 29 teams 1996 - 2003, 30 teams 2004 onward
games = range(1,991)
years = [2011]

for year in years:

  season = str(year) + '-' + str(year+1)
  playbyplay_df = pd.DataFrame()
  
  for game in games:
    print year, game
    gameid = 20000000 + game + ((year-2000)*100000)
    url = 'http://stats.nba.com/stats/playbyplayv2?EndPeriod=10&EndRange=55800&GameID=00' + str(gameid) + '&RangeType=2&Season=' + season + '&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
    
    res = requests.get(url)
    cols = res.json()['resultSets'][0]['headers']
    rows = res.json()['resultSets'][0]['rowSet']
    df = pd.DataFrame(rows, columns=cols)
    playbyplay_df = playbyplay_df.append(df)
    
  playbyplay_df.to_csv('playbyplay' + str(year) + '.csv')