# player_bios.py - scraps data from stats.nba.com and inserts into player_bios table within MySQL nba stats database
import requests

from settings import Settings
from models import PlayerBios

settings = Settings()
settings.db.create_tables([PlayerBios], safe=True)

headers  = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-token': 'true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

season_list = [
	'1996-97',
	'1997-98',
	'1998-99',
	'1999-00',
	'2000-01',
	'2001-02',
	'2002-03',
	'2003-04',
	'2004-05',
	'2005-06',
	'2006-07',
	'2007-08',
	'2008-09',
	'2009-10',
	'2010-11',
	'2011-12',
	'2012-13',
	'2013-14',
	'2014-15',
	'2015-16',
	'2016-17',
	'2017-18',
	'2018-19',
	'2019-20'
]

#per_mode = 'Per100Possessions'
per_mode = 'Totals'
#per_mode = 'Per36'
#per_mode = 'PerGame'

# for loop to loop over seasons
for season_id in season_list:
	#player_info_url = 'http://stats.nba.com/stats/leaguedashplayerbiostats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&Season=' + seasonid + '&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='
    player_info_url = 'http://stats.nba.com/stats/leaguedashplayerbiostats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode={}&Period=0&PlayerExperience=&PlayerPosition=&Season={}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='.format(per_mode, season_id)
	# json response
    response = requests.get(url=player_info_url, headers=headers).json()
    # pulling just the data we want
    player_info = response['resultSets'][0]['rowSet']
    # looping over data to insert into table
    for row in player_info:
        player = PlayerBios(
            season_id=season_id,  # this is key, need this to join and sort by seasons
            player_id=row[0],
            player_name=row[1],
            team_id=row[2],
            team_abbreviation=row[3],
            age=row[4],
            player_height=row[5],
            player_height_inches=row[6],
            player_weight=row[7],
            college=row[8],
            country=row[9],
            draft_year=row[10],
            draft_round=row[11],
            draft_number=row[12],
            gp=row[13],
            pts=row[14],
            reb=row[15],
            ast=row[16],
            net_rating=row[17],
            oreb_pct=row[18],
            dreb_pct=row[19],
            usg_pct=row[20],
            ts_pct=row[21],
            ast_pct=row[22]
            )

        player.save()
        print("Done with another season.")

print ("Done inserting player bios data to the database!")