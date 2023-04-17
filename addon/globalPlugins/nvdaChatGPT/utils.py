def extract_json_from_exception(text):
    start_index = text.find('{')

    if start_index != -1:
        return text[start_index:]
    else:
        return None
