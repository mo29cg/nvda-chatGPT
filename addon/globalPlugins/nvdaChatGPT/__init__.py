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
from logHandler import log

configManager.initConfiguration()
try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.warning(
		"Unable to initialise translations. This may be because the addon is running from NVDA scratchpad."
	)

# Translators: Name  of category in setting panel and input gestures.
category_name = _("Ask chatGPT")


class OptionsPanel(gui.SettingsPanel):
	title = category_name

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		# Translators: TextBox for open ai api key.
		label = _("chatGPT api key:")
		self.apiKey = sHelper.addLabeledControl(label, wx.TextCtrl)
		self.apiKey.Value = configManager.getConfig("apiKey")

		# Translators: SelectBox for output language when you ask meaning of a word.
		label = _("Output language of a meaning of words :")
		self.outputLanguage = sHelper.addLabeledControl(label, wx.Choice, choices=languages.LANGUAGE_OPTIONS)
		self.outputLanguage.Selection = configManager.getConfig("outputLanguageIndex")

		# making it configurable only when asking a sentence, because when asking a meaning of words,
		# the quality doesn't really change
		# Translators: SelectBox of chat GPT version when user ask a sentence
		label = _("Chat gpt version that respond to a conversation :")
		self.gptVersionSentence = sHelper.addLabeledControl(
			label, wx.Choice, choices=languages.ENGINE_OPTIONS
		)
		self.gptVersionSentence.Selection = configManager.getConfig("gptVersionSentenceIndex")

		# Translators: Checkbox for if you want a caution or not.
		label = _("Don't show a caution when a conversation is long")
		self.dontShowCaution = sHelper.addItem(wx.CheckBox(self, label=label))
		self.dontShowCaution.Value = configManager.getConfig("dontShowCaution")

	def onSave(self):
		configManager.setConfig("apiKey", self.apiKey.Value)
		configManager.setConfig("outputLanguageIndex", self.outputLanguage.Selection)
		configManager.setConfig("gptVersionSentenceIndex", self.gptVersionSentence.Selection)
		configManager.setConfig("dontShowCaution", self.dontShowCaution.Value)


def get_selected_text():
	# this way, it can get selected text from anywhere
	focusObj = api.getFocusObject()
	treeInterceptor = focusObj.treeInterceptor
	if isinstance(treeInterceptor, treeInterceptorHandler.DocumentTreeInterceptor):
		# try:
		info = treeInterceptor.makeTextInfo(textInfos.POSITION_SELECTION)
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
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(OptionsPanel)

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(OptionsPanel)

	@script(
		category=category_name,
		# Translators: Description of gesture in input gesture.
		description=_("Ask the meaning of a word to chatGPT"),
		gestures=["kb:NVDA+shift+w"],
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
			target=asker.askChatGPT,
			kwargs={"prompt": asker.createAskMeaningPrompt(selectedText), "model": "gpt-3.5-turbo"},
			# Translators: Message when a word is sent to chatGPT
			startMessage=_("asking the meaning to chatGPT"),
		)

	@script(
		category=category_name,
		# Translators: Description of ask sentence gesture in input gesture.
		description=_("Ask the sentence to chatGPT"),
		gestures=["kb:NVDA+shift+l"],
	)
	def script_askSentence(self, gesture):
		if isApiKeyEmpty():
			return

		gui.mainFrame.prePopup()
		textBoxInstance = QuestionDialog(EnumPromptOption.ASKSENTENCE)
		textBoxInstance.Show()
		textBoxInstance.Raise()
		gui.mainFrame.postPopup()
