from peewee import *
# from main import db
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
    id = IntegerField()
    name = TextField()
    track = BooleanField()
    title = TextField(null=True)

    class Meta:
        db_table = 'chat'


class User(BaseModel):
    id = IntegerField()
    username = TextField()
    phone = TextField()
    photo = BlobField(null=True)

    class Meta:
        db_table = 'user'


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

    class Meta:
        db_table = 'message'

    def modify(self):
        self.state = 1
        self.version = self.version + 1
        self.save()

    def delete_(self):
        self.state = 2
        self.save()


class Messages:

    def __init__(self, messages=None):
        if messages is None:
            self.messages = Message.select()
        else:
            self.messages = messages

    def add(self, message):
        self.messages.append(message)
        message.save(force_insert = True)

    def modify(self, message):
        for msg in self.messages:
            if str(msg.id) == str(message.id):
                msg.modify()
        self.messages.append(message)
        message.save(force_insert = True)

    def delete(self, message):
        for msg in self.messages:
            if str(msg.id) == str(message.id):
                msg.delete_()
                message.chat_id = msg.chat_id
        self.messages.append(message)
        message.save(force_insert = True)


class Chats:
    chats = []

    def __init__(self, chats, monitored):
        Chat.delete().execute()
        for chat in chats:
            if chats[chat] in monitored:
                item = Chat.create(id=chat, name=chats[chat], track=True)
                self.chats.append(item)
            else:
                item = Chat.create(id=chat, name=chats[chat], track=False)
                self.chats.append(item)

    def get_monitored(self):
        return Chat.select().where(Chat.track is True)
