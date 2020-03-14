from peewee import *
from datetime import date
from playhouse.postgres_ext import PostgresqlExtDatabase

# db = SqliteExtDatabase('peewee.db', pragmas=(
#     ('cache_size', -1024 * 64),  # 64MB page-cache.
#     ('journal_mode', 'wal'),  # Use WAL-mode (you should always use this!).
#     ('foreign_keys', 1),
#     ('c_extensions', True)))  # Enforce foreign-key constraints.

db = PostgresqlDatabase('postgres',  user='max', password='max',
                           host='45.11.24.68', port=5432)


def Init():
    with db:
        if (not db.table_exists('Chat')):
            db.create_tables([Chat, User, Message, CUser, CToken])

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
    # photo = BlobField(null=True)

class Message(BaseModel):
    rowid = IntegerField(unique=True, primary_key=True)
    message_id = IntegerField(index=True)
    version = IntegerField()
    act_date = DateTimeField(),
    user = ForeignKeyField(User, backref = 'messages')
    create_date = DateTimeField()
    chat = ForeignKeyField(Chat, backref = 'messages'),
    state = IntegerField()
    content = TextField()

class CUser(BaseModel):
    rowid = IntegerField(unique=True, primary_key=True)
    username = TextField()
    password = TextField()
    is_active = BooleanField()
    is_telegramm_auth = BooleanField()
    class Meta:
        indexes = (
            (('username', 'password'), True),
        )

class CToken(BaseModel):
    rowid = IntegerField(unique=True, primary_key=True)
    user = ForeignKeyField(CUser, backref = 'tokens'),
    token = TextField()
