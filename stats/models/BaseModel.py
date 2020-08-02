from peewee import *
from settings import Settings

settings = Settings()

class BaseModel(Model):
    class Meta:
        database = settings.db
