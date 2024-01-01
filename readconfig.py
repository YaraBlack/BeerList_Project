import json

def readConfig():
    fileR = open("config.json", "r", encoding="utf-8")
    config = json.load(fileR)
    fileR.close()
    return config