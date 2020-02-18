from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase, RowIDField

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
    id = IntegerField(unique=True, primary_key=True)
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
    rowid = RowIDField(primary_key=True)
    id = IntegerField(index=True)
    version = IntegerField()
    user_id = IntegerField(null=True)
    act_date = DateTimeField()
    create_date = DateTimeField()
    chat_id = ForeignKeyField(Chat, field='id', backref='messages', db_column='chat_id')
    state = IntegerField()
    content = TextField(null=True)
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
    messages = []

    def __init__(self, messages=None):
        self.messages = []
        if messages is None:
            q = Message.select()
            for msg in q:
                self.messages.append(msg)
        else:
            self.messages = messages

    def add(self, message):
        self.messages.append(message)
        print(1)
        message.save()
        print(2)

    def modify(self, message):
        for msg in self.messages:
            if str(msg.id) == str(message.id):
                msg.modify()
                print(0)
        self.messages.append(message)
        print(1)
        message.save()
        print(2)

    def delete(self, message):
        for msg in self.messages:
            if str(msg.id) == str(message.id):
                msg.delete_()
                message.chat_id = msg.chat_id
        self.messages.append(message)
        message.save()

    @staticmethod
    def get_all_messages():
        messages = []
        q = Message.select()
        for msg in q:
            messages.append(msg)
        return messages


class Chats:
    chats = []

    def __init__(self, chats, monitored):
        all_chats = self.get_all_chats()
        monitored_chats = self.get_monitored()
        for chat in chats:
            if chat not in all_chats:
                if chats[chat] in monitored:
                    item = Chat.create(id=chat, name=chats[chat], track=True)
                    self.chats.append(item)
                else:
                    item = Chat.create(id=chat, name=chats[chat], track=False)
                    self.chats.append(item)
            else:
                if chats[chat] in monitored and chat not in monitored_chats:
                    Chat.update({Chat.track: True}).where(Chat.id == chat).execute()
                elif chats[chat] not in monitored and chat in monitored_chats:
                    Chat.update({Chat.track: False}).where(Chat.id == chat).execute()

    @staticmethod
    def get_monitored():
        monitored = {}
        q = (Chat.select().where(Chat.track == True))
        for chat in q:
            monitored[chat.id] = chat.name
        return monitored

    @staticmethod
    def get_all_chats():
        chats = {}
        q = (Chat.select())
        for chat in q:
            chats[chat.id] = chat.name
        return chats

# all_messages = Messages()
#
# msg = Message(id=150, version=0, user_id=15, act_date='2019-12-12 23:15:04', create_date='2019-12-12 23:15:04',
#               chat_id=-1001036362176, state=0, content='noga')
#
# all_messages.add(msg)
#
# print(Chats.get_monitored())
# print(all_messages.messages)

# test_dict = {12: 'goga', 115: 'magoga'}
# dict_2 = [{17: 'jopa'}, {12: 'goga'}]
#
# for i in dict_2:
#     print(i)
#     if i in test_dict:
#         print('Yes')
# if 17 not in dict_2:
#     print(72)

# a = Messages.get_all_messages()[3]
# pass
