import addonHandler
from . import (
    languages as languages,
    messenger as messenger,
    configManager as configManager,
)
from revChatGPT.V3 import Chatbot
from . import utils as utils
import json
from . import instructions as instructions
from logHandler import log

try:
    addonHandler.initTranslation()
except addonHandler.AddonError:
    log.warning(
        "Unable to initialise translations. This may be because the addon is running from NVDA scratchpad."
    )


def createAskMeaningPrompt(word):
    outputLanguageIndex = configManager.getConfig("outputLanguageIndex")

    return languages.ASK_MEANING_PROMPT_MODELS[outputLanguageIndex].format(word)


def askChatGPT(prompt: str, chatbot: Chatbot = None):
    if chatbot is None:
        chatbot = Chatbot(api_key=configManager.getConfig("apiKey"))
    try:
        response = chatbot.ask(prompt)

    # revChatGPT is not setting type for Exceptions currently, we need more efforts to handle errors well.
    except Exception as e:
        errorText = utils.extract_json_from_exception(str(e))
        errorJson = json.loads(errorText)
        errorType = errorJson["error"]["type"]
        if errorType == "invalid_request_error":
            messenger.emitUiBrowseableMessage(
                instructions.API_KEY_INCORRECT_ERROR)
        elif errorType == "insufficient_quota":
            messenger.emitUiBrowseableMessage(
                instructions.INSUFFICIENT_QUOTA_ERROR)
        else:
            unexpectedErrorMessage = _(
                # Translators: Message when it encounter an unexpected error, the error itself will be shown
                #  below this.
                "Unexpected error occured. Please send the error message below to the add-on "
                "author's email address, lcong5946@gmail.com \n\n "
            )
            messenger.emitUiBrowseableMessage(unexpectedErrorMessage + str(e))

        return

    messenger.emitUiBrowseableMessage(response)
