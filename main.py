from telethon import TelegramClient, connection, events
from datetime import datetime
import my_objects
import configparser
from flask import Flask, render_template, request
import datetime
from threading import Thread
from playhouse.sqlite_ext import SqliteExtDatabase

# Init
# Flask
app = Flask(__name__, template_folder="./Front/test/", static_folder="./Front/test/")
app.config["SECRET_KEY"] = "thisissecretkey"

# Connect
config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

client = TelegramClient(
    username, api_id, api_hash,
    connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
    proxy=('Unity-Proxy.dynu.com', 80, 'ddf4359a9b325ff1d1e5084df0e0f7537b')
)

# DB
db = SqliteExtDatabase('peewee.db', pragmas=(
    ('cache_size', -1024 * 64),  # 64MB page-cache.
    ('journal_mode', 'wal'),  # Use WAL-mode (you should always use this!).
    ('foreign_keys', 1),
    ('c_extensions', True)))  # Enforce foreign-key constraints.

# Threads
web_ui = Thread(target=app.run)
listener_loop = Thread(target=client.run_until_disconnected)

# Other
chat_names = ('Это Куэльпорр детка!', 'Зип Зяп и Зюп', 'RT на русском', 'Наш Ривер Парк')


# Generate and display main page
@app.route('/')
def crutch():
    monitored_chat_id = request.args.get('chat', default=0, type=int)
    viewed_message_id = request.args.get('msg', default=0, type=int)
    global monitors, all_messages
    all_messages = my_objects.Messages()
    chat_messages = []
    message_versions = []
    for message in all_messages.messages:
        if message.chat_id == monitored_chat_id and message.version == 0:
            chat_messages.append(message)
    for message in all_messages.messages:
        if message.id == viewed_message_id:
            message_versions.append(message)
    template_context = dict(name=username, chats=chats, chat_messages=chat_messages, message_versions=message_versions,
                            monitored=monitors.chats)
    return render_template('index.html', **template_context)


# Listeners
@client.on(events.NewMessage(chats=chat_names))
async def new_message(event):
    message = event.message.to_dict()
    message_text = message['message']
    user_id = str(message['from_id'])
    message_id = str(message['id'])
    message_date = message['date'].strftime("%Y-%m-%d %H:%M:%S")
    chat_id = event.message.chat_id
    print("new_message", message_text, user_id, message_id)
    msg = my_objects.Message([message_id, 0, user_id, message_date, message_date, chat_id, 0, message_text, None])
    all_messages.add(msg)


@client.on(events.MessageEdited(chats=chat_names))
async def message_edited(event):
    message = event.message.to_dict()
    message_text = message['message']
    user_id = str(message['from_id'])
    message_id = str(message['id'])
    message_date = message['date']
    chat_id = event.message.chat_id
    print("edited", message_text, user_id, message_id)
    msg = my_objects.Message([message_id, 0, user_id, message_date, message_date, chat_id, 1, message_text, None])
    all_messages.modify(msg)


@client.on(events.MessageDeleted())
async def message_deleted(event):
    message_text = ''
    user_id = ''
    message_id = str(event.deleted_id)
    message_date = datetime.now()
    chat_id = ''
    print("delete", message_text, user_id, message_id)
    msg = my_objects.Message([message_id, 0, user_id, message_date, message_date, chat_id, 2, message_text, None])
    all_messages.delete(msg)


# if __name__ == "__main__":

client.start()
# Get chats
chats = {}
for chat in client.iter_dialogs():
    chats[chat.id] = chat.name

# Init schema and get messages
my_objects.init()
all_chats = my_objects.Chats(chats, chat_names)
all_messages = my_objects.Messages()
monitors = all_chats.get_monitored()

# input()
web_ui.start()
listener_loop.start()

web_ui.join()
listener_loop.join()
