from telethon import TelegramClient, connection, events
from datetime import datetime
import message_db.db_tools
import my_objects
import configparser
from flask import Flask, render_template
from jinja2 import Template
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "thisissecretkey"


@app.route('/')
def crutch():
    template_context = dict(name=username, chats=chats, messages=all_messages, monitored=chat_names)
    return render_template('Front/test/index.html', **template_context)


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

chat_names = ('Это Куэльпорр детка!', 'Зип Зяп и Зюп', 'RT на русском')


@client.on(events.NewMessage(chats=chat_names))
async def new_message(event):
    message = event.message.to_dict()
    message_text = message['message']
    user_id = str(message['from_id'])
    message_id = str(message['id'])
    message_date = message['date'].strftime("%Y-%m-%d %H:%M:%S")
    chat_id = event.message.chat_id
    print("new_message", message_text, user_id, message_id)
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
    print("edited", message_text, user_id, message_id)

    msg = my_objects.Message([message_id, 0, user_id, message_date, message_date, chat_id, 1, message_text])
    all_messages.modify(msg)


@client.on(events.MessageDeleted())
async def message_deleted(event):
    message_text = ''
    user_id = ''
    message_id = str(event.deleted_id)
    message_date = datetime.now()
    chat_id = ''
    print("delete", message_text, user_id, message_id)
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
monitors = my_objects.MonitoredChats()

# input()
app.run(debug=True)
client.run_until_disconnected()
