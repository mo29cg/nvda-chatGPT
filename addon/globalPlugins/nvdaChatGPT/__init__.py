import pprint
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'site-packages'))

# f = open("C:\\Users\\suzuki\\1.json", "w")
# print(pprint.pformat(sys.path), file=f)
# f.close()
import gui
import wx
import config
from scriptHandler import script
import inputCore
import globalPluginHandler
from revChatGPT.Official import Chatbot
import treeInterceptorHandler
import ui
import textInfos
import api
import threading
from openai.error import RateLimitError
from openai.error import ServiceUnavailableError

module = "askChatGPT"


def initConfiguration():
    confspec = {
        "apiKey": "string( default='')",
        "outputLanguageIndex": "integer( default=0, min=0, max=2)",
        "askWordBinding": "string( default='NVDA+shift+a')",
        "askSentence": "string( default='NVDA+shift+l')",
    }
    config.conf.spec[module] = confspec


def getConfig(key):
    value = config.conf[module][key]
    return value


def setConfig(key, value):
    config.conf[module][key] = value


initConfiguration()


class OptionsPanel(gui.SettingsPanel):
    title = _("askChatGPT")
    languages = [
        _("English"),
        _("Japanese"),
    ]

    def makeSettings(self, settingsSizer):
        sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

        self.apiKey = sHelper.addLabeledControl(
            _("chatGPT api key:"), wx.TextCtrl)
        self.apiKey.Value = getConfig("apiKey")

        label = _("Output language :")
        self.outputLanguage = sHelper.addLabeledControl(
            label, wx.Choice, choices=self.languages)
        self.outputLanguage.Selection = getConfig(
            "outputLanguageIndex")

        self.askWordBinding = sHelper.addLabeledControl(
            _("key binding for ask wword: "), wx.TextCtrl)

        self.askWordBinding.Value = getConfig("askWordBinding")

        self.askSentence = sHelper.addLabeledControl(
            _("key binding for ask sentence:"), wx.TextCtrl)
        self.askSentence.Value = getConfig("askSentence")

    def onSave(self):
        setConfig("apiKey", self.apiKey.Value)
        setConfig("outputLanguageIndex", self.outputLanguage.Selection)
        setConfig("askSentence", self.askSentence.Value)
        ui.message("You need to restart nvda to take effect")

# this way, it can get selected text from anywhere


def get_selected_text():
    obj = api.getFocusObject()
    treeInterceptor = obj.treeInterceptor
    if isinstance(treeInterceptor, treeInterceptorHandler.DocumentTreeInterceptor):
        obj = treeInterceptor

    try:
        info = obj.makeTextInfo(textInfos.POSITION_SELECTION)
    except (RuntimeError, NotImplementedError):
        return ""
    return info.text.strip()


def createAskMeaning(word):
    outputLanguageIndex = getConfig("outputLanguageIndex")

    if (outputLanguageIndex == 0):
        return "What is the meaning of " + word + "? Respond in english"
    elif (outputLanguageIndex == 1):
        return word + "とはどういう意味ですか、返答は日本語でお願いします"


def askChatGPT(text, functionStartMessage):
    ui.message(functionStartMessage)

    chatbot = Chatbot(
        api_key=getConfig("apiKey"))
    try:
        response = chatbot.ask(text)
        ui.browseableMessage(response["choices"][0]["text"])
    except (RateLimitError, ServiceUnavailableError):
        ui.message("the server is busy, try again later")


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    def __init__(self):
        super(GlobalPlugin, self).__init__()
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(
            OptionsPanel)

    def terminate(self):
        super(GlobalPlugin, self).terminate()
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(
            OptionsPanel)

    @ script(
        description=_("ask the meaning of a word to chatGPT"),
        gestures=["kb:" + getConfig("askWordBinding")]
    )
    def script_askMeaningOfWord(self, gesture):
        selectedText = get_selected_text()
        if len(selectedText) == 0:
            ui.message("no selection")
            return

        threading1 = threading.Thread(
            target=askChatGPT, args=(createAskMeaning(selectedText), "asking the meaning to chatGPT"))
        threading1.start()

    @ script(
        description=_("ask the meaning of a word to chatGPT"),
        gestures=["kb:" + getConfig("askSentence")]
        # gestures=["kb:NVDA+l"]
    )
    def script_askSentence(self, gesture):
        selectedText = get_selected_text()
        if len(selectedText) == 0:
            ui.message("no selection")
            return

        threading1 = threading.Thread(
            target=askChatGPT, args=(selectedText, "sending the sentence to chatGPT"))
        threading1.start()
