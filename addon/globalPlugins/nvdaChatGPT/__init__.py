import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'site-packages'))
from .asker import askChatGPT, createAskMeaningPrompt
from . import languages as languages
from . import asker as asker
from .promptOption import EnumPromptOption
from . import configManager as configManager
from .myLog import mylog
from .promptOption import EnumPromptOption
from .dialogs import QuestionDialog
import gui
import wx
import config
from scriptHandler import script
import globalPluginHandler
from revChatGPT.V3 import Chatbot
import treeInterceptorHandler
import ui
import textInfos
import api
import threading
from openai.error import RateLimitError, AuthenticationError
from openai.error import ServiceUnavailableError
import queueHandler
from . import requestThreader as requestThreader
from . import instructions as instructions
from . import messenger as messenger
import addonHandler


configManager.initConfiguration()
addonHandler.initTranslation()


class OptionsPanel(gui.SettingsPanel):
    # Translators: Name  of category in setting panel.
    title = _("Ask chatGPT")

    def makeSettings(self, settingsSizer):
        sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

        # Translators: TextBox for open ai api key.
        label = _("chatGPT api key:")
        self.apiKey = sHelper.addLabeledControl(
            label, wx.TextCtrl)
        self.apiKey.Value = configManager.getConfig("apiKey")

        # Translators: SelectBox for output language when you ask meaning of a word.
        label = _("Output language of a meaning of words :")
        self.outputLanguage = sHelper.addLabeledControl(
            label, wx.Choice, choices=languages.LANGUAGE_OPTIONS)
        self.outputLanguage.Selection = configManager.getConfig(
            "outputLanguageIndex")

        # Translators: Checkbox for if you want a caution or not.
        label = _("Don't show a caution when a conversation is long")
        self.dontShowCaution = sHelper.addItem(
            wx.CheckBox(self, label=label))
        self.dontShowCaution.Value = configManager.getConfig("dontShowCaution")

    def onSave(self):
        configManager.setConfig("apiKey", self.apiKey.Value)
        configManager.setConfig("outputLanguageIndex",
                                self.outputLanguage.Selection)
        configManager.setConfig("dontShowCaution", self.dontShowCaution.Value)


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

    apiKey = configManager.getConfig("apiKey")
    if len(apiKey) == 0:
        messenger.emitUiBrowseableMessage(instructions.API_KEY_NOT_SET_ERROR)
        return True

    return False


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
        # Translators: Name of category in input gesture.
        category=_("Ask chatGPT"),
        # Translators: Description of gesture in input gesture.
        description=_("Ask the meaning of a word to chatGPT"),
        gestures=["kb:NVDA+shift+w"]
    )
    def script_askMeaningOfWord(self, gesture):
        if isApiKeyEmpty():
            return
        selectedText = get_selected_text()

        if isSelectedTextEmpty(selectedText):
            gui.mainFrame.prePopup()
            textBoxInstance = QuestionDialog(EnumPromptOption.ASKMEANINGOF)
            textBoxInstance.Show()
            # Raise put focus on the window, when it is already open, but lost focus.
            textBoxInstance.Raise()
            gui.mainFrame.postPopup()
            return

        requestThreader.start_thread(
            asker.askChatGPT, (asker.createAskMeaningPrompt(selectedText),),
            startMessage="asking the meaning to chatGPT")

    @script(
        # Translators: Name of category in input gesture.
        category=_("Ask chatGPT"),
        description=_("Ask the sentence to chatGPT"),
        gestures=["kb:NVDA+shift+l"]
    )
    def script_askSentence(self, gesture):
        if isApiKeyEmpty():
            return

        gui.mainFrame.prePopup()
        textBoxInstance = QuestionDialog(EnumPromptOption.ASKSENTENCE)
        textBoxInstance.Show()
        textBoxInstance.Raise()
        gui.mainFrame.postPopup()
