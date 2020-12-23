def convert(text):
    text = text.replace(" ", "_")
    text = text.replace("(", "_")
    text = text.replace(")", "_")
    text = text.lower()
    return text
