from .promptOption import EnumPromptOption
import config
from openai.error import RateLimitError, AuthenticationError, ServiceUnavailableError
from revChatGPT.V3 import Chatbot
import ui
import queueHandler
import markdown2
import threading


module = "askChatGPT"
threadObj = None
THREAD_NAME = "askChatGPT"


def getConfig(key):
    value = config.conf[module][key]
    return value


def createAskMeaningPrompt(word):

    languagesModels = [
        "What is the meaning of {}? Respond in Chinese",
        "What is the meaning of {}? Respond in English",
        "What is the meaning of {}? Respond in Italian",
        "{}とはどういう意味ですか、返答は日本語でお願いします",
        "What is the meaning of {}? Respond in Korean",
        "What is the meaning of {}? Respond in Portuguese",
        "What is the meaning of {}? Respond in Spanish",
        "What is the meaning of {}? Respond in Turkish",
    ]
    outputLanguageIndex = getConfig("outputLanguageIndex")

    return languagesModels[outputLanguageIndex].format(word)


def askChatGPT(prompt: str, functionStartMessage):

    # Apparently ui.message doesn'T work in threads with a braille display, and this is how to make it work.
    queueHandler.queueFunction(
        queueHandler.eventQueue, ui.message, functionStartMessage)

    chatbot = Chatbot(
        api_key=getConfig("apiKey"))
    try:
        response = chatbot.ask(prompt)
        queueHandler.queueFunction(
            queueHandler.eventQueue, ui.browseableMessage, markdown2.markdown(response, extras=["fenced-code-blocks"]), isHtml=True)
    except (RateLimitError, ServiceUnavailableError):
        queueHandler.queueFunction(
            queueHandler.eventQueue, ui.message, "the server is busy, try again later")
    except (AuthenticationError):
        queueHandler.queueFunction(
            queueHandler.eventQueue, ui.message, "The api key is incorrect, set a correct one..")


def isProcessingOtherQuestion() -> bool:
    runningThreads = threading.enumerate()
    for th in runningThreads:
        if th.name == "askChatGPT":
            queueHandler.queueFunction(
                queueHandler.eventQueue, ui.message, "You are already asking something, wait for the response first")
            return True
    return False


def startThreadOfRequesting(promptOption: EnumPromptOption, input: str):
    if isProcessingOtherQuestion():
        return

    global threadObj
    if promptOption == EnumPromptOption.ASKMEANINGOF:
        threadObj = threading.Thread(
            target=askChatGPT, args=(createAskMeaningPrompt(input), "asking the Weaning to chatGPT"), name=THREAD_NAME)
    elif promptOption == EnumPromptOption.ASKSENTENCE:
        threadObj = threading.Thread(
            target=askChatGPT, args=(input, "asking the sentence to chatGPT"), name=THREAD_NAME)

    threadObj.start()
