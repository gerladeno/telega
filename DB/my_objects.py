from datetime import datetime, timedelta
from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase
from config import *

# Connect to DB
db = PostgresqlExtDatabase('postgres', user=db_user, password=db_password, host=db_host, port=5432, autoconnect=True)


def init():
    # Check if DB has the tables we need to work. If not, create them
    with db:
        if not db.table_exists('chat', db_user):
            db.create_tables([Chat])
            db_logger.info(u'Table Chat not found, created anew')
        if not db.table_exists('message', db_user):
            db.create_tables([Message])
            db_logger.info(u'Table Message not found, created anew')
        if not db.table_exists('user', db_user):
            db.create_tables([User])
            db_logger.info(u'Table User not found, created anew')


class BaseModel(Model):
    _create_at = DateTimeField(default=datetime.now())
    _modified_at = DateTimeField(default=datetime.now())

    class Meta:
        database = db


class Chat(BaseModel):
    id = TextField(primary_key=True)
    name = TextField()
    track = BooleanField()
    title = TextField(null=True)

    class Meta:
        db_table = 'chat'


class User(BaseModel):
    id = TextField()
    username = TextField()
    phone = TextField()
    photo = BlobField(null=True)

    class Meta:
        db_table = 'user'


class Message(BaseModel):
    uid = BigAutoField(primary_key=True)
    id = TextField()
    version = IntegerField()
    user_id = TextField(null=True)
    chat_id = ForeignKeyField(Chat, field='id', backref='messages', db_column='chat_id')
    state = IntegerField()
    content = TextField(null=True)
    media = TextField(null=True)

    class Meta:
        db_table = 'message'

    # A method to change version and state. We call it, if this message was edited
    def modify(self):
        self.state = 1
        self.version = self.version + 1
        self._modified_at = datetime.now()
        self.save()

    def delete_(self):
        self.state = 2
        self._modified_at = datetime.now()
        self.save()

