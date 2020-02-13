from telethon import TelegramClient, connection, events
from datetime import datetime
import my_objects
import configparser
from flask import Flask, render_template, request
import datetime
from threading import Thread
import ast
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
chat_names = ast.literal_eval(config['Chat']['monitored'])

client = TelegramClient(
    username, api_id, api_hash,
    connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
    proxy=('proxy.mtproto.co', 443, '11112222333344445555666677778888')
)

# Threads
web_ui = Thread(target=app.run, kwargs={'host': '0.0.0.0'})
listener_loop = Thread(target=client.run_until_disconnected)


# Generate and display main page
@app.route('/')
def crutch():
    monitored_chat_id = request.args.get('chat', default=0, type=int)
    viewed_message_id = request.args.get('msg', default=0, type=int)
    global monitors, all_messages
    all_messages = my_objects.Messages.get_all_messages()
    chat_messages = []
    message_versions = []
    for message in all_messages:
        if message.chat_id_id == monitored_chat_id and message.version == 0:
            chat_messages.append(message)
    for message in all_messages:
        if message.id == viewed_message_id:
            message_versions.append(message)
    template_context = dict(name=username, chats=chats, chat_messages=chat_messages, message_versions=message_versions,
                            monitored=monitors)
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
    msg = my_objects.Message(id=message_id, version=0, user_id=user_id, act_date=message_date, create_date=message_date,
                             chat_id=chat_id, state=0, content=message_text)
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
    msg = my_objects.Message(id=message_id, version=0, user_id=user_id, act_date=message_date, create_date=message_date,
                             chat_id=chat_id, state=1, content=message_text)
    all_messages.modify(msg)


@client.on(events.MessageDeleted())
async def message_deleted(event):
    message_text = ''
    user_id = ''
    message_id = str(event.deleted_id)
    message_date = datetime.now()
    chat_id = ''
    print("delete", message_text, user_id, message_id)
    msg = my_objects.Message(id=message_id, version=0, user_id=user_id, act_date=message_date, create_date=message_date,
                             chat_id=chat_id, state=2, content=message_text)
    all_messages.delete(msg)


# if __name__ == "__main__":

client.start()
print('connected')
# Get chats
chats = {}
for chat in client.iter_dialogs():
    chats[chat.id] = chat.name

# Init schema and get messages
my_objects.init()
all_chats = my_objects.Chats(chats, chat_names)
monitors = all_chats.get_monitored()
all_messages = my_objects.Messages()

# input()
listener_loop.start()
web_ui.start()

listener_loop.join()
quit()
web_ui.join()