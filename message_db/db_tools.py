import os
import sqlite3
import logger
import my_objects

db_filename = 'schema.db'
create_schema_file = 'message_db/create_schema.sql'


def init(chats, monitored_chats):
    db_is_new = not os.path.exists(db_filename)

    with sqlite3.connect(db_filename) as connection:

        if db_is_new:
            logger.db_log('DB not found')
            logger.db_log('Creating schema...')
            try:
                with open(create_schema_file, 'rt') as f:
                    schema = f.read()
                connection.executescript(schema)
                logger.db_log('Schema created with file ' + create_schema_file)
            except (FileNotFoundError, IOError):
                logger.db_log('ERROR: File not found, creation failed')

            for chat in chats:
                name = chats[chat].replace("'", "''")
                insert = "insert into chat (id, name) values(" + str(chat) + ",'" + name + "')"
                connection.execute(insert)

            connection.commit()
            logger.db_log('Insert chat successful')

            for chat in monitored_chats:
                name = chat.replace("'", "''")
                insert = "insert into monitored_chat (id, name) select * from chat " \
                         "where name='" + name + "'"
                try:
                    connection.execute(insert)
                except sqlite3.DatabaseError:
                    logger.db_log("ERROR: " + name + ' is not in chat list')
            connection.commit()
            logger.db_log('Insert monitored_chat successful')

        else:
            logger.db_log('Database exists, assume schema does, too.')
    connection.close()


def update(chats, monitored_chats):
    with sqlite3.connect(db_filename) as connection:
        if not chats:
            connection.execute("delete from monitored_chat")
            connection.commit()
            logger.db_log('Monitored_chat table emptied')
        else:
            connection.execute("delete from monitored_chat")
            connection.execute("delete from chat")
            connection.commit()
            logger.db_log('Chat tables emptied')
            for chat in chats:
                name = chats[chat].replace("'", "''")
                insert = "insert into chat (id, name) values(" + str(chat) + ",'" + name + "')"
                connection.execute(insert)

            connection.commit()
            logger.db_log('Update chat successful')

        for chat in monitored_chats:
            name = chat.replace("'", "''")
            insert = "insert into monitored_chat (id, name) select * from chat " \
                     "where name='" + name + "'"
            try:
                connection.execute(insert)
            except sqlite3.DatabaseError:
                logger.db_log(name + ' is not in chat list')
        connection.commit()
        logger.db_log('Monitored_chat update successful')
    connection.close()


def new_message(message):
    with sqlite3.connect(db_filename) as connection:
        c = connection.cursor()
        c.execute('select id from message where id = ?', (message[0],))
        connection.execute(
            'insert into message (id, version, user_id, act_date, create_date, chat_id, state, content)'
            ' values(?,?,?,?,?,?,?,?)',
            message)
        connection.commit()
        logger.db_log('Message with ID ' + message[0] + ' created')
    connection.close()


def get_messages(ids=None):
    msg_list = []
    with sqlite3.connect(db_filename) as connection:
        c = connection.cursor()
        if not ids:
            c.execute('select * from message')
            for msg in c.fetchall():
                msg_list.append(my_objects.Message(list(msg)))
        else:
            string = "select * from message where id in ("
            for id in ids:
                string = string + str(id) + ','
            string = string[:-1] + ')'
            c.execute(string)
            for msg in c.fetchall():
                msg_list.append(my_objects.Message(list(msg)))
    connection.close()
    return msg_list


def modify_message(message):
    with sqlite3.connect(db_filename) as connection:
        c = connection.cursor()
        c.execute('select id from message where id=?', (message[0],))
        flag = bool(c.fetchall())
        if flag:
            connection.execute(
                'update message set id = ?, version = ?, user_id = ?, act_date = ?, ' +
                'create_date = ?, chat_id = ?, state = ?, content = ?'
                ,
                message)
            connection.commit()
            logger.db_log('Message with ID ' + str(message[0]) + ' modified')
        else:
            logger.db_log('Message with ID ' + str(message[0]) + ' not found, thus it was not modified')
    connection.close()


def delete_message(ids, version=None):
    with sqlite3.connect(db_filename) as connection:
        if not version:
            string = "delete from message where id in ("
            for id in ids:
                string = string + str(id) + ','
            string = string[:-1] + ')'
            connection.execute(string)
        else:
            connection.execute('delete from message where id = ? and version = ?')
        connection.commit()
    connection.close()


def load_chats():
    with sqlite3.connect(db_filename) as connection:
        c = connection.cursor()
        c.execute('select * from chat')
        res = c.fetchall()
    connection.close()
    return res


def load_monitored_chats():
    with sqlite3.connect(db_filename) as connection:
        c = connection.cursor()
        c.execute('select * from monitored_chat')
        res = c.fetchall()
    connection.close()
    return res
