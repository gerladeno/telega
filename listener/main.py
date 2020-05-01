from peewee import PeeweeException
from DB.data_access import *
from datetime import datetime

import shutil


# TODO rework file storage (not in the container)
# TODO rework front (Max)
# TODO place config outside of containers
# TODO share logs
# TODO create a page with system information
# TODO editing configs via UI

# Listeners
@client.on(events.NewMessage(chats=chat_names))
async def new_message(event):
    message = event.message.to_dict()
    message_text = message['message']
    user_id = str(message['from_id'])
    message_id = str(message['id'])
    message_date = message['date'].strftime("%Y-%m-%d %H:%M:%S")
    chat_id = event.message.chat_id
    filename = None
    if event.message.media:
        filename = await client.download_media(event.message)
        shutil.move(filename, dirlist['media'])
        msg_logger.info(u'Media {} saved successfully'.format(filename))
    msg_logger.info(u'New message created. Id: {}, content: {}'.format(message_id, message_text))
    try:
        msg = Message.create(id=message_id, version=0, user_id=user_id, _modified_at=message_date,
                             _create_at=message_date,
                             chat_id=chat_id, state=0, content=message_text, media=filename)
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
    filename = None
    if event.message.media:
        filename = await client.download_media(event.message)
        shutil.move(filename, dirlist['media'])
        msg_logger.info(u'Media {} saved successfully'.format(filename))
    msg_logger.info(u'Message was edited. Id: {}, content: {}'.format(message_id, message_text))
    try:
        msg = Message.create(id=message_id, version=0, user_id=user_id, _modified_at=message_date,
                             _create_at=message_date,
                             chat_id=chat_id, state=1, content=message_text, media=filename)
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
    client.start(password=password)
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
    chat_names = Chats.get_monitored()
    logging.info(u'Chats exported to DB')
    all_messages = Messages()
    logging.info(u'All messages inited')
    print("started")
    client.run_until_disconnected()
