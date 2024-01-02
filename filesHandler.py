import json
import os
from PyQt6.QtWidgets import QFileDialog

# Return a path to open a file
def openSingleFile(parentWidget, fileType: str) -> str:
    file_filter = ""
    if fileType == "img":
        file_filter = "Image file (*.bpm *.jpg *.jpeg *.png)"
    elif fileType == "db":
        file_filter = "JSON file (*.json)"
    path, _ = QFileDialog.getOpenFileName(
                            parent = parentWidget,
                            caption = 'Select a file',
                            directory = os.getcwd(),
                            filter = file_filter
    )
    
    return str(path)

# Return a path to save a file
def saveSingleFile(parentWidget) -> str:
    file_filter = "JSON file (*.json)"
    path, _ = QFileDialog.getSaveFileName(
        parent = parentWidget,
        caption = 'Save as',
        directory = os.getcwd(),
        filter = file_filter
    )
    
    return str(path)

# Write to file
def jsonWrite(path: str, myDict: dict, mode: str) -> None:
    try:
        fileW = open(path, mode, encoding = "utf-8")
        json.dump(myDict, fileW, ensure_ascii = False, indent = 4)
    except FileNotFoundError as error:
        print("Error!", error)
    else:
        fileW.close()
        print("The file has been written successfully!\n")
        

# Read from file
def jsonRead(path: str, myDict: dict) -> None:
    try:
        fileR = open(path, "r", encoding = "utf-8")
        data_from_file = json.load(fileR)
    except FileNotFoundError as error:
        print("Error!", error)
    else:
        fileR.close()
        myDict.clear()
        myDict.update(data_from_file)
        print("The file has been read successfully!\n")
    
