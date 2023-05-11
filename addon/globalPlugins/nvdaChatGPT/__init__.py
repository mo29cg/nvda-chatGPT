import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'site-packages'))
from . import languages as languages
from . import asker as asker
from .promptOption import EnumPromptOption
from . import configManager as configManager
from .dialogs import QuestionDialog
import gui
import wx
from scriptHandler import script
import globalPluginHandler
import treeInterceptorHandler
import textInfos
import api
from . import requestThreader as requestThreader
from . import instructions as instructions
from . import messenger as messenger
import addonHandler


configManager.initConfiguration()
addonHandler.initTranslation()
# Translators: Name  of category in setting panel and input gestures.
category_name = _("Ask chatGPT")


class OptionsPanel(gui.SettingsPanel):
    title = category_name

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


def get_selected_text():
    # this way, it can get selected text from anywhere
    focusObj = api.getFocusObject()
    treeInterceptor = focusObj.treeInterceptor
    if isinstance(treeInterceptor, treeInterceptorHandler.DocumentTreeInterceptor):

        # try:
        info = treeInterceptor.makeTextInfo(
            textInfos.POSITION_SELECTION)
        # selected text in html text box of firefox is not in treeInterceptor
        if info.text != "":
            return info.text.strip()
        # except:
        # pass

    try:
        info = focusObj.makeTextInfo(textInfos.POSITION_SELECTION)
        return info.text.strip()

    except (RuntimeError, NotImplementedError):
        return ""


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
        category=category_name,
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
            # Translators: Message when a word is sent to chatGPT
            startMessage=_("asking the meaning to chatGPT"))

    @script(
        category=category_name,
        # Translators: Description of ask sentence gesture in input gesture.
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
