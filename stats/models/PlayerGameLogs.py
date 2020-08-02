from peewee import *
from models import BaseModel

class PlayerGameLogs(BaseModel):
    season_id = CharField(null = True)
    player_id = IntegerField(null = True)
    player_name = CharField(null = True)
    team_id = IntegerField(null = True)
    team_abbreviation = CharField(null = True)
    team_name = CharField(null = True)
    game_id = CharField(null = True)
    game_date = CharField(null = True)
    matchup = CharField(null = True)
    wl = CharField(null = True)
    min = FloatField(null = True)
    fgm = FloatField(null = True)
    fga = FloatField(null = True)
    fg_pct = FloatField(null = True)
    fg3m = FloatField(null = True)
    fg3a = FloatField(null = True)
    fg3_pct = FloatField(null = True)
    ftm = FloatField(null = True)
    fta = FloatField(null = True)
    ft_pct = FloatField(null = True)
    oreb = FloatField(null = True)
    dreb = FloatField(null = True)
    reb = FloatField(null = True)
    ast = FloatField(null = True)
    stl = FloatField(null = True)
    blk = FloatField(null = True)
    tov = FloatField(null = True)
    pf = FloatField(null = True)
    pts = FloatField(null = True)
    plus_minus = FloatField(null = True)
    video_available = IntegerField(null = True)
	
    class Meta:
        db_table = 'player_game_logs'