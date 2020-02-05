from peewee import *
#from main import db
from playhouse.sqlite_ext import SqliteExtDatabase


# DB
db = SqliteExtDatabase('peewee.db', pragmas=(
    ('cache_size', -1024 * 64),  # 64MB page-cache.
    ('journal_mode', 'wal'),  # Use WAL-mode (you should always use this!).
    ('foreign_keys', 1),
    ('c_extensions', True)))  # Enforce foreign-key constraints.


def init():
    with db:
        if not db.table_exists('Chat'):
            db.create_tables([Chat, User, Message])


class BaseModel(Model):
    class Meta:
        database = db


class Chat(BaseModel):
    id = IntegerField(primary_key=True)
    name = TextField()
    track = BooleanField
    title = TextField()

    def __init__(self, id, name, track=False, title=""):
        self.id = id
        self.name = name
        self.track = track
        self.title = title


class User(BaseModel):
    id = IntegerField(primary_key=True)
    username = TextField()
    phone = TextField()
    photo = BlobField(null=True)


class Message(BaseModel):
    id = IntegerField(index=True)
    version = IntegerField()
    user_id = IntegerField()
    act_date = DateTimeField()
    create_date = DateTimeField()
    chat_id = ForeignKeyField(Chat, backref='messages')
    state = IntegerField()
    content = TextField()
    media = BlobField(null=True)

    def __init__(self, id, version=None, user_id=None, act_date=None, create_date=None, chat_id=None, state=None,
                 content=None, media=None):
        if version is None:
            self.id = id[0]
            self.version = id[1]
            self.user_id = id[2]
            self.act_date = id[3]
            self.create_date = id[4]
            self.chat_id = id[5]
            self.state = id[6]
            self.content = id[7]
            self.media = id[8]
            self.list = id
        else:
            self.id = id
            self.version = version
            self.user_id = user_id
            self.act_date = act_date
            self.create_date = create_date
            self.chat_id = chat_id
            self.state = state
            self.content = content
            self.media = media

    def modify(self):
        self.state = 1
        self.version = self.version + 1
        self.save()

    def delete_(self):
        self.state = 2
        self.save()


class Messages:
    messages = []

    def __init__(self, messages=None):
        if messages is None:
            self.messages = Message.select()
        else:
            self.messages = messages

    def add(self, message):
        self.messages.append(message)
        message.save()

    def modify(self, message):
        for msg in self.messages:
            if str(msg.id) == str(message.id):
                msg.modify()
        self.messages.append(message)
        message.save()

    def delete(self, message):
        for msg in self.messages:
            if str(msg.id) == str(message.id):
                msg.delete_()
                message.chat_id = msg.chat_id
        self.messages.append(message)
        message.save()


class Chats:
    chats = []

    def __init__(self, chats, monitored):
        for chat in chats:
            if chats[chat] in monitored:
                self.chats.append(Chat(id=chat, name=chats[chat], track=True))
            else:
                self.chats.append(Chat(id=chat, name=chats[chat]))

    def get_monitored(self):
        return Chat.select().where(Chat.track is True)
