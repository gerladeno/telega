import message_db.db_tools
import logger


class Message:

    def __init__(self, id, version=None, user_id=None, act_date=None, create_date=None, chat_id=None, state=None,
                 content=None):
        if version is None:
            self.id = id[0]
            self.version = id[1]
            self.user_id = id[2]
            self.act_date = id[3]
            self.create_date = id[4]
            self.chat_id = id[5]
            self.state = id[6]
            self.content = id[7]
            self.list = id
        else:
            self.id = id
            self.version = version
            self.user_id = user_id
            self.act_date = act_date
            self.create_date = create_date
            self.chat_id = chat_id
            self.state = state
            self.content = content
            self.list = [str(self.id), str(self.version), str(self.user_id), str(self.act_date), str(self.create_date),
                         str(self.chat_id), str(self.state), str(self.content)]

    def recalc(self):
        self.list = [str(self.id), str(self.version), str(self.user_id), str(self.act_date), str(self.create_date),
                     str(self.chat_id), str(self.state), str(self.content)]

    def save(self):
        message_db.db_tools.new_message(self.list)

    def modify(self):
        message_db.db_tools.modify_message(self.list)


class Messages:
    def __init__(self, messages=None):
        if messages is None:
            self.messages = message_db.db_tools.get_messages()
        else:
            self.messages = messages

    def find(self, id):
        for msg in self.messages:
            if msg.id == id:
                return True

    def add(self, message):
        if self.find(message.id):
            logger.logic_log('ERROR: Message with id ' + message.id + ' already exists')
        else:
            self.messages.append(message)
            message.save()

    def modify(self, message):
        for msg in self.messages:
            if str(msg.id) == str(message.id):
                msg.version = msg.version + 1
                msg.state = 1
                msg.recalc()
                msg.modify()
        message.state = 1
        self.messages.append(message)
        message_db.db_tools.new_message(message)

    def delete(self, message):
        for msg in self.messages:
            if str(msg.id) == str(message.id):
                msg.version = msg.version + 1
                msg.state = 2
                msg.recalc()
                msg.modify()
        message.state = 2
        self.messages.append(message)
        message_db.db_tools.new_message(message)
