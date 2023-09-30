import addonHandler
from logHandler import log


def extract_json_from_exception(text):
    start_index = text.find("{")

    if start_index != -1:
        return text[start_index:]
    else:
        return None


def initTranslationWithErrorHandling():
    try:
        addonHandler.initTranslation()
    except addonHandler.AddonError:
        log.warning(
            "Unable to initialise translations. This may be because"
            " the addon is running from NVDA scratchpad."
        )
