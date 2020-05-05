from peewee import PeeweeException
from DB.data_access import *
from datetime import datetime

import shutil


# TODO rework front (Max)
# TODO editing configs via UI (with Max)

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
    if event.message.media and not event.message.media.poll:
        filename = str(chat_id) + '_' + message_id
        filename = await client.download_media(event.message, filename)
        shutil.move(filename, dirlist['media'])
        msg_logger.info(u'Media {} saved successfully'.format(filename))
    elif event.message.media.poll:
        message_text = message['media']['poll']['question'] + '\n' + 'SYSTEM: Note, this message will not be updated.'
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

    # to ignore polls. Is still in investigation
    if message['via_bot_id'] != 129782279:
        message_text = message['message']
        user_id = str(message['from_id'])
        message_id = str(message['id'])
        message_date = message['date']
        chat_id = event.message.chat_id
        filename = None
        if event.message.media:
            filename = str(chat_id) + '_' + message_id
            filename = await client.download_media(event.message, filename)
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

    # Check if all monitors are in chats
    for chat in chat_names:
        if chat not in chats.values():
            logging.warning(u'Chat {} was not found in all chats. Removed from monitored.'.format(chat))
            chat_names.remove(chat)

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
