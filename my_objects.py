from datetime import datetime
from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase
import logging
import logging.handlers

CONNECTION_LOG_FILENAME = u'logs/connect.log'
MSG_LOG_FILENAME = u'logs/msg.log'
DB_LOG_FILENAME = u'logs/db.log'

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO,
                    filename=CONNECTION_LOG_FILENAME)

formatter = logging.Formatter(u'%(levelname)-8s [%(asctime)s] %(message)s')

handler = logging.handlers.TimedRotatingFileHandler(MSG_LOG_FILENAME)
msg_logger = logging.getLogger('TCL')
msg_logger.setLevel(logging.INFO)
msg_logger.addHandler(handler)
msg_logger.propagate = False
handler.setFormatter(formatter)

handler = logging.handlers.TimedRotatingFileHandler(DB_LOG_FILENAME)
db_logger = logging.getLogger('DB')
db_logger.setLevel(logging.INFO)
db_logger.addHandler(handler)
db_logger.propagate = False
handler.setFormatter(formatter)

# DB
db = PostgresqlExtDatabase('postgres', user='tcl', password='tcl', host="localhost", port=5432, autoconnect=True)


def init():
    with db:
        if not db.table_exists('chat', 'tcl'):
            db.create_tables([Chat])
            db_logger.info(u'Table Chat not found, created anew')
        if not db.table_exists('message', 'tcl'):
            db.create_tables([Message])
            db_logger.info(u'Table Message not found, created anew')
        if not db.table_exists('user', 'tcl'):
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
        db_logger.info(u'Created new message. Id: {}, text: {}'.format(message.id, message.content))

    def modify(self, message):
        for msg in self.messages:
            if msg.id == message.id and msg.chat_id == message.chat_id:
                msg.modify()
                db_logger.info(u'Modified message. Id: {}, text: {}'.format(msg.id, msg.content))
        self.messages.append(message)

    def delete(self, message):
        for msg in self.messages:
            if msg.id == message.id and msg.chat_id == message.chat_id:
                msg.delete_()
                message.chat_id = msg.chat_id
                db_logger.info(u'Deleted message. Chat: {}, Id: {}, text:{}'.format(msg.chat_id, msg.id, msg.content))
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
