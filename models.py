from peewee import *
import datetime
from playhouse.db_url import connect

DATABASE = SqliteDatabase('Urls.sqlite')

class Urls(Model):
    id = IntegerField(primary_key=True)
    orginal_url = TextField(unique=True)
    short_url = TextField(unique=True)
    count = IntegerField(default=1)
    created_at = DateTimeField(default=datetime.datetime.now)


    class Meta:
        database = DATABASE



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Urls], safe=True)
    print("TABLES Created")
    DATABASE.close()


    