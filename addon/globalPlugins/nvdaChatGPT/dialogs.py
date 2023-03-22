from .asker import askChatGPT, createAskMeaning
import threading
from .promptOption import EnumPromptOption
import queueHandler
import ui
import wx
import gui
from gui import guiHelper
import weakref
from .myLog import mylog


threadObj = None


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

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sHelper = guiHelper.BoxSizerHelper(self, wx.VERTICAL)

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.AddSpacer(guiHelper.SPACE_BETWEEN_ASSOCIATED_CONTROL_VERTICAL)
        self.noteEditArea = wx.TextCtrl(
            self, style=wx.TE_RICH2 | wx.TE_MULTILINE)
        sizer.Add(self.noteEditArea, proportion=1, flag=wx.EXPAND)
        sHelper.addItem(sizer, proportion=1, flag=wx.EXPAND)

        self.noteEditArea.SetFocus()

        buttons = guiHelper.ButtonHelper(wx.HORIZONTAL)

        discardButton = buttons.addButton(
            self,
            id=wx.ID_CLOSE,
            label=_("&Close"))
        discardButton.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
        sHelper.addDialogDismissButtons(buttons, True)
        mainSizer.Add(sHelper.sizer, proportion=1, flag=wx.EXPAND)
        self.SetSizer(mainSizer)
        self.noteEditArea.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.noteEditArea.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.Bind(wx.EVT_CLOSE, self.onDiscard)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)
        self.EscapeId = wx.ID_CLOSE

    def onKeyDown(self, event):

        keycode = event.GetKeyCode()

        if keycode == wx.WXK_CONTROL:
            self.controlPressed = True

        elif keycode == wx.WXK_RETURN and self.controlPressed:
            # Don't allow asking two questions at the same time.
            runnings = threading.enumerate()
            for th in runnings:
                if th.name == "askChatGPT":
                    queueHandler.queueFunction(
                        queueHandler.eventQueue, ui.message, "You are already asking something, wait for the response first")
                    break
            else:
                userInput = self.noteEditArea.GetValue()
                self.startThreadOfRequesting(userInput)

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
        evt.Skip()

    def onDiscard(self, evt):
        self._clean()

    def _clean(self):

        self.DestroyChildren()
        self.Destroy()

    def startThreadOfRequesting(self, input: str):
        global threadObj
        if self.promptOption == EnumPromptOption.ASKMEANINGOF:
            threadObj = threading.Thread(
                target=askChatGPT, args=(createAskMeaning(input), "asking the Weaning to chatGPT"), name="askChatGPT")
        elif self.promptOption == EnumPromptOption.ASKSENTENCE:
            threadObj = threading.Thread(
                target=askChatGPT, args=(input, "asking the sentence to chatGPT"), name="askChatGPT")
        threadObj.start()
