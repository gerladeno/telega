from DB.my_objects import *


# Message holder
class Messages:
    """
    This is a class, which is just a list of messages.

    Constructor.
    We create a list of messages by selecting them all from DB
    (there is an if-else clause, but we currently never get to else, there is no such code here).

    add. We just append e new message to the list

    modify. We do not ever modify any messages. We create new version. We call msg.modify()
    (a method of a message-object) to only change version and state (0 - new message, 1 - edited message,
    2 - deleted message). And we append a new message to our list

    delete. The idea is the same: change version and state and create a new message, with notion, that this message
    mas deleted. However delete part doesn't work properly.

    static methods here are to obvious to comment

    """
    messages = []

    def __init__(self, messages=None):
        self.messages = []
        if messages is None:
            q = Message.select()
            for msg in q:
                self.messages.append(msg)
        else:
            self.messages = messages

    def add(self, message):
        self.messages.append(message)
        db_logger.info(u'Created new message. Id: {}, text: {}'.format(message.id, message.content))

    def modify(self, message):
        for msg in self.messages:
            if msg.id == message.id and msg.chat_id == message.chat_id:
                msg.modify()
                db_logger.info(u'Modified message. Id: {}, text: {}'.format(msg.id, msg.content))
        self.messages.append(message)

    def delete(self, message):
        for msg in self.messages:
            if msg.id == message.id and msg.chat_id == message.chat_id:
                msg.delete_()
                message.chat_id = msg.chat_id
                db_logger.info(u'Deleted message. Chat: {}, Id: {}, text:{}'.format(msg.chat_id, msg.id, msg.content))
        self.messages.append(message)

    @staticmethod
    def get_all_messages():
        messages = []
        q = Message.select()
        for msg in q:
            messages.append(msg)
        return messages

    @staticmethod
    def get_sorted_messages(days=7):
        messages = []
        dt = datetime.now() - timedelta(days=days)
        q = Message \
            .select() \
            .where(Message._modified_at >= dt) \
            .order_by(Message._modified_at.asc(), Message.version.asc())
        for item in q:
            messages.append(item)
        return messages

    @staticmethod
    def get_statistics():
        chats = []
        q = Message \
            .select(Message.chat_id, fn.COUNT(Message.id).alias('Msg_count')) \
            .where(Message.version == 0) \
            .group_by(Message.chat_id_id)

        for item in q:
            chats.append([item.chat_id.name, item.Msg_count])
        return chats


class Chats:
    """
    The idea is pretty much the same as with messages: a simple list, that holds all the chats

    Constructor is a bit tricky, because we have to check the flag if a chat is monitored or not (that's what all those
    ifs and elses are bout).
    """
    chats = []

    def __init__(self, chats, monitored):
        all_chats = self.get_all_chats()
        monitored_chats = self.get_monitored()
        for chat in chats:
            if chat not in all_chats:
                if chats[chat] in monitored:
                    item = Chat.create(id=chat, name=chats[chat], track=True)
                    self.chats.append(item)
                else:
                    item = Chat.create(id=chat, name=chats[chat], track=False)
                    self.chats.append(item)
            else:
                if chats[chat] in monitored and chat not in monitored_chats:
                    Chat.update({Chat.track: True}).where(Chat.id == chat).execute()
                elif chats[chat] not in monitored and chat in monitored_chats:
                    Chat.update({Chat.track: False}).where(Chat.id == chat).execute()

    @staticmethod
    def get_monitored():
        monitored = {}
        q = (Chat.select().where(Chat.track == True))
        for chat in q:
            monitored[chat.id] = chat.name
        return monitored

    @staticmethod
    def get_all_chats():
        chats = {}
        q = (Chat.select())
        for chat in q:
            chats[chat.id] = chat.name
        return chats
