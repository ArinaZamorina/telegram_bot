import os
from peewee import *

if __name__ == '__main__':
    raise NotSupportedError("Can only be used as a module")

DB = MySQLDatabase('historydb', user=os.getenv('LOG'), password=os.getenv('PASSWORD'),
                   host=os.getenv('HOST'), port=int(os.getenv('PORT')))
DB.connect()


class BaseModel(Model):
    class Meta:
        database = DB


class Person(BaseModel):
    chat_id = IntegerField()
    name = TextField()


class History(BaseModel):
    chat_id = IntegerField()
    command = TextField()
    time = TimeField()
    hotels = TextField()


def migrate():
    cur = DB.cursor()
    cur.execute("SHOW TABLES FROM `historydb` like 'person'")
    result = cur.fetchall()
    if len(result) == 0:
        DB.create_tables([Person])

    cur = DB.cursor()
    cur.execute("SHOW TABLES FROM `historydb` like 'history'")
    result = cur.fetchall()
    if len(result) == 0:
        DB.create_tables([History])
