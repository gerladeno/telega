from datetime import datetime
from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase
import logging
import logging.handlers

LOG_FILENAME = u'main.log'

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO)
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20, backupCount=15)
# DB
db = PostgresqlExtDatabase('postgres', user='tcl', password='tcl', host="localhost", port=5432, autoconnect=True)


def init():
    with db:
        if not db.table_exists('Chat'):
            db.create_tables([Chat])
            logging.info(u'Table Chat not found, created anew')
        if not db.table_exists('Message'):
            db.create_tables([Message])
            logging.info(u'Table Message not found, created anew')
        if not db.table_exists('User'):
            db.create_tables([User])
            logging.info(u'Table User not found, created anew')


class BaseModel(Model):
    _create_at = DateTimeField(default=datetime.now())
    _modified_at = DateTimeField(default=datetime.now())

    class Meta:
        database = db


class Chat(BaseModel):
    id = BigIntegerField(primary_key=True)
    name = TextField()
    track = BooleanField()
    title = TextField(null=True)

    class Meta:
        db_table = 'chat'


class User(BaseModel):
    id = BigIntegerField()
    username = TextField()
    phone = TextField()
    photo = BlobField(null=True)

    class Meta:
        db_table = 'user'


class Message(BaseModel):
    uid = BigAutoField(primary_key=True)
    id = BigIntegerField()
    version = IntegerField()
    user_id = BigIntegerField(null=True)
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

    def modify(self, message):
        for msg in self.messages:
            if str(msg.id) == str(message.id) and str(msg.chat_id) == str(message.chat_id):
                msg.modify()
                logging.info(u'Modified message. Id: {}, text: {}'.format(msg.id, msg.content))
        self.messages.append(message)

    def delete(self, message):
        for msg in self.messages:
            if str(msg.id) == str(message.id) and str(msg.chat_id) == str(message.chat_id):
                msg.delete_()
                message.chat_id = msg.chat_id
                logging.info(u'Deleted message. Chat: {}, Id: {}, text:{}'.format(msg.chat_id, msg.id, msg.content))
        self.messages.append(message)

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
