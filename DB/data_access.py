from DB.my_objects import *

class Messages:
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
        q = Message\
            .select()\
            .where(Message._modified_at >= dt)\
            .order_by(Message._modified_at.asc(), Message.version.asc())
        for item in q:
            messages.append(item)
        return messages


class Chats:
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