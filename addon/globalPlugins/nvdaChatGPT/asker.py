from typing import List, Optional, TypedDict
import addonHandler
from . import (
    languages as languages,
    messenger as messenger,
    configManager as configManager,
)

from . import utils as utils
import json
from . import instructions as instructions
from logHandler import log
from openai import OpenAI
from . import myLog as myLog


try:
    addonHandler.initTranslation()
except addonHandler.AddonError:
    log.warning(
        "Unable to initialise translations."
        "This may be because the addon is running from NVDA scratchpad."
    )


def createAskMeaningPrompt(word: str):
    outputLanguageIndex = configManager.getConfig("outputLanguageIndex")

    return languages.ASK_MEANING_PROMPT_MODELS[outputLanguageIndex].format(word)


class Message(TypedDict):
    role: str
    content: str


def createMessage(prompt: str, pastConvo: Optional[List[Message]] = None):
    messages = (
        [
            {
                "role": "system",
                "content": "You are a helpful assistant",
            },
        ]
        if pastConvo is None
        else pastConvo
    )

    messages.append(
        {
            "role": "user",
            "content": prompt,
        },
    )

    return messages


def askChatGPT(prompt: str, conversation=None):
    messages = createMessage(prompt, conversation)

    client = OpenAI(api_key=configManager.getConfig("apiKey"))

    try:
        completion = client.chat.completions.create(
            # TODO: use the model specified in config when asking a sentence.
            model="gpt-3.5-turbo",
            messages=messages,
        )

        response = completion.choices[0].message.content

    except Exception as e:
        myLog.mylog(e)
        if e.type == "invalid_request_error":
            messenger.emitUiBrowseableMessage(instructions.API_KEY_INCORRECT_ERROR)
        elif e.type == "insufficient_quota":
            messenger.emitUiBrowseableMessage(instructions.INSUFFICIENT_QUOTA_ERROR)
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

    messages.append({"role": "assistant", "content": response})

    myLog.mylog(json.dumps(messages))

    return messages
