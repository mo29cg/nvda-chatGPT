from json.decoder import JSONDecodeError
import json
import os

convo_file_name = "chatGPT_conversations.json"
source_dir = os.path.dirname(os.path.abspath(__file__))
convo_file_path = os.path.join(source_dir, convo_file_name)


with open(convo_file_path, 'w'):
    pass


def saveConversation(conversation):

    f = open(convo_file_path, "w", encoding='utf-8')
    json_string = json.dumps(conversation, ensure_ascii=False, indent=2)
    print(json_string, file=f)


def readConversation():
    with open(convo_file_path, 'r', encoding="utf-8") as file:
        try:
            data = json.load(file)
            if "default" in data:
                return data["default"]
            else:
                return []
        except (JSONDecodeError):
            return []
