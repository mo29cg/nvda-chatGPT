import addonHandler
from . import (
    languages as languages,
    messenger as messenger,
    configManager as configManager,
)
from . import convoManager as convoManager
from .myLog import mylog
from revChatGPT.V3 import Chatbot
from . import utils as utils
import json
from . import instructions as instructions
from .utils import initTranslationWithErrorHandling

initTranslationWithErrorHandling()


def createAskMeaningPrompt(word):
    outputLanguageIndex = configManager.getConfig("outputLanguageIndex")

    return languages.ASK_MEANING_PROMPT_MODELS[outputLanguageIndex].format(word)


def askChatGPT(prompt: str, chatbot: Chatbot = None):
    if chatbot == None:
        chatbot = Chatbot(api_key=configManager.getConfig("apiKey"))
    try:
        response = chatbot.ask(prompt)

    # revChatGPT is not setting type for Exceptions currently, we need more efforts to handle errors well.
    except Exception as e:
        errorText = utils.extract_json_from_exception(str(e))
        errorJson = json.loads(errorText)
        errorType = errorJson["error"]["type"]
        if errorType == "invalid_request_error":
            messenger.emitUiBrowseableMessage(instructions.API_KEY_INCORRECT_ERROR)
        elif errorType == "insufficient_quota":
            messenger.emitUiBrowseableMessage(instructions.INSUFFICIENT_QUOTA_ERROR)
        else:
            unexpectedErrorMessage = _(
                # Translators: Message when it encounter an unexpected error, the error itself will be shown below this.
                "Unexpected error occured. Please send the error message below to the add-on author's email address, lcong5946@gmail.com \n\n "
            )
            messenger.emitUiBrowseableMessage(unexpectedErrorMessage + str(e))

        return

    messenger.emitUiBrowseableMessage(response)
