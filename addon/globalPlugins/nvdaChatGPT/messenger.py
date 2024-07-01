import queueHandler
import ui
from .temporary_path import temporary_sys_path


with temporary_sys_path():
    import markdown2


def emitUiBrowseableMessage(message):
    html_String = markdown2.markdown(
        message, extras=["fenced-code-blocks", "code-friendly"]
    )

    html_String = html_String.rstrip("\n")
    queueHandler.queueFunction(
        queueHandler.eventQueue, ui.browseableMessage, html_String, isHtml=True
    )


def emitUiMessage(message):
    queueHandler.queueFunction(queueHandler.eventQueue, ui.message, message)
