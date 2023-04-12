import threading
debug = False


if debug:
    LOG_FILE_NAME = "C:\\Users\\suzuki\\TerminalOutputs\\firstLog.json"
    f = open(LOG_FILE_NAME, "w")
    f.close()
    LOG_MUTEX = threading.Lock()


def mylog(s):
    with LOG_MUTEX:
        f = open(LOG_FILE_NAME, "a", encoding='utf-8')
        print(s, file=f)
        f.close()
