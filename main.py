from peewee import PeeweeException
from telethon import TelegramClient, connection, events
from my_objects import *
import configparser
from datetime import datetime
import ast
import os

# TODO rework save to postgres
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
dirlist = ast.literal_eval(config['Dirs']['List'])

if 'HOSTNAME' in os.environ and os.environ['HOSTNAME'] == 'ruvds-q0byo':
    client = TelegramClient(username, api_id, api_hash)
    logging.info(u'Connecting directly')
else:
    client = TelegramClient(
        username, api_id, api_hash,
        connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
        proxy=('proxy.mtproto.co', 443, '11112222333344445555666677778888')
    )
    logging.info(u'Connecting via MTProxy')

for directory in dirlist:
    if not os.path.exists(directory):
        os.makedirs(directory)


# Listeners
@client.on(events.NewMessage(chats=chat_names))
async def new_message(event):
    message = event.message.to_dict()
    message_text = message['message']
    user_id = str(message['from_id'])
    message_id = str(message['id'])
    message_date = message['date'].strftime("%Y-%m-%d %H:%M:%S")
    chat_id = event.message.chat_id
    media = None
    if event.message.media:
        media = await client.download_media(event.message)
        os.system('mv {} {}/'.format(media, dirlist[1]))
    msg_logger.info(u'New message created. Id: {}, content: {}'.format(message_id, message_text))
    try:
        msg = Message.create(id=message_id, version=0, user_id=user_id, _modified_at=message_date,
                             _create_at=message_date,
                             chat_id=chat_id, state=0, content=message_text, media=media)
        all_messages.add(msg)
    except PeeweeException:
        db_logger.error(u'Failed to save new message. Id :{}, error:{}'.format(message_id, str(PeeweeException)))
        db.close()


@client.on(events.MessageEdited(chats=chat_names))
async def message_edited(event):
    message = event.message.to_dict()
    message_text = message['message']
    user_id = str(message['from_id'])
    message_id = str(message['id'])
    message_date = message['date']
    chat_id = event.message.chat_id
    media = None
    if event.message.media:
        media = await client.download_media(event.message)
        os.system('mv {} {}/'.format(media, dirlist[1]))
    msg_logger.info(u'Message was edited. Id: {}, content: {}'.format(message_id, message_text))
    try:
        msg = Message.create(id=message_id, version=0, user_id=user_id, _modified_at=message_date,
                             _create_at=message_date,
                             chat_id=chat_id, state=0, content=message_text, media=media)
        all_messages.modify(msg)
    except PeeweeException:
        db_logger.error(u'Failed to edit message. Id :{}, error:{}'.format(message_id, str(PeeweeException)))
        db.close()


@client.on(events.MessageDeleted())
async def message_deleted(event):
    message_text = ''
    user_id = ''
    message_id = str(event.deleted_id)
    message_date = datetime.now()
    chat_id = ''
    msg_logger.info(u'Message was deleted. Id: {}, content: {}'.format(message_id, message_text))
    try:
        msg = Message.create(id=message_id, version=0, user_id=user_id, _modified_at=message_date,
                             _create_at=message_date,
                             chat_id=chat_id, state=2, content=message_text)
        all_messages.delete(msg)
    except PeeweeException:
        db_logger.error(u'Failed to delete message. Id: {}, error:{}'.format(message_id, str(PeeweeException)))
        db.close()


if __name__ == "__main__":

    client.start()
    logging.info(u'Connected')
    # Get chats
    chats = {}
    for chat in client.iter_dialogs():
        chats[str(chat.id)] = chat.name
    logging.info(u'Chats loaded from tg')
    # Init schema and get messages
    init()
    logging.info(u'Schema inited')
    all_chats = Chats(chats, chat_names)
    logging.info(u'Chats exported to DB')
    all_messages = Messages()
    logging.info(u'All messages inited')

    client.run_until_disconnected()
