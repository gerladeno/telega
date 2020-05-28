from peewee import PeeweeException
from DB.data_access import *
from datetime import datetime
import filecmp

import shutil


# Listeners
@client.on(events.NewMessage(chats=chat_names))
async def new_message(event):
    # We get a message, we put it to dict, we parse it.
    message = event.message.to_dict()
    message_text = message['message']
    user_id = str(message['from_id'])
    message_id = str(message['id'])
    message_date = message['date'].strftime("%Y-%m-%d %H:%M:%S")
    chat_id = event.message.chat_id
    filename = None

    # We check, if the message contains media file
    if event.message.media:
        # We check if it is a poll (polls are terrible).
        if hasattr(event.message.media, 'poll'):
            message_text = message['media']['poll'][
                               'question'] + '\n' + 'SYSTEM: Note, this message will not be updated.'
        else:
            filename = os.path.join(dirlist['media'], str(chat_id) + '_' + message_id)
            filename = await client.download_media(event.message, filename)
            filename = str(filename).split('/')[1]
            msg_logger.info(u'Media {} saved successfully'.format(filename))
    msg_logger.info(u'New message created. Id: {}, content: {}'.format(message_id, message_text))
    try:
        # We create a message (this creation automatically creates a corresponding object in database
        # Note that version and state are hardcoded. They are always 0 for a new message
        msg = Message.create(id=message_id, version=0, user_id=user_id, _modified_at=message_date,
                             _create_at=message_date,
                             chat_id=chat_id, state=0, content=message_text, media=filename)
        # We call .add method to also add new message to our in-memory message holder
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
            filename = os.path.join(dirlist['media'], str(chat_id) + '_' + message_id)
            filename = await client.download_media(event.message, filename)
            filename = str(filename)
            msg_logger.info(u'Media {} saved successfully'.format(filename))
        msg_logger.info(u'Message was edited. Id: {}, content: {}'.format(message_id, message_text))
        try:
            # Note that version and state are hardcoded. Version is still 0 (it is always 0 for an actual version),
            # but state is 1. For all versions of edited messages state is 1
            msg = Message.create(id=message_id, version=0, user_id=user_id, _modified_at=message_date,
                                 _create_at=message_date,
                                 chat_id=chat_id, state=1, content=message_text, media=filename)
            all_messages.modify(msg)
        except PeeweeException:
            db_logger.error(u'Failed to edit message. Id :{}, error:{}'.format(message_id, str(PeeweeException)))
            db.close()


# Never mind. Delete sucks.
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
    # Init all_chats - our chat holder
    all_chats = Chats(chats, chat_names)
    chat_names = Chats.get_monitored()
    logging.info(u'Chats exported to DB')
    # Init all_messages - our message holder
    all_messages = Messages()
    logging.info(u'All messages inited')
    print("started")
    # Endless event-loop
    client.run_until_disconnected()
