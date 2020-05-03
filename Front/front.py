import DB.data_access as my_objects
from flask import Flask, render_template, request, url_for, send_file
import logging
import os
import subprocess
import json

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
    all_messages = my_objects.Messages.get_sorted_messages(days=my_objects.days)
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


@app.route('/media/')
def media():
    name = request.args.get('media', default=0, type=str)
    filename = os.path.join('../media/', name)
    return send_file(filename, as_attachment=True)


@app.route('/status/')
def status():
    df = ''
    volumes = []
    top = ''
    inspect = ''
    try:
        du = {'logs': subprocess.check_output('du -d 0 -h /opt/tcl/logs/', shell=True),
              'media': subprocess.check_output('du -d 0 -h /opt/tcl/media/', shell=True),
              'postgres': subprocess.check_output('du -d 0 -h /var/lib/postgresql/data/', shell=True)}
    except Exception:
        du = {}
    # df = subprocess.check_output('df -h', shell=True)
    # top = subprocess.check_output('top -b -n 1', shell=True)
    # volumes = subprocess.check_output('docker volume ls -q', shell=True).splitlines()
    # volumes = [a.decode() for a in volumes]
    # inspect = {}
    # for v in volumes:
    #     inspect[v] = json.dumps(json.loads(subprocess.check_output("docker volume inspect {}".format(v), shell=True)),
    #                             indent=2)

    # Config
    config = my_objects.config._sections.copy()
    config.pop('Telegram')
    config.pop('DB')

    # DB
    db_stats = my_objects.Messages.get_statistics()

    template_context = dict(df=df, top=top, volumes=volumes, inspect=inspect, config=config, db_stats=db_stats, du=du)
    return render_template('status.html', **template_context)


app.run(host='0.0.0.0')
