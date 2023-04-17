import queueHandler
import ui
import markdown2


def emitUiBrowseableMessage(message):
    html_String = markdown2.markdown(
        message, extras=["fenced-code-blocks", "code-friendly"])
    queueHandler.queueFunction(
        queueHandler.eventQueue, ui.browseableMessage, html_String, isHtml=True)


def emitUiMessage(message):
    queueHandler.queueFunction(
        queueHandler.eventQueue, ui.message, message)
