import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'site-packages'))
from .myLog import mylog
from .promptOption import EnumPromptOption
from .dialogs import TextBox
# f = open("C:\\Users\\suzuki\\1.json", "w")
# print(pprint.pformat(sys.path), file=f)
# f.close()
import gui
import wx
import config
from scriptHandler import script
import globalPluginHandler
from revChatGPT.Official import Chatbot
import treeInterceptorHandler
import ui
import textInfos
import api
import threading
from openai.error import RateLimitError, AuthenticationError
from openai.error import ServiceUnavailableError
import queueHandler

module = "askChatGPT"


def initConfiguration():
    confspec = {
        "apiKey": "string( default='')",
        "outputLanguageIndex": "integer( default=0, min=0, max=2)",
        "openTextBox": "boolean( default=False)",
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

        label = _("Output language of a meaning of wordsf :")
        self.outputLanguage = sHelper.addLabeledControl(
            label, wx.Choice, choices=self.languages)
        self.outputLanguage.Selection = getConfig(
            "outputLanguageIndex")

        label = _("Open text box, when nothing is selected.")
        self.openTextBoxCheckbox = sHelper.addItem(
            wx.CheckBox(self, label=label))
        self.openTextBoxCheckbox .Value = getConfig("openTextBox")

    def onSave(self):
        setConfig("apiKey", self.apiKey.Value)
        setConfig("outputLanguageIndex", self.outputLanguage.Selection)
        setConfig("openTextBox", self.openTextBoxCheckbox .Value)


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


def isSelectedTextEmpty(selectedText):
    if len(selectedText) == 0:

        return True
    else:
        return False


def isApiKeyEmpty():

    apiKey = getConfig("apiKey")
    if len(apiKey) == 0:
        ui.message("Set an api key first.")
        return True

    return False


def createAskMeaning(word):
    outputLanguageIndex = getConfig("outputLanguageIndex")

    if (outputLanguageIndex == 0):
        return "What is the meaning of " + word + "? Respond in english"
    elif (outputLanguageIndex == 1):
        return word + "とはどういう意味ですか、返答は日本語でお願いします"


def askChatGPT(text, functionStartMessage):
    # Apparently ui.message doesn'T work in threads with a braille display, and this is how to make it work.
    queueHandler.queueFunction(
        queueHandler.eventQueue, ui.message, functionStartMessage)

    chatbot = Chatbot(
        api_key=getConfig("apiKey"))
    try:
        response = chatbot.ask(text)
        queueHandler.queueFunction(
            queueHandler.eventQueue, ui.browseableMessage, response["choices"][0]["text"])
    except (RateLimitError, ServiceUnavailableError):
        queueHandler.queueFunction(
            queueHandler.eventQueue, ui.message, "the server is busy, try again later")
    except (AuthenticationError):
        queueHandler.queueFunction(
            queueHandler.eventQueue, ui.message, "The api key is incorrect, set a correct one..")


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    def __init__(self):
        super(GlobalPlugin, self).__init__()
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(
            OptionsPanel)

    def terminate(self):
        super(GlobalPlugin, self).terminate()
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(
            OptionsPanel)

    @script(
        category=_("Ask chatGPT"),
        description=_("Ask the meaning of a word to chatGPT"),
        gestures=["kb:NVDA+shift+w"]
    )
    def script_askMeaningOfWord(self, gesture):
        if isApiKeyEmpty():
            return
        selectedText = get_selected_text()

        if isSelectedTextEmpty(selectedText):
            gui.mainFrame.prePopup()
            textBoxInstance = TextBox(EnumPromptOption.ASKMEANINGOF)
            textBoxInstance.Show()
            # Raise put focus on the window, when it is already open, but lost focus.
            textBoxInstance.Raise()
            gui.mainFrame.postPopup()
            return

        threading1 = threading.Thread(
            target=askChatGPT, args=(createAskMeaning(selectedText), "asking the meaning to chatGPT"))
        threading1.start()

    @script(
        category=_("Ask chatGPT"),
        description=_("Ask the sentence to chatGPT"),
        gestures=["kb:NVDA+shift+l"]
    )
    def script_askSentence(self, gesture):
        if isApiKeyEmpty():
            return

        gui.mainFrame.prePopup()
        textBoxInstance = TextBox(EnumPromptOption.ASKSENTENCE)
        textBoxInstance.Show()
        textBoxInstance.Raise()
        gui.mainFrame.postPopup()
