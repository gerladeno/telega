from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase, RowIDField
from datetime import date

def Init():
    with db:
        if (not db.table_exists('Chat')):
            db.create_tables([Chat, User, Message])

db = SqliteExtDatabase('peewee.db', pragmas=(
    ('cache_size', -1024 * 64),  # 64MB page-cache.
    ('journal_mode', 'wal'),  # Use WAL-mode (you should always use this!).
    ('foreign_keys', 1),
    ('c_extensions', True)))  # Enforce foreign-key constraints.

class BaseModel(Model):
    class Meta:
        database = db

class Chat(BaseModel):
    id = IntegerField(unique=True, primary_key=True)
    name = TextField()
    title = TextField()
    track = BooleanField(default=True)

class User(BaseModel):
    id = IntegerField(unique=True, primary_key=True)
    username = TextField()
    phone = TextField()
    photo = BlobField(null=True)

class Message(BaseModel):
    rowid = RowIDField()
    message_id = IntegerField(index=True)
    version = IntegerField()
    act_date = DateTimeField(),
    user = ForeignKeyField(User, backref = 'messages')
    create_date = DateTimeField()
    chat = ForeignKeyField(Chat, backref = 'messages'),
    state = IntegerField()
    content = TextField()