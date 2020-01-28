log = []
log_file = 'db.log'


async def db_log(text):
    f = open(log_file, 'a')
    f.write(text + "\n")
    f.flush()
    global log
    log.append(text)
    print(log)


async def logic_log(text):
    f = open(log_file, 'a')
    f.write(text + "\n")
    f.flush()
    global log
    log.append(text)
    print(log)
