import queueHandler
import ui
import markdown2


def emitUiBrowseableMessage(message):

    queueHandler.queueFunction(
        queueHandler.eventQueue, ui.browseableMessage, markdown2.markdown(message, extras=["fenced-code-blocks"]), isHtml=True)


def emitUiMessage(message):
    queueHandler.queueFunction(
        queueHandler.eventQueue, ui.message, message)
