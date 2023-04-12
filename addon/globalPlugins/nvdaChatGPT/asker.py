from . import languages as languages
from . import messenger as messenger
from . import configManager as configManager
from . import convoManager as convoManager
from .myLog import mylog
from revChatGPT.V3 import Chatbot


def createAskMeaningPrompt(word):

    outputLanguageIndex = configManager.getConfig("outputLanguageIndex")

    return languages.ASK_MEANING_PROMPT_MODELS[outputLanguageIndex].format(word)


def askChatGPT(prompt: str, chatbot: Chatbot = None):

    if chatbot == None:
        chatbot = Chatbot(
            api_key=configManager.getConfig("apiKey"))
    try:
        response = chatbot.ask(prompt)

    # revChatGPT is not setting type for Exceptions currently, we need more efforts to handle errors well.
    except Exception as e:
        mylog(e)
        messenger.emitUiMessage(
            "The api key is incorrect, set a correct one!")
        return

    messenger.emitUiBrowseableMessage(response)
