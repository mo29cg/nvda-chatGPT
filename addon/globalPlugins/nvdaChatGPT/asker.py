import config

from openai.error import RateLimitError, AuthenticationError, ServiceUnavailableError
from revChatGPT.Official import Chatbot
import ui
import queueHandler
module = "askChatGPT"


def getConfig(key):
    value = config.conf[module][key]
    return value


def createAskMeaning(word):
    outputLanguageIndex = getConfig("outputLanguageIndex")

    if (outputLanguageIndex == 0):
        return "What is the meaning of " + word + "? Respond in english"
    elif (outputLanguageIndex == 1):
        return word + "とはどういう意味ですか、返答は日本語でお願いします"


def askChatGPT(text, functionStartMessage):
    # Apparently ui.message doesn'T work in threads with a braille display, and this is how to make it work.

    chatbot = Chatbot(
        api_key=getConfig("apiKey"))
    try:
        response = chatbot.ask(text)
        queueHandler.queueFunction(
            queueHandler.eventQueue, ui.browseableMessage, response["choices"][0]["text"])
        # ui.browseableMessage(response["choices"][0]["text"])
    except (RateLimitError, ServiceUnavailableError):
        queueHandler.queueFunction(
            queueHandler.eventQueue, ui.message, "the server is busy, try again later")
    except (AuthenticationError):
        queueHandler.queueFunction(
            queueHandler.eventQueue, ui.message, "The api key is incorrect, set a correct one..")
