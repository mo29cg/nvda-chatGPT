import threading
debug = True


if debug:
    LOG_FILE_NAME = "C:\\Users\\suzuki\\TerminalOutputs\\firstLog.json"
    f = open(LOG_FILE_NAME, "w")
    f.close()
    LOG_MUTEX = threading.Lock()


def mylog(s):
    with LOG_MUTEX:
        f = open(LOG_FILE_NAME, "a", encoding='utf-8')
        print(s, file=f)
        # f.write(s.encode('UTF-8'))
        # f.write('\n')
        f.close()


# debug = False
# if debug:
#     import threading
#     LOG_FILE_NAME = "C:\\Users\\tony\\Dropbox\\1.txt"
#     f = open(LOG_FILE_NAME, "w")
#     f.close()
#     LOG_MUTEX = threading.Lock()

#     def mylog(s):
#         with LOG_MUTEX:
#             f = open(LOG_FILE_NAME, "a", encoding='utf-8')
#             print(s, file=f)
#             # f.write(s.encode('UTF-8'))
#             # f.write('\n')
#             f.close()
# else:
#     def mylog(*arg, **kwarg):
#         pass
