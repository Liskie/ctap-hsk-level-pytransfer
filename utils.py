# -*- coding:UTF-8 -*-

class TokensDict():
    names = ["raw", "word", "tag", "lemma", "entity", "chunk"]
    def __init__(self, name):
        self.field = {
            "$type": "ai.lum.odinson.TokensField",
            "name": self.set_name(name),
            "tokens": list()
        }

    def set_name(self, name):
        if name not in TokensDict.names:
            raise AssertionError("name is not in presets")
        else:
            return name

    def __getitem__(self, key):
        return self.field[key]

    def __setitem__(self, key, value):
        self.field[key] = value

    def __delitem__(self, key):
        del self.field[key]

class GraphDict():
    def __init__(self):
        self.field = {
            "$type": "ai.lum.odinson.GraphField",
            "name": "dependencies",
            "edges": list(),
            "roots": list()
        }

    def __getitem__(self, key):
        return self.field[key]

    def __setitem__(self, key, value):
        self.field[key] = value

    def __delitem__(self, key):
        del self.field[key]

def read_text(path):
    with open(path, "r", encoding="utf-8") as fr:
        for line in fr:
            line = line.strip() 
            if line:
                yield line

def ssplit(text):
    essay = []
    for line in text.split(" "): 
        if line:
            essay.append(line)
    return(essay)
