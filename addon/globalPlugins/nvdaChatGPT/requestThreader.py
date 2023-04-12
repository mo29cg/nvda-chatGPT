# This file is for create a thread and limit the total threads to 1.
from . import convoManager as convoManager
import threading
from . import messenger as messenger


threadObj = None
THREAD_NAME = "askChatGPT"
MAXIMUM_CONVERSATION = 10


def isProcessingOtherQuestion() -> bool:
    for th in threading.enumerate():
        if th.name == "askChatGPT":
            messenger.emitUiMessage(
                "You are already asking something, wait for the response first")

            return True
    return False


def is_conversation_too_long():
    conversation = convoManager.readConversation()
    if "default" in conversation and len(conversation["default"]) > MAXIMUM_CONVERSATION:
        messenger.emitUiMessage(
            "You already asked 10 questions in a conversation, to ask more, re-open the window")
        return True
    return False


def start_thread(target, args, startMessage: str):
    if isProcessingOtherQuestion() or is_conversation_too_long():
        return

    messenger.emitUiMessage(startMessage)

    global threadObj

    threadObj = threading.Thread(
        target=target, args=args, name=THREAD_NAME)

    threadObj.start()
