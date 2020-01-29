from telethon import TelegramClient, sync, connection, events
from datetime import datetime
import message_db.db_tools
import my_objects
import os
import configparser
import json

config = configparser.ConfigParser()
config.read("config.ini")

api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

client = TelegramClient(
    'Testing MyTCL', api_id, api_hash,
    connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
    proxy=('russia-dd.proxy.digitalresistance.dog', 443, 'ddd41d8cd98f00b204e9800998ecf8427e')
)

chat_names = ('Это Куэльпорр детка!', 'Зип Зяп и Зюп', 'RT на русском')


@client.on(events.NewMessage(chats=chat_names))
async def new_message(event):
    message = event.message.to_dict()
    message_text = message['message']
    user_id = str(message['from_id'])
    message_id = str(message['id'])
    message_date = message['date'].strftime("%Y-%m-%d %H:%M:%S")
    chat_id = event.message.chat_id
    msg = my_objects.Message([message_id, 0, user_id, message_date, message_date, chat_id, 0, message_text])
    all_messages.add(msg)


@client.on(events.MessageEdited(chats=chat_names))
async def message_edited(event):
    message = event.message.to_dict()
    message_text = message['message']
    user_id = str(message['from_id'])
    message_id = str(message['id'])
    message_date = message['date']
    chat_id = event.message.chat_id
    msg = my_objects.Message([message_id, 0, user_id, message_date, message_date, chat_id, 1, message_text])
    all_messages.modify(msg)


@client.on(events.MessageDeleted())
async def message_deleted(event):
    message_text = ''
    user_id = ''
    message_id = str(event.deleted_id)
    message_date = datetime.now()
    chat_id = ''
    if all_messages.find(message_id):
        msg = my_objects.Message([message_id, 0, user_id, message_date, message_date, chat_id, 2, message_text])
        all_messages.delete(msg)


# if __name__ == "__main__":

client.start()
# Get chats
chats = {}
for chat in client.iter_dialogs():
    chats[chat.id] = chat.name

# Init schema and get messages
message_db.db_tools.init(chats, chat_names)
all_messages = my_objects.Messages()

client.run_until_disconnected()
