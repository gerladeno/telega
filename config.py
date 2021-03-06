import configparser
import ast
import logging
import logging.handlers
import os
from telethon import TelegramClient, connection, events
from telethon.tl.functions.channels import JoinChannelRequest

# Configs
config = configparser.ConfigParser()

try:
    config.read("./config/config.ini")
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    username = config['Telegram']['username']
    password = config['Telegram']['password']
    chat_names = ast.literal_eval(config['Chat']['monitored'])
    dirlist = ast.literal_eval(config['Dirs']['List'])
    env = config['Proxy']['env']
    proxy_site = config['Proxy']['site']
    proxy_port = int(config['Proxy']['port'])
    proxy_secret = config['Proxy']['secret']
    db_host = config['DB']['host']
    db_user = config['DB']['user']
    db_password = config['DB']['password']
    days = int(config['Front']['days_to_display'])
except Exception:
    logging.warning(u'No config file with proper settings found. Starting with default settings')
    api_id = 1033718
    api_hash = '4752738f1f604ad5d1878ce1cd2de907'
    username = 'Telegram Chat Listener'
    password = None
    chat_names = ("Telegram", "MarketTwits")
    dirlist = {'logs': "logs", 'media': "media", 'config': "config"}
    env = 'dev'
    proxy_site = 'proxy.mtproto.co'
    proxy_port = 443
    proxy_secret = '11112222333344445555666677778888'
    db_host = 'localhost'
    db_user = 'tcl'
    db_password = 'tcl'
    days = 7

for directory in dirlist:
    if not os.path.exists(dirlist[directory]):
        os.makedirs(dirlist[directory])

# Config loggers
CONNECTION_LOG_FILENAME = dirlist['logs'] + u'/connect.log'
MSG_LOG_FILENAME = dirlist['logs'] + u'/msg.log'
DB_LOG_FILENAME = dirlist['logs'] + u'/db.log'

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO,
                    filename=CONNECTION_LOG_FILENAME)

formatter = logging.Formatter(u'%(levelname)-8s [%(asctime)s] %(message)s')

handler = logging.handlers.TimedRotatingFileHandler(MSG_LOG_FILENAME, when='D', interval=7)
msg_logger = logging.getLogger('TCL')
msg_logger.setLevel(logging.INFO)
msg_logger.addHandler(handler)
msg_logger.propagate = False
handler.setFormatter(formatter)

handler = logging.handlers.TimedRotatingFileHandler(DB_LOG_FILENAME, when='D', interval=7)
db_logger = logging.getLogger('DB')
db_logger.setLevel(logging.INFO)
db_logger.addHandler(handler)
db_logger.propagate = False
handler.setFormatter(formatter)

# Set connection

if env == 'PROD':
    client = TelegramClient(username, api_id, api_hash)
    logging.info(u'Connecting directly')
else:
    client = TelegramClient(
        username, api_id, api_hash,
        connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
        proxy=(proxy_site, proxy_port, proxy_secret)
    )
    logging.info(u'Connecting via MTProxy')

# This is a code to join channels via API (instead of adding them manually).
# Also uncomment two last strings in this file
# Join channels
# from telethon.sync import TelegramClient, connection, events
# ls = ['@Burovaia', '@internet_people', '@russianmacro', '@AK47pfl', '@breakingmash', '@banksta', '@trubapodneglinnoy',
#       '@cbrstocks', '@boilerroomchannel']


def join(channel):
    channel_entity = client.get_entity(channel)
    client(JoinChannelRequest(channel_entity))


# This is a code to connect to Telegram if config.py is run explicitly
# python config.py
if __name__ == "__main__":
    client.start(password=password)
    logging.info(u'Connected')

    # for item in ls:
    #     join(item)
