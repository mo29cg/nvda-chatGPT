from .myLog import mylog
from . import requestThreader as requestThreader
from . import messenger as messenger
from . import asker as asker
from . import configManager as configManager
from . import convoManager as convoManager
from revChatGPT.V3 import Chatbot
from .promptOption import EnumPromptOption
import wx
import gui
from gui import guiHelper
import weakref


class CautionDialog(wx.Dialog):
    def __init__(self, parent, title, message):
        super(CautionDialog, self).__init__(parent, -1, title)

        # Translators: CheckBox for a caution dialog that asks users to continue
        label = _("Don't show again")
        self.dont_ask_again = wx.CheckBox(
            self, label=label)
        self.message = wx.StaticText(self, label=message)
        yesButton = wx.Button(self, wx.ID_YES, label='Yes')
        noButton = wx.Button(self, wx.ID_NO, label='No')

        yesButton.Bind(wx.EVT_BUTTON, self.onYes)
        noButton.Bind(wx.EVT_BUTTON, self.onNo)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.message, 8, wx.ALL, 5)
        sizer.Add(self.dont_ask_again, 3, wx.ALL, 0)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(yesButton, 0, wx.ALL, 5)
        btn_sizer.Add(noButton, 0, wx.ALL, 5)
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER)
        self.SetSizer(sizer)

    def onYes(self, event):
        self.EndModal(wx.ID_YES)

    def onNo(self, event):
        self.EndModal(wx.ID_NO)


class QuestionDialog(wx.Dialog):
    controlPressed = False

    # Assigning a function becaues we need to call to get content of weak ref.
    def instance(): return None

    def __new__(cls, *args, **kwargs):
        instance = QuestionDialog.instance()
        if instance is None or instance.promptOption != args[0]:
            return super(QuestionDialog, cls).__new__(cls, *args, **kwargs)
        return instance

    def __init__(self, promptOption: EnumPromptOption):
        self.promptOption = promptOption
        if QuestionDialog.instance() is not None:
            if QuestionDialog.instance().promptOption == promptOption:
                return
            else:
                QuestionDialog.instance()._clean()

        if promptOption == EnumPromptOption.ASKMEANINGOF:
            # Translators:Title for a dialog when a user want to ask meaning of a word
            title = _("What word do you want to know?")
        elif promptOption == EnumPromptOption.ASKSENTENCE:
            # Translators: Title for a dialog when a user want to ask a sentence
            title = _("What do you want to ask?")

        QuestionDialog.instance = weakref.ref(self)

        super().__init__(
            gui.mainFrame,
            title=title,
            size=wx.Size(500, 500),
            pos=wx.DefaultPosition,
            style=wx.CAPTION | wx.CLOSE_BOX | wx.RESIZE_BORDER | wx.STAY_ON_TOP
        )

        self.chatbot = Chatbot(
            api_key=configManager.getConfig("apiKey"),)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sHelper = guiHelper.BoxSizerHelper(self, wx.VERTICAL)

        self.new_sizer = wx.BoxSizer(wx.VERTICAL)

        if promptOption == EnumPromptOption.ASKSENTENCE:
            self.initChatLogList()

        self.new_sizer.AddSpacer(
            guiHelper.SPACE_BETWEEN_ASSOCIATED_CONTROL_VERTICAL)
        self.noteEditArea = wx.TextCtrl(
            self, style=wx.TE_RICH2 | wx.TE_MULTILINE)
        self.new_sizer.Add(self.noteEditArea, proportion=1, flag=wx.EXPAND)
        sHelper.addItem(self.new_sizer, proportion=1, flag=wx.EXPAND)

        self.noteEditArea.SetFocus()

        buttons = guiHelper.ButtonHelper(wx.HORIZONTAL)

        # Translators: Button of a question dialog.
        label = _("&Submit")
        submitButton = buttons.addButton(
            self,
            label=label)
        submitButton.Bind(wx.EVT_BUTTON, lambda evt: self.onSubmit())

        # Translators: Button for a question dialog.
        label = _("&Cancel")
        discardButton = buttons.addButton(
            self,
            id=wx.ID_CLOSE,
            label=label)
        discardButton.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
        sHelper.addDialogDismissButtons(buttons, True)
        mainSizer.Add(sHelper.sizer, proportion=1, flag=wx.EXPAND)
        self.SetSizer(mainSizer)
        self.noteEditArea.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.noteEditArea.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.Bind(wx.EVT_CLOSE, self.onDiscard)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)
        self.EscapeId = wx.ID_CLOSE

    def initChatLogList(self):
        self.panel = wx.Panel(self)
        self.list_box = wx.ListBox(self.panel, style=wx.LB_SINGLE)
        self.list_box.Bind(wx.EVT_CHAR_HOOK, self.onListKeyDown)
        self.list_box.Bind(wx.EVT_SET_FOCUS, self.on_list_box_focus)

        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_sizer.Add(self.list_box, 1, wx.EXPAND)

        self.panel.SetSizer(panel_sizer)
        self.new_sizer.Add(self.panel, 1, wx.EXPAND | wx.ALL, 5)

    def getChatLog(self):
        data = convoManager.readConversation()
        chat_log_array = []
        for item in data:
            if item["role"] == "user":
                # Translators: Prefix of user's message in the chat log
                youPrefix = _("You : ")
                chat_log_array.append(youPrefix + item["content"])
            elif item["role"] == "assistant":
                chat_log_array.append("ChatGPT : " + item["content"])

        return chat_log_array

    def refreshChatLog(self):
        items = self.getChatLog()

        self.list_box.SetItems(items)

    def conversation_flow(self, prompt: str):

        conversation = convoManager.readConversation()

        if len(conversation) != 0:
            self.chatbot.conversation = conversation

        asker.askChatGPT(prompt, chatbot=self.chatbot)

        convoManager.saveConversation(
            {"default": self.chatbot.conversation})
        self.refreshChatLog()

    def confirm_continue_if_conversation_is_long(self) -> bool:
        conversation = convoManager.readConversation()

        # 11 because it has one default message
        if len(conversation) == 11 and configManager.getConfig("dontShowCaution") == False:
            # Translators:  Title of a caution dialog when a conversation is long
            cautionTitle = _("Do you want to continue?")
            cautionMessage = _(
                # Translators: Message of a caution dialog when a conversation is long
                "You've already asked 5 questions in a conversation,\nnote that the longer conversation the more your credit (or your real money) consume.\nDo you want to continue?")
            dlg = CautionDialog(self, cautionTitle, cautionMessage)
            result = dlg.ShowModal()
            dontShowAgainValue = dlg.dont_ask_again.Value
            dlg.Destroy()

            if result == wx.ID_YES:
                if dontShowAgainValue == True:
                    configManager.setConfig("dontShowCaution", True)
            else:
                return False
        return True

    def request_chatGPT(self, input: str):

        if self.promptOption == EnumPromptOption.ASKMEANINGOF:
            # Translators: Message when a word is sent to chatGPT
            startMessage = _("asking the meaning to chatGPT")
            requestThreader.start_thread(
                target=asker.askChatGPT, args=(asker.createAskMeaningPrompt(
                    input),), startMessage=startMessage)
        elif self.promptOption == EnumPromptOption.ASKSENTENCE:
            # Translators: Message when a word is sent to chatGPT
            startMessage = _("asking that to chatGPT")
            requestThreader.start_thread(
                target=self.conversation_flow, args=(input, ), startMessage=startMessage)

    def on_list_box_focus(self, event):
        # Always set focus to the last element, when list_box gets focus
        last_item_index = self.list_box.GetCount() - 1
        self.list_box.SetSelection(last_item_index)

    def onListKeyDown(self, event):
        keycode = event.GetKeyCode()

        if keycode == wx.WXK_RETURN:
            if self.list_box.GetCount() == 0:
                return

            selected_item = self.list_box.GetString(
                self.list_box.GetSelection())

            parts = selected_item.split(":", 1)

            if len(parts) > 1:
                result = parts[1]
            else:
                result = ""
            messenger.emitUiBrowseableMessage(result)
        else:
            event.Skip()

    def onSubmit(self):
        userInput = self.noteEditArea.GetValue()
        if userInput .strip() == "":
            # Translators: Error message when trying to submit without entering anything.
            errorMessage = _("The text box is empty, type something!")
            messenger.emitUiMessage(errorMessage)
            return

        # Doing both self.noteEditArea.Clear() and self._clean() at the same time causes an error which I don't understand
        if self.promptOption == EnumPromptOption.ASKSENTENCE:
            if self.confirm_continue_if_conversation_is_long() != True:
                return
            self.noteEditArea.Clear()

        self.request_chatGPT(userInput)

        if self.promptOption == EnumPromptOption.ASKMEANINGOF:
            self._clean()

    def onKeyDown(self, event):

        keycode = event.GetKeyCode()

        if keycode == wx.WXK_CONTROL:
            self.controlPressed = True

        elif keycode == wx.WXK_RETURN and self.controlPressed:
            self.onSubmit()

            return
        event.Skip()

    def onKeyUp(self, event):

        keycode = event.GetKeyCode()

        if keycode == wx.WXK_CONTROL:
            self.controlPressed = False

        else:
            event.Skip()

    def onDestroy(self, evt):
        convoManager.saveConversation({"default": []})
        evt.Skip()

    def onDiscard(self, evt):
        self._clean()

    def _clean(self):
        self.DestroyChildren()
        self.Destroy()
