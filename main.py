from peewee import PeeweeException
from telethon import TelegramClient, connection, events
from my_objects import *
import configparser
import datetime
import ast

# TODO rework save to postgres
# TODO detach web-ui into separate program
# TODO rework front
# TODO no crash on chat rename
# TODO receive and save media
# TODO get old messages

# Connect
config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']
chat_names = ast.literal_eval(config['Chat']['monitored'])

client = TelegramClient(
    username, api_id, api_hash,
    connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
    proxy=('proxy.mtproto.co', 443, '11112222333344445555666677778888')
)


# Listeners
@client.on(events.NewMessage(chats=chat_names))
async def new_message(event):
    message = event.message.to_dict()
    message_text = message['message']
    user_id = str(message['from_id'])
    message_id = str(message['id'])
    message_date = message['date'].strftime("%Y-%m-%d %H:%M:%S")
    chat_id = event.message.chat_id
    logging.debug("new_message", message_text, user_id, message_id)
    try:
        msg = Message.create(id=message_id, version=0, user_id=user_id, _modified_at=message_date,
                             _create_at=message_date,
                             chat_id=chat_id, state=0, content=message_text)
        all_messages.add(msg)
    except PeeweeException:
        logging.error("Failed to save new message. Id :{}, text:{}".format(message_id, message_text))


@client.on(events.MessageEdited(chats=chat_names))
async def message_edited(event):
    message = event.message.to_dict()
    message_text = message['message']
    user_id = str(message['from_id'])
    message_id = str(message['id'])
    message_date = message['date']
    chat_id = event.message.chat_id
    logging.debug("edited", message_text, user_id, message_id)
    try:
        msg = Message.create(id=message_id, version=0, user_id=user_id, _modified_at=message_date,
                             _create_at=message_date,
                             chat_id=chat_id, state=1, content=message_text)
        all_messages.modify(msg)
    except PeeweeException:
        logging.error("Failed to edit message. Id :{}, text:{}".format(message_id, message_text))


@client.on(events.MessageDeleted())
async def message_deleted(event):
    message_text = ''
    user_id = ''
    message_id = str(event.deleted_id)
    message_date = datetime.now()
    chat_id = ''
    logging.debug("delete", message_text, user_id, message_id)
    try:
        msg = Message.create(id=message_id, version=0, user_id=user_id, _modified_at=message_date,
                             _create_at=message_date,
                             chat_id=chat_id, state=2, content=message_text)
        all_messages.delete(msg)
    except PeeweeException:
        logging.error("Failed to delete message. Id: {}, text: {}".format(message_id, message_text))


# if __name__ == "__main__":

client.start()
logging.info('connected')
# Get chats
chats = {}
for chat in client.iter_dialogs():
    chats[chat.id] = chat.name
logging.info('Chats loaded from tg')
# Init schema and get messages
init()
logging.info('Schema inited')
all_chats = Chats(chats, chat_names)
logging.info('Chats exported to DB')
all_messages = Messages()
logging.info('All messages inited')

client.run_until_disconnected()
