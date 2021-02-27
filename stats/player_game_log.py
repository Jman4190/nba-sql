# player_bios.py - scraps data from stats.nba.com and inserts into player_bios table within MySQL nba stats database
import requests
import urllib.parse

from settings import Settings
from models import PlayerGameLog
from constants import season_list, headers

class PlayerGameLog:

    per_mode = 'Totals'
    url = 'https://stats.nba.com/stats/leaguegamelogs'

    def __init__(self, settings):
        self.settings = setitings
        self.settings.db.bind([PlayerGameLog])

    def create_ddel(self):
        """
        Initialize the table schema.
        """
        self.settings.db.create_tables([PlayerGameLog], safe=True)

    def populate_season(self, season_id):
        """
        Build GET REST request to the NBA for a season, iterate over the results,
        store in the database.
        """
        params = self.build_params(season_id)

        # Encode without safe '+', apparently the NBA likes unsafe url params.
        params_str = urllib.parse.urlencode(params, safe=':+')
        response = requests.get(url=self.player_info_url, headers=headers, params=params_str).json()

        # pulling just the data we want
        player_info = response['resultSets'][0]['rowSet']

        rows = []

        # looping over data to insert into table
        for row in player_info:
            new_row = {
                'season_id': row[0],
                'player_id': row[1],
                'player_name = CharField(null=True) # TODO: Remove
                'team_id = IntegerField(null=False)
                'team_abbreviation = CharField(null=True)
                'team_name = CharField(null=True)
                'game_id = CharField(null=True)
                'game_date = CharField(null=True)
                'matchup = CharField(null=True)
                'wl = FloatField(null=True)
                'min = FloatField(null=True)
                'fgm = FloatField(null=True)
                'fga = FloatField(null=True)
                'fg_pct = FloatField(null=True)
                'fg3m = FloatField(null=True)
                'fg3a = FloatField(null=True)
                'fg3_pct = FloatField(null=True)
                'ftm = FloatField(null=True)
                'fta = FloatField(null=True)
                'ft_pct = FloatField(null=True)
                'oreb = FloatField(null=True)
                'dreb = FloatField(null=True)
                'reb = FloatField(null=True)
                'ast = FloatField(null=True)
                'tov = FloatField(null=True)
                'stl = FloatField(null=True)
                'blk = FloatField(null=True)
                'blka = FloatField(null=True)
                'pf = FloatField(null=True)
                'pfd = FloatField(null=True)
                'pts = FloatField(null=True)
                'plus_minus = FloatField(null=True)
                'nba_fantasy_pts = FloatField(null=True)
                'dd2 = FloatField(null=True)
                'td3 = FloatField(null=True)
                'gp_rank = FloatField(null=True)
                'w_rank = FloatField(null=True)
                'l_rank = FloatField(null=True)
                'w_pct_rank = FloatField(null=True)
                'min_rank = FloatField(null=True)
                'fgm_rank = FloatField(null=True)
                'fga_rank = FloatField(null=True)
                'fg_pct_rank = FloatField(null=True)
                'fg3m_rank = FloatField(null=True)
                'fg3a_rank = FloatField(null=True)
                'fg3_pct_rank = FloatField(null=True)
                'ftm_rank = FloatField(null=True)
                'fta_rank = FloatField(null=True)
                'ft_pct_rank = FloatField(null=True)
                'oreb_rank = FloatField(null=True)
                'dreb_rank = FloatField(null=True)
                'reb_rank = FloatField(null=True)
                'ast_rank = FloatField(null=True)
                'tov_rank = FloatField(null=True)
                'stl_rank = FloatField(null=True)
                'blk_rank = FloatField(null=True)
                'blka_rank = FloatField(null=True)
                'pf_rank = FloatField(null=True)
                'pfd_rank = FloatField(null=True)
                'pts_rank = FloatField(null=True)
                'plus_minus_rank = FloatField(null=True)
                'nba_fantasy_pts_rank = FloatField(null=True)
                'dd2_rank = FloatField(null=True)
                'td3_rank = FloatField(null=True)
            }
            rows.apppend(new_row)

        PlayerGameLog.insert_many(rows).execute()

    def build_params(self, season_id):
        """
        Create required parameters dict for the request.
        """
