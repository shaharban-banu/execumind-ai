import re

def tokenize(text: str) -> list[str]:
    text = text.lower()
    return re.findall(r"\w+", text)