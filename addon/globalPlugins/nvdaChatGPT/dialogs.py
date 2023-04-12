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


class TextBox(wx.Dialog):
    # Assigning a function becaues we need to call to get content of weak ref.
    instances = {EnumPromptOption.ASKMEANINGOF: lambda: None,
                 EnumPromptOption.ASKSENTENCE: lambda: None}

    controlPressed = False

    def __new__(cls, *args, **kwargs):
        instance = TextBox.instances[args[0]]()
        if instance is None:
            return super(TextBox, cls).__new__(cls, *args, **kwargs)
        return instance

    def initChatLogList(self):
        self.panel = wx.Panel(self)
        self.list_box = wx.ListBox(self.panel, style=wx.LB_SINGLE)
        self.list_box.Bind(wx.EVT_CHAR_HOOK, self.onListKeyDown)
        self.list_box.Bind(wx.EVT_SET_FOCUS, self.on_list_box_focus)

        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_sizer.Add(self.list_box, 1, wx.EXPAND)

        self.panel.SetSizer(panel_sizer)
        self.new_sizer.Add(self.panel, 1, wx.EXPAND | wx.ALL, 5)

    def __init__(self, promptOption: EnumPromptOption):
        self.promptOption = promptOption
        if promptOption == EnumPromptOption.ASKMEANINGOF:
            # kill other instances.
            otherInstance = TextBox.instances[EnumPromptOption.ASKSENTENCE]()
            if otherInstance is not None:
                TextBox.instances[EnumPromptOption.ASKSENTENCE]()._clean()
                TextBox.instances[EnumPromptOption.ASKSENTENCE] = lambda: None

            title = _("What word do you want to know?")
        elif promptOption == EnumPromptOption.ASKSENTENCE:
            # kill other instances.
            otherInstance = TextBox.instances[EnumPromptOption.ASKMEANINGOF]()
            if otherInstance is not None:
                otherInstance ._clean()
                TextBox.instances[EnumPromptOption.ASKMEANINGOF] = lambda: None

            title = _("What do you want to ask?")

        if TextBox.instances[promptOption]() is not None:
            return
        TextBox.instances[promptOption] = weakref.ref(self)

        super().__init__(
            gui.mainFrame,
            title=title,
            size=wx.Size(500, 500),
            pos=wx.DefaultPosition,
            style=wx.CAPTION | wx.CLOSE_BOX | wx.RESIZE_BORDER | wx.STAY_ON_TOP
        )

        self.chatbot = Chatbot(
            api_key=configManager.getConfig("apiKey"))

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sHelper = guiHelper.BoxSizerHelper(self, wx.VERTICAL)

        self.new_sizer = wx.BoxSizer(wx.VERTICAL)

        if promptOption == EnumPromptOption.ASKSENTENCE:
            self.initChatLogList()
            # self.add_items_to_list()

        self.new_sizer.AddSpacer(
            guiHelper.SPACE_BETWEEN_ASSOCIATED_CONTROL_VERTICAL)
        self.noteEditArea = wx.TextCtrl(
            self, style=wx.TE_RICH2 | wx.TE_MULTILINE)
        self.new_sizer.Add(self.noteEditArea, proportion=1, flag=wx.EXPAND)
        sHelper.addItem(self.new_sizer, proportion=1, flag=wx.EXPAND)

        self.noteEditArea.SetFocus()

        buttons = guiHelper.ButtonHelper(wx.HORIZONTAL)

        discardButton = buttons.addButton(
            self,
            id=wx.ID_CLOSE,
            label=_("&Cancel"))
        discardButton.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
        sHelper.addDialogDismissButtons(buttons, True)
        mainSizer.Add(sHelper.sizer, proportion=1, flag=wx.EXPAND)
        self.SetSizer(mainSizer)
        self.noteEditArea.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.noteEditArea.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.Bind(wx.EVT_CLOSE, self.onDiscard)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)
        self.EscapeId = wx.ID_CLOSE

    def getChatLog(self):
        data = convoManager.readConversation()
        chat_log_array = []
        for item in data["default"]:
            if item["role"] == "user":
                chat_log_array.append("You : " + item["content"])
            elif item["role"] == "assistant":
                chat_log_array.append("ChatGPT : " + item["content"])

        return chat_log_array

    def refreshChatLog(self):
        items = self.getChatLog()

        self.list_box.SetItems(items)

    def conversation_flow(self, prompt: str):

        conversation = convoManager.readConversation()

        if "default" in conversation and len(conversation["default"]) != 0:
            self.chatbot.conversation = conversation["default"]

        asker.askChatGPT(prompt, chatbot=self.chatbot)

        convoManager.saveConversation(
            {"default": self.chatbot.conversation})
        self.refreshChatLog()

    def request_chatGPT(self, input: str):

        if self.promptOption == EnumPromptOption.ASKMEANINGOF:
            requestThreader.start_thread(
                target=asker.askChatGPT, args=(asker.createAskMeaningPrompt(
                    input),), startMessage="asking the meaning to chatGPT")
        elif self.promptOption == EnumPromptOption.ASKSENTENCE:
            requestThreader.start_thread(
                target=self.conversation_flow, args=(input, ), startMessage="sending the sentence to chatGPT")

    # Always set focus to the last element, when list_box gets focus
    def on_list_box_focus(self, event):
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

    def onKeyDown(self, event):

        keycode = event.GetKeyCode()

        if keycode == wx.WXK_CONTROL:
            self.controlPressed = True

        elif keycode == wx.WXK_RETURN and self.controlPressed:

            userInput = self.noteEditArea.GetValue()

            self.noteEditArea.Clear()

            self.request_chatGPT(userInput)

            if self.promptOption == EnumPromptOption.ASKMEANINGOF:
                self._clean()

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
