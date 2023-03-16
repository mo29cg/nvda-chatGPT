import ui
import wx
import gui
from gui import guiHelper
import weakref
from .myLog import mylog

textBoxInstance = None


class TextBox(wx.Dialog):

    @classmethod
    def _instance(cls):
        """ type: () -> NoteTakerDialog
        return None until this is replaced with a weakref.ref object. Then the instance is retrieved
        with by treating that object as a callable.
        """
        return None

    def __new__(cls, *args, **kwargs):
        instance = TextBox._instance()
        if instance is None:
            return super(TextBox, cls).__new__(cls, *args, **kwargs)
        return instance

    def __init__(self):
        if TextBox._instance() is not None:
            return
        TextBox._instance = weakref.ref(self)

        title = _("Text box")

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
        self.Bind(wx.EVT_CLOSE, self.onDiscard)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)
        self.EscapeId = wx.ID_CLOSE

    def onKeyDown(self, event):

        keycode = event.GetKeyCode()

        # windows key, it might be better if text box closes, when focus is moved by windows + number
        if keycode == 393:
            self._clean()
        else:
            event.Skip()

    def onDestroy(self, evt):
        global textBoxInstance
        textBoxInstance = None
        evt.Skip()

    def onDiscard(self, evt):
        self._clean()

    def _clean(self):

        self.DestroyChildren()
        self.Destroy()
