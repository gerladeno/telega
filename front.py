import my_objects
from flask import Flask, render_template, request
import configparser
import ast

# Init
# Flask
app = Flask(__name__, template_folder="./Front/test/", static_folder="./Front/test/")
app.config["SECRET_KEY"] = "thisissecretkey"

config = configparser.ConfigParser()
config.read("config.ini")
username = config['Telegram']['username']
chat_names = ast.literal_eval(config['Chat']['monitored'])


# Generate and display main page
@app.route('/')
def crutch():
    monitored_chat_id = request.args.get('chat', default=0, type=int)
    viewed_message_id = request.args.get('msg', default=0, type=int)
    monitors = my_objects.Chats.get_monitored()
    all_messages = my_objects.Messages.get_all_messages()
    chat_messages = []
    message_versions = []
    for message in all_messages:
        if message.chat_id_id == monitored_chat_id and message.version == 0:
            chat_messages.append(message)
    for message in all_messages:
        if message.id == viewed_message_id:
            message_versions.append(message)
    template_context = dict(name=username, chat_messages=chat_messages, message_versions=message_versions,
                            monitored=monitors)
    return render_template('index.html', **template_context)


app.run(host='0.0.0.0')
