from peewee import *
from . import Player
from . import Team

class PlayerSeason(Model):

    ## Default to auto generated id column here, because
    ## a player could belong to multiple teams in a season (not unique)
    ## and team_id is also nullable (which makes it unique).
    ## A nullable foreign key as part of a composite primary key 
    ## is a bit too gnarly, so we're going to have a 
    ## unique composite index.

    ## Is this the right way to do this? Should we just get rid of this table?

    ## Composite Unique Index Fields
    player_id = ForeignKeyField(Player, index=True)
    season_id = CharField(null=False, index=True)
    team_id = ForeignKeyField(Team, index=True, null=True)

    age = IntegerField(null=True)
    player_height = CharField(null=True)
    player_height_inches = IntegerField(null=True)
    player_weight = CharField(null=True)
    gp = IntegerField(null=True)
    pts = FloatField(null=True)
    reb = FloatField(null=True)
    ast = FloatField(null=True)
    net_rating = FloatField(null=True)
    oreb_pct = FloatField(null=True)
    dreb_pct = FloatField(null=True)
    usg_pct = FloatField(null=True)
    ts_pct = FloatField(null=True)
    ast_pct = FloatField(null=True)
	
    class Meta:
        db_table = 'player_season'
        indexes = (
            (('player_id', 'season_id', 'team_id'), True),
        )
