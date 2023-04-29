# This file is for create a thread and limit the total threads to 1.
from . import convoManager as convoManager
import threading
from . import messenger as messenger
import wx


threadObj = None
THREAD_NAME = "askChatGPT"


def isProcessingOtherQuestion() -> bool:
    for th in threading.enumerate():
        if th.name == "askChatGPT":
            messenger.emitUiMessage(
                "You are already asking something, wait for the response first")

            return True
    return False


def start_thread(target, args, startMessage: str):
    if isProcessingOtherQuestion():
        return

    messenger.emitUiMessage(startMessage)

    global threadObj

    threadObj = threading.Thread(
        target=target, args=args, name=THREAD_NAME)

    threadObj.start()
