import DB.data_access as my_objects
from flask import Flask, render_template, request, url_for, send_file
import configparser
import ast
import logging
import os

FRONT_LOG_FILENAME = u'logs/front.log'

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO,
                    filename=FRONT_LOG_FILENAME)

# Init Flask
app = Flask(__name__, template_folder="resources/", static_folder="resources/")


# Generate and display main page
@app.route('/')
def main():
    monitored_chat_id = request.args.get('chat', default=0, type=str)
    monitors = my_objects.Chats.get_monitored()
    all_messages = my_objects.Messages.get_sorted_messages(7)
    chat_messages = []
    msg_list = []
    for message in all_messages:
        if message.chat_id_id == monitored_chat_id:
            if message.state == 0:
                chat_messages.append(message)
                msg_list.append(message.id)
            elif message.id not in msg_list:
                tmp = []
                msg_list.append(message.id)
                for msg in all_messages:
                    if msg.id == message.id:
                        tmp.append(msg)
                chat_messages.append(tmp)
    template_context = dict(name=my_objects.username, chat_messages=chat_messages, monitored=monitors)
    page = render_template('index.html', **template_context)
    return page


@app.route('/logs/')
def logs():
    log_files = os.listdir('logs')
    path = os.path.abspath('logs')
    template_context = dict(log_files=log_files, path=path)
    return render_template('logs.html', **template_context)


@app.route('/file/')
def file():
    name = request.args.get('file', default=0, type=str)
    filename = os.path.join('../logs/', name)
    return send_file(filename, as_attachment=True)


app.run(host='0.0.0.0')
