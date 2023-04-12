import config

module = "askChatGPT"


def initConfiguration():
    confspec = {
        "apiKey": "string( default='')",
        "outputLanguageIndex": "integer( default=2, min=0, max=11)",
    }
    config.conf.spec[module] = confspec


def getConfig(key):
    value = config.conf[module][key]
    return value


def setConfig(key, value):
    config.conf[module][key] = value
