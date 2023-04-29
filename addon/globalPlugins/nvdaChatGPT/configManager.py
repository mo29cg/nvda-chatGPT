import config

module = "askChatGPT"


def initConfiguration():
    confspec = {
        "apiKey": "string( default='')",
        "outputLanguageIndex": "integer( default=3, min=0, max=15)",
        "dontShowCaution": "boolean( default=False)",
    }
    config.conf.spec[module] = confspec


def getConfig(key):
    value = config.conf[module][key]
    return value


def setConfig(key, value):
    config.conf[module][key] = value
