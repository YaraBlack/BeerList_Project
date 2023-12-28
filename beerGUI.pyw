import sys
import os
from functools import partial
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton,\
    QGridLayout, QWidget, QFrame, QLineEdit, QDialog, QPlainTextEdit,\
    QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtGui import QPixmap
from filesHandler import *

def gridTemplate(parent):
    layout = QGridLayout(parent)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    return layout


class RegistrationForm(QDialog):
    def __init__(self):
        super(RegistrationForm, self).__init__()
        
        self.setWindowTitle("Registration")
        self.setFixedSize(300, 300)

    
    
    
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("BeerList")
        self.setFixedSize(800, 600)
        
        self.tempDict = {}
        self.imagePath = ""
        self.createContent()
        self.show()
        
        
    def setTable(self):
        self.table.setRowCount(len(self.tempDict))
        
        for i, (name, nameAttr) in enumerate(self.tempDict.items()):
            item_name = QTableWidgetItem(name)
            item_alco = QTableWidgetItem(nameAttr['alco'])
            item_ingr = QTableWidgetItem(nameAttr['ingr'])
            item_descr = QTableWidgetItem(nameAttr['descr'])
            self.table.setItem(i, 0, item_name)
            self.table.setItem(i, 1, item_alco)
            self.table.setItem(i, 2, item_ingr)
            self.table.setItem(i, 3, item_descr)
    
    def openDB(self):
        path = openSingleFile(self, "db")
        if path:
            jsonRead(path, self.tempDict)        
            self.setTable()
            self.clearEdit()
        else:
            print("Operation has been canceled!")
    
    def saveFile(self):
        path = saveSingleFile(self)
        if path:
            jsonWrite(path, self.tempDict)
        else:
            print("Operation has been canceled!")
    
    def clearEdit(self):
        self.input_beerName.setText("")
        self.input_beerAlco.setText("")
        self.input_beerIngr.setPlainText("")
        self.input_beerTaste.setPlainText("")
        self.imagePath = ""        
        self.addForm_layout.addWidget(self.img_placeholder, 0 ,0, 1, 3, Qt.AlignmentFlag.AlignHCenter)
    
    def inputsReadOnly(self, val: bool):
        self.input_beerName.setReadOnly(val)
        self.input_beerAlco.setReadOnly(val)
        self.input_beerIngr.setReadOnly(val)
        self.input_beerTaste.setReadOnly(val)
        self.button_addImage.setEnabled(not val)
    
    def setImage(self, source, sourcePath = ""):
        if source == "button":
            path = openSingleFile(self, "img")
        elif source == "func":
            path = sourcePath
            
        if path:
            self.imagePath = path
            self.label_image.setPixmap(QPixmap(path).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
            self.img_placeholder.setParent(None)
            self.addForm_layout.addWidget(self.label_image, 0, 0, 1, 3, Qt.AlignmentFlag.AlignHCenter)
        else:
            print("Operation has been canceled!")
        
    def addItemToTable(self):
        
        self.tempDict[self.input_beerName.text()] = {
            'alco': self.input_beerAlco.text(),
            'ingr': self.input_beerIngr.toPlainText(),
            'descr': self.input_beerTaste.toPlainText(),
            'imgPath': self.imagePath}
        print(self.tempDict)
        
        self.clearEdit()
        self.setTable()
        
    def addNew(self):
        self.clearEdit()
        self.inputsReadOnly(False)
        

    def removeItem(self):
        pass
    
    def editItem(self):
        pass

    def getDataFromTable(self, item: QTableWidgetItem):
        if(item.data(0) in self.tempDict):
            
            for key, value in self.tempDict.items():
                if 'imgPath' not in value:
                    self.tempDict[key]['imgPath'] = ""
            
            print(f"{item.data(0)} has values {self.tempDict[item.data(0)]}")
            self.input_beerName.setText(f"{item.data(0)}")
            self.input_beerAlco.setText(f"{self.tempDict[item.data(0)]['alco']}")
            self.input_beerIngr.setPlainText(f"{self.tempDict[item.data(0)]['ingr']}")
            self.input_beerTaste.setPlainText(f"{self.tempDict[item.data(0)]['descr']}")
            if self.tempDict[item.data(0)]['imgPath']:
                print(self.tempDict[item.data(0)]['imgPath'])
                self.setImage("func", self.tempDict[item.data(0)]['imgPath'])                
            else:
                self.addForm_layout.addWidget(self.img_placeholder, 0 ,0, 1, 3, Qt.AlignmentFlag.AlignHCenter)

            if not self.input_beerName.isReadOnly():
                self.inputsReadOnly(True)
        else:
            print("Wrong data! Either empty cell or not name cell!")
    
    def createContent(self):
            
        # Create Main Frame
        self.main_contentFrame = QFrame(self)
        self.setCentralWidget(self.main_contentFrame)
        
        # Create Main Layout
        self.main_contentLayout = gridTemplate(self.main_contentFrame)
        self.main_contentFrame.setLayout(self.main_contentLayout)
        self.main_contentFrame.setStyleSheet('QFrame {background-color: #F9D7AF; }')
        
###############################################################################
        
        # User section
        # Create User section Frame
        self.user_contentFrame = QFrame(self.main_contentFrame)
        self.user_contentFrame.setFixedSize(800, 40)
        
        self.user_contentFrame.setStyleSheet('QFrame { border-bottom: 1px solid black;\
            background-color: #DCAE77;}')
        
        # Create User section Layout
        self.user_contentLayout = gridTemplate(self.user_contentFrame)
        self.user_contentFrame.setLayout(self.user_contentLayout)
        self.user_contentLayout.setSpacing(10)

        # Create registration form to call later
        self.rForm = RegistrationForm()

        # Create buttons and inputs and set their size
        self.button_open = QPushButton("Open", self.user_contentFrame)
        self.button_open.setFixedSize(70, 25)
        
        
        self.button_save = QPushButton("Save", self.user_contentFrame)
        self.button_save.setFixedSize(70, 25)
        
        self.button_logIn = QPushButton("Log in", self.user_contentFrame)
        self.button_logIn.setFixedSize(100, 25)
        
        self.button_signUp = QPushButton("Sign Up", self.user_contentFrame)
        self.button_signUp.setFixedSize(100, 25)

        self.button_signUp.clicked.connect(self.rForm.show)
        
        self.input_username = QLineEdit(self.user_contentFrame)
        self.input_username.setFixedSize(150, 25)
        self.input_username.setPlaceholderText('Login')
        
        self.input_password = QLineEdit(self.user_contentFrame)
        self.input_password.setFixedSize(150, 25)
        self.input_password.setPlaceholderText('Password')
        
        # Add elements to User section Frame's Layout
        self.user_contentLayout.setColumnMinimumWidth(0, 10)
        self.user_contentLayout.addWidget(self.button_open, 0, 1)
        self.user_contentLayout.addWidget(self.button_save, 0, 2)
        self.user_contentLayout.setColumnMinimumWidth(3, 50)
        self.user_contentLayout.addWidget(self.input_username, 0, 4)
        self.user_contentLayout.addWidget(self.input_password, 0, 5)
        self.user_contentLayout.addWidget(self.button_logIn, 0, 6)
        self.user_contentLayout.addWidget(self.button_signUp, 0, 7)
        self.user_contentLayout.setColumnMinimumWidth(12, 10)
        
###############################################################################
        # Edit section
        # Edit section Frame
        self.edit_contentFrame = QFrame(self.main_contentFrame)
        self.edit_contentFrame.setFixedSize(300, 560)
        self.edit_contentFrame.setStyleSheet('QFrame { border-right: 1px solid black; }')
        
        # Edit section layout
        self.edit_contentLayout = gridTemplate(self.edit_contentFrame)
        self.edit_contentFrame.setLayout(self.edit_contentLayout)
        
        #Control panel section
        # Control panel section Frame
        self.controlPanel_contentFrame = QFrame(self.edit_contentFrame)
        self.controlPanel_contentFrame.setFixedSize(300, 40)
        self.controlPanel_contentFrame.setStyleSheet('QFrame { border-bottom: 1px solid black; }')
        
        # Control panel section Layout
        self.controlPanel_contentLayout = gridTemplate(self.controlPanel_contentFrame)
        self.controlPanel_contentFrame.setLayout(self.controlPanel_contentLayout)
        
        # Add buttons to the control panel
        self.button_addNew = QPushButton("Add New", self.controlPanel_contentFrame)
        self.button_addNew.setFixedSize(70, 25)
        
        
        self.button_remove = QPushButton("Remove", self.controlPanel_contentFrame)
        self.button_remove.setFixedSize(70, 25)
        self.button_remove.setEnabled(False)
        
        self.button_editContent = QPushButton("Edit", self.controlPanel_contentFrame)
        self.button_editContent.setFixedSize(70, 25)
        self.button_editContent.setEnabled(False)
        
        self.controlPanel_contentLayout.setColumnMinimumWidth(0, 20)
        self.controlPanel_contentLayout.addWidget(self.button_addNew, 0, 1)
        self.controlPanel_contentLayout.setColumnMinimumWidth(2, 20)
        self.controlPanel_contentLayout.addWidget(self.button_remove, 0, 3)
        self.controlPanel_contentLayout.setColumnMinimumWidth(4, 20)
        self.controlPanel_contentLayout.addWidget(self.button_editContent, 0, 5)
        self.controlPanel_contentLayout.setColumnMinimumWidth(6, 70)
        
        # Input and info section        
        # Input and info section Frame
        self.inputAndInfo_contentFrame = QFrame(self.edit_contentFrame)
        self.inputAndInfo_contentFrame.setFixedSize(300, 520)
        self.inputAndInfo_contentFrame.setStyleSheet("QFrame {background-color: orange; }")
        
        # # Input and info section Layout
        inputAndInfo_contentLayout = gridTemplate(self.inputAndInfo_contentFrame)
        self.inputAndInfo_contentFrame.setLayout(inputAndInfo_contentLayout)
        
        self.addForm = QWidget(self.inputAndInfo_contentFrame)
        self.addForm.setFixedSize(300, 520)
        self.addForm_layout = gridTemplate(self.addForm)
        self.addForm.setLayout(self.addForm_layout)
        self.addForm.setStyleSheet(" QLabel {border: 0px}")
        self.addForm_layout.setContentsMargins(10, 10, 10, 10)
        self.addForm_layout.setSpacing(5)
        
        
        self.button_addImage = QPushButton("Add image", self.addForm)
        self.button_addImage.setFixedSize(80, 25)

        
        self.button_confirmForm = QPushButton("Confirm", self.addForm)
        self.button_confirmForm.setFixedSize(80, 25)
        
        self.label_beerName = QLabel("Name of the beer:")
        
        self.label_beerAlco = QLabel("Alcohol in %:")
        
        self.label_beerIngr = QLabel("Ingredients:")
        
        self.label_beerTaste = QLabel("Taste description:")
        
        self.input_beerName = QLineEdit(self.addForm)
        self.input_beerName.setFixedSize(170, 25)
        
        self.input_beerAlco = QLineEdit(self.addForm)
        self.input_beerAlco.setFixedSize(170, 25)
        
        self.input_beerIngr = QPlainTextEdit(self.addForm)
        self.input_beerIngr.setFixedSize(170, 80)
        self.input_beerIngr.setStyleSheet("background-color: white")
        
        self.input_beerTaste = QPlainTextEdit(self.addForm)
        self.input_beerTaste.setFixedSize(170, 80)
        self.input_beerTaste.setStyleSheet("background-color: white")
        
        self.label_image = QLabel("", self.addForm)
        
        self.img_placeholder = QFrame(self.addForm)
        self.img_placeholder.setFixedSize(200, 200)
        self.img_placeholder.setStyleSheet("border: 1px solid black")
        
        
        
        self.addForm_layout.addWidget(self.img_placeholder, 0 ,0, 1, 3, Qt.AlignmentFlag.AlignHCenter)
        self.addForm_layout.addWidget(self.button_addImage, 1, 0, 1, 3, Qt.AlignmentFlag.AlignHCenter)
        self.addForm_layout.addWidget(self.label_beerName, 2, 0)
        self.addForm_layout.addWidget(self.input_beerName, 2, 1, 1, 2)
        self.addForm_layout.addWidget(self.label_beerAlco, 3, 0)
        self.addForm_layout.addWidget(self.input_beerAlco, 3, 1, 1, 2)
        self.addForm_layout.addWidget(self.label_beerIngr, 4, 0)
        self.addForm_layout.addWidget(self.input_beerIngr, 4, 1, 1, 2)
        self.addForm_layout.addWidget(self.label_beerTaste, 5, 0)
        self.addForm_layout.addWidget(self.input_beerTaste, 5, 1, 1, 2)
        self.addForm_layout.addWidget(self.button_confirmForm, 6, 0, 1, 3, Qt.AlignmentFlag.AlignHCenter)
        
        inputAndInfo_contentLayout.addWidget(self.addForm, 0, 0)
        

        
        self.edit_contentLayout.addWidget(self.controlPanel_contentFrame, 0, 0)
        self.edit_contentLayout.addWidget(self.inputAndInfo_contentFrame, 1, 0)
        
        
        
        
        
        
###############################################################################
        
        # List output section
        # List output section Frame
        listOutput_contentFrame = QFrame(self.main_contentFrame)
        listOutput_contentFrame.setFixedSize(500, 560)
        listOutput_contentLayout = gridTemplate(listOutput_contentFrame)
        listOutput_contentFrame.setLayout(listOutput_contentLayout)
        
        
        self.table = QTableWidget(listOutput_contentFrame)

        self.table.setRowCount(1)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Alc %", "Ingridients", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.table.setCornerButtonEnabled(False)
        self.table.setColumnWidth(0, 120)
        self.table.setColumnWidth(1, 46)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)
        
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        listOutput_contentLayout.addWidget(self.table, 0, 0)
        
        # Connect all Signals to Slots
        self.button_open.clicked.connect(self.openDB)
        self.button_save.clicked.connect(self.saveFile)
        self.button_addNew.clicked.connect(self.addNew)
        self.button_addImage.clicked.connect(partial(self.setImage, "button"))
        self.button_confirmForm.clicked.connect(self.addItemToTable)
        
        self.table.itemClicked.connect(self.getDataFromTable)

        
        # Add layouts to Main Frame
        self.main_contentLayout.addWidget(self.user_contentFrame, 0, 0)
        self.main_contentLayout.addWidget(self.edit_contentFrame, 1, 0)
        self.main_contentLayout.addWidget(listOutput_contentFrame, 1, 1, 1, 2)
        

app = QApplication(sys.argv)
window = MainWindow()
app.exec()