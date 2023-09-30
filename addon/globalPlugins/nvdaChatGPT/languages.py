# -*- coding: UTF-8 -*-
from logHandler import log
import addonHandler

try:
    addonHandler.initTranslation()
except addonHandler.AddonError:
    log.warning(
        "Unable to initialise translations. This may be because the addon is running from NVDA scratchpad."
    )

# Hard-coded because I wanted the capability to set output language
# to the one different than the language of nvda
ASK_MEANING_PROMPT_MODELS = [
    "What is the meaning of {}? Respond in Arabic",
    "What is the meaning of {}? Respond in Chinese",
    "What is the meaning of {}? Respond in Danish",
    "What is the meaning of {}? Respond in English",
    "What is the meaning of {}? Respond in French",
    "What is the meaning of {}? Respond in German",
    "What is the meaning of {}? Respond in Italian",
    "{}とはどういう意味ですか、返答は日本語でお願いします",
    "What is the meaning of {}? Respond in Korean",
    "What is the meaning of {}? Respond in Portuguese",
    "What is the meaning of {}? Respond in Russian",
    "What is the meaning of {}? Respond in Slovak",
    "What is the meaning of {}? Respond in Spanish",
    "What is the meaning of {}? Respond in Turkish",
    "What is the meaning of {}? Respond in Ukrainian",
]


LANGUAGE_OPTIONS = [
    # Translators: Output language option.
    _("Arabic"),
    # Translators: Output language option.
    _("Chinese"),
    # Translators: Output language option.
    _("Danish"),
    # Translators: Output language option.
    _("English"),
    # Translators: Output language option.
    _("French"),
    # Translators: Output language option.
    _("German"),
    # Translators: Output language option.
    _("Italian"),
    # Translators: Output language option.
    _("Japanese"),
    # Translators: Output language option.
    _("Korean"),
    # Translators: Output language option.
    _("Portuguese"),
    # Translators: Output language option.
    _("Russian"),
    # Translators: Output language option.
    _("Slovak"),
    # Translators: Output language option.
    _("Spanish"),
    # Translators: Output language option.
    _("Turkish"),
    # Translators: Output language option.
    _("Ukrainian"),
]

ENGINE_OPTIONS = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-0613",
]
