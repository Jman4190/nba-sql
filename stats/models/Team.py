from peewee import *

class Team(Model):
    team_id = IntegerField(primary_key=True)
    abbreviation = CharField(null = True)
    nickname = CharField(null = True)
    year_founded = CharField(null = True)

    class Meta:
        db_table = 'team'
