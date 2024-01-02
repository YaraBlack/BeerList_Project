import sys
import requests
from functools import partial
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton,\
    QGridLayout, QWidget, QFrame, QLineEdit, QDialog, QPlainTextEdit,\
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QVBoxLayout
from PyQt6.QtGui import QPixmap, QRegularExpressionValidator, QIcon
from filesHandler import *




class RegistrationForm(QDialog):
    def __init__(self):
        super(RegistrationForm, self).__init__()
        
        self.setWindowTitle("Registration")
        self.setFixedSize(170, 200)
        self.setWindowIcon(QIcon("resources/icons/icon2.png"))
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        self.AttMessageBox = AttentionMessageBox()
        self.OKMessageBox = OKMessageBox()
                
        self.reg_layout = QVBoxLayout()
        self.setLayout(self.reg_layout)
        
        self.label_userName = QLabel("Username:")
        self.label_password = QLabel("Password:")
        
        self.input_regLogin = QLineEdit()
        self.input_regLogin.setFixedSize(150, 25)
        self.input_regLogin.setMaxLength(20)
        
        self.input_regPass = QLineEdit()
        self.input_regPass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_regPass.setMaxLength(20)
        self.input_regPass.setFixedSize(150, 25)
        
        self.button_register = QPushButton("Submit")
        self.button_register.setFixedSize(50, 25)
        
        self.reg_layout.addWidget(self.label_userName)
        self.reg_layout.addWidget(self.input_regLogin)
        self.reg_layout.addWidget(self.label_password)
        self.reg_layout.addWidget(self.input_regPass)
        self.reg_layout.addWidget(self.button_register, 1,
                                  Qt.AlignmentFlag.AlignHCenter)
        
        self.button_register.clicked.connect(self.regSubmit)
    
    def regSubmit(self):
        if self.input_regLogin.text() and self.input_regPass.text():
            registration_endpoint = "http://localhost:5001/register"
            
            data = {"username": self.input_regLogin.text(),
                    "password": self.input_regPass.text()}
            try:
                response = requests.post(registration_endpoint, json=data)
                
                if response.status_code == 200:
                    print("Registration successful!")
                    self.OKMessageBox.invokeMsgBox(1)
                    self.input_regLogin.setText("")
                    self.input_regPass.setText("")
                    self.close()
                elif response.status_code == 500:
                    self.AttMessageBox.invokeMsgBox(4)
                else:
                    print("Registration failed.", response.status_code,
                          response.text)
                    self.AttMessageBox.invokeMsgBox(5)
            except Exception as e:
                print("Error:", e)
        
        else:
            self.AttMessageBox.invokeMsgBox(1)
        

class OKMessageBox(QMessageBox):
    def __init__(self):
        super(OKMessageBox, self).__init__()
            
        self.setWindowTitle("Success!")
        self.setWindowIcon(QIcon("resources/icons/icon2.png"))
        
    def invokeMsgBox(self, msgType: int):
        match msgType:
            case 1:
                self.setText("Registation completed!")
            case 2:
                self.setText("Logged in successfully!")
                
        self.exec()

class AttentionMessageBox(QMessageBox):
    def __init__(self):
        super(AttentionMessageBox,self).__init__()
        
        self.setWindowTitle("Attention!")
        self.setIcon(QMessageBox.Icon.Warning)
        self.setWindowIcon(QIcon("resources/icons/icon2.png"))   
    
    def invokeMsgBox(self, msgType: int):
        match msgType:
            case 1:
                self.setText("One of the fields is empty!")
            case 2:
                self.setText("The alcohol percentage is entered incorrectly!")
            case 3:
                self.setText("The points are entered incorrectly!")
            case 4:
                self.setText("User with such username already exists!")
            case 5:
                self.setText("Error! There's problem with a request!")
            case 6:
                self.setText("Invalid username or password!")
            case 7:
                self.setText("Error! Wrong JSON values!")
            case 8:
                self.setText("Error! Wrong JSON structure!")
                
        self.exec()

class NumericTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except ValueError:
            return super().__lt__(other)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("BeerList")
        self.setFixedSize(800, 600)
        self.setWindowIcon(QIcon("resources/icons/icon2.png"))
        
        
        self.tempDict = {}
        self.imagePath = ""
        self.activeRow = 0
        self.createContent()
        self.changeState(val=True, state="start")
        self.show()
        
    def gridTemplate(self, parent):
        layout = QGridLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        return layout
        
    def setTable(self, setDict: dict):
        self.table.setRowCount(len(setDict))
        
        for i, (name, nameAttr) in enumerate(setDict.items()):
            item_name = QTableWidgetItem(name)
            item_alco = NumericTableWidgetItem(nameAttr['alco'])
            item_grade = NumericTableWidgetItem(nameAttr['grade'])
            item_ingr = QTableWidgetItem(nameAttr['ingr'])
            item_descr = QTableWidgetItem(nameAttr['descr'])
            self.table.setItem(i, 0, item_name)
            self.table.setItem(i, 1, item_alco)
            self.table.setItem(i, 2, item_grade)
            self.table.setItem(i, 3, item_ingr)
            self.table.setItem(i, 4, item_descr)
    
    def openDB(self):
        path = openSingleFile(self, "db")
        if path:
            try:
                jsonRead(path, self.tempDict)        
                self.setTable(self.tempDict)
                self.addNew()
            except TypeError as e:
                print("Error! Check JSON values!\n", e)
                self.AttMessageBox.invokeMsgBox(7)
            except KeyError as e:
                print("Error! Wrong JSON structure!\n", e, "is absent.")
                self.AttMessageBox.invokeMsgBox(8)
        else:
            print("Operation has been canceled!")
    
    def saveFile(self):
        path = saveSingleFile(self)
        if path:
            jsonWrite(path, self.tempDict, "w")
        else:
            print("Operation has been canceled!")
    
    def clearEdit(self):
        self.input_beerName.setText("")
        self.input_beerAlco.setText("")
        self.input_beerPoints.setText("")
        self.input_beerIngr.setPlainText("")
        self.input_beerTaste.setPlainText("")
        self.imagePath = ""        
        self.addForm_layout.addWidget(self.img_placeholder, 0 ,0, 1, 5,
                                      Qt.AlignmentFlag.AlignHCenter)
    
    def changeState(self, val: bool, editBtnPressed=False, state: str="std"):
        if state == "start":
            self.button_open.setEnabled(not val)
            self.button_save.setEnabled(not val)
            self.button_addNew.setEnabled(not val)
            self.button_addImage.setEnabled(not val)
            self.button_confirmForm.setEnabled(not val)
            self.input_beerName.setReadOnly(val)
            self.input_beerAlco.setReadOnly(val)
            self.input_beerPoints.setReadOnly(val)
            self.input_beerIngr.setReadOnly(val)
            self.input_beerTaste.setReadOnly(val)
        elif state == "loggedIn":
            self.button_open.setEnabled(val)
            self.button_save.setEnabled(val)
            self.button_addNew.setEnabled(val)
            self.button_addImage.setEnabled(val)
            self.button_confirmForm.setEnabled(val)
            self.input_beerName.setReadOnly(not val)
            self.input_beerAlco.setReadOnly(not val)
            self.input_beerPoints.setReadOnly(not val)
            self.input_beerIngr.setReadOnly(not val)
            self.input_beerTaste.setReadOnly(not val)


        else:
            self.input_beerName.setReadOnly(val)
            self.input_beerAlco.setReadOnly(val)
            self.input_beerPoints.setReadOnly(val)
            self.input_beerIngr.setReadOnly(val)
            self.input_beerTaste.setReadOnly(val)
            self.button_addImage.setEnabled(not val)
            self.button_confirmForm.setEnabled(not val)
            if not editBtnPressed:
                self.button_remove.setEnabled(val)
                self.button_editContent.setEnabled(val)
            
    
    def setImage(self, source, sourcePath = ""):
        if source == "button":
            path = openSingleFile(self, "img")
        elif source == "func":
            path = sourcePath
        else:
            print("Wrong function call!")
            
        if path:
            self.imagePath = path
            self.label_image.setPixmap(QPixmap(path).scaled(200, 200,
                                        Qt.AspectRatioMode.KeepAspectRatio))
            self.img_placeholder.setParent(None)
            self.addForm_layout.addWidget(self.label_image, 0, 0, 1, 5,
                                        Qt.AlignmentFlag.AlignHCenter)
        else:
            print("Operation has been canceled!")
    
    def checkFloatInput(self):
        alcCheck = self.input_beerAlco.text().split(".")
        pointsCheck = self.input_beerPoints.text().split(".")
        errCounter = 0
        if not (self.input_beerName.text() and self.input_beerAlco.text() and
            self.input_beerPoints.text() and self.input_beerIngr.toPlainText() and
            self.input_beerTaste.toPlainText()):
            self.AttMessageBox.invokeMsgBox(1)
            errCounter += 1
        elif len(alcCheck) > 1:
            if not alcCheck[1]:
                self.AttMessageBox.invokeMsgBox(2)
                errCounter += 1
        elif len(pointsCheck) > 1:
            if not pointsCheck[1]:
                self.AttMessageBox.invokeMsgBox(3)
                errCounter += 1
        
        if errCounter:
            return False
        else:
            return True
        
    def addItemToTable(self, state: str):
        if self.checkFloatInput():
            if state == "new":
                self.tempDict[self.input_beerName.text()] = {
                    'alco': self.input_beerAlco.text(),
                    'grade': self.input_beerPoints.text(),
                    'ingr': self.input_beerIngr.toPlainText(),
                    'descr': self.input_beerTaste.toPlainText(),
                    'imgPath': self.imagePath}
            elif state == "edit":
                editedItem = {}
            
                editedItem[self.input_beerName.text()] = {
                    'alco': self.input_beerAlco.text(),
                    'grade': self.input_beerPoints.text(),
                    'ingr': self.input_beerIngr.toPlainText(),
                    'descr': self.input_beerTaste.toPlainText(),
                    'imgPath': self.imagePath}
            
                self.tempDict = dict(list(self.tempDict.items())[:self.activeRow] +
                                    list(editedItem.items()) +
                                    list(self.tempDict.items())[self.activeRow + 1:])
                
                print("Edited successfully!")
            
            self.clearEdit()
            self.setTable(self.tempDict)
        else:
            print("AttentionMessageBox has been invoked!")
        
    def addNew(self):
        self.clearEdit()
        self.changeState(False)
        self.button_confirmForm.clicked.disconnect()
        self.button_confirmForm.clicked.connect(partial(self.addItemToTable,
                                                        "new"))
        

    def removeItem(self):
        delKey = ""
        for index, key in enumerate(self.tempDict):
            if key == self.input_beerName.text():
                self.table.removeRow(index)
                delKey = key
        if self.table.rowCount() == 0:
            self.table.setRowCount(1)
        self.addNew()
        print(f"The item {self.tempDict.pop(delKey)} has been deleted!")

    
    def editItem(self):
        self.changeState(False, True)
        
        self.button_confirmForm.clicked.disconnect()
        self.button_confirmForm.clicked.connect(partial(self.addItemToTable,
                                                        "edit"))
        

    def getDataFromTable(self, item: QTableWidgetItem):
        self.activeRow = item.row()
        if item.column() == 0:
            if(item.data(0) in self.tempDict):
                
                print(f"{item.data(0)} has values {self.tempDict[item.data(0)]}")
                self.input_beerName.setText(f"{item.data(0)}")
                self.input_beerAlco.setText(f"{self.tempDict[item.data(0)]['alco']}")
                self.input_beerPoints.setText(f"{self.tempDict[item.data(0)]['grade']}")
                self.input_beerIngr.setPlainText(f"{self.tempDict[item.data(0)]['ingr']}")
                self.input_beerTaste.setPlainText(f"{self.tempDict[item.data(0)]['descr']}")
                if self.tempDict[item.data(0)]['imgPath']:
                    self.setImage("func", self.tempDict[item.data(0)]['imgPath'])                
                else:
                    self.addForm_layout.addWidget(self.img_placeholder, 0 ,0, 1, 5,
                                                Qt.AlignmentFlag.AlignHCenter)
                
                
                if not self.input_beerName.isReadOnly():
                    self.changeState(True)
            else:
                print("Data isn't in dictionary!")
    
    def search(self):
        searchBeer = self.input_searchBar.text()
        if searchBeer in self.tempDict:
            searchItem = {searchBeer: self.tempDict[searchBeer]}
            self.setTable(searchItem)
        elif searchBeer == "":
            self.setTable(self.tempDict)
            
    
    def logout(self):
        self.label_user.setText("")
        self.changeAuthElements(False)
        self.changeState(val=True, state="start")
    
    def login(self):
        if self.input_username.text() and self.input_password.text():
            auth_endpoint = "http://localhost:5001/login"
            
            data = {"username": self.input_username.text(),
                    "password": self.input_password.text()}
            try:
                response = requests.post(auth_endpoint, json=data)
                
                if response.status_code == 200:
                    print("Authentication successful!")
                    self.OKMessageBox.invokeMsgBox(2)
                    self.changeState(val=True, state="loggedIn")
                    self.changeAuthElements(True)
                    self.label_user.setText(f"Hello, \
{self.input_username.text()}!")
                    self.input_username.setText("")
                    self.input_password.setText("")
                elif response.status_code == 401:
                    print("Invalid username or password!")
                    self.AttMessageBox.invokeMsgBox(6)
                else:
                    print("Authentication failed.",response.status_code,
                          response.text)
            except Exception as e:
                print("Error:", e)
            
            

    
    def changeAuthElements(self, isLogged):
        if isLogged:
            self.input_username.setParent(None)
            self.input_password.setParent(None)
            self.button_logIn.setParent(None)
            self.button_signUp.setParent(None)
            self.auth_frameLayout.addWidget(self.label_user, 0, 1)
            self.auth_frameLayout.addWidget(self.button_logOut, 0, 2)
            self.user_wrapperLayout.addWidget(self.search_frame, 0, 1)
            self.user_wrapperLayout.addWidget(self.auth_frame, 0, 2)
            self.user_wrapperLayout.setColumnMinimumWidth(2, 300)
        else:
            self.label_user.setParent(None)
            self.button_logOut.setParent(None)
            self.search_frame.setParent(None)
            self.auth_frameLayout.addWidget(self.input_username, 0, 1)
            self.auth_frameLayout.addWidget(self.input_password, 0, 2)
            self.auth_frameLayout.addWidget(self.button_logIn, 0, 3)
            self.auth_frameLayout.addWidget(self.button_signUp, 0, 4)
            self.user_wrapperLayout.addWidget(self.auth_frame, 0, 1)
            self.user_wrapperLayout.setColumnMinimumWidth(2, 0)
    
    def createContent(self):
            
        # Create Main Frame
        self.main_contentFrame = QFrame(self)
        self.setCentralWidget(self.main_contentFrame)
        
        # Create Main Layout
        self.main_contentLayout = self.gridTemplate(self.main_contentFrame)
        self.main_contentFrame.setLayout(self.main_contentLayout)
        self.main_contentFrame.setStyleSheet('QFrame \
                                {background-color: #F9D7AF; }')

        # Create message boxes to call later
        self.AttMessageBox = AttentionMessageBox()
        self.OKMessageBox = OKMessageBox()

        # Create registration form to call later
        self.rForm = RegistrationForm()
        
###############################################################################
        
        # User section
        # Create User section Frame
        self.user_contentFrame = QFrame(self.main_contentFrame)
        self.user_contentFrame.setFixedSize(800, 40)
        
        self.user_contentFrame.setStyleSheet("""
            QFrame {
                border-bottom: 1px solid black;
                background-color: #DCAE77;
                }
            
            QLabel {
                border: 0px
                }
            """)
        
        # Create User section Layout
        self.user_wrapperLayout = self.gridTemplate(self.user_contentFrame)
        self.user_contentFrame.setLayout(self.user_wrapperLayout)
        
        self.files_frame = QFrame(self.user_contentFrame)
        self.files_frameLayout = self.gridTemplate(self.files_frame)
        self.files_frameLayout.setSpacing(10)
        self.files_frame.setStyleSheet("border-right: 1px solid black")
        
        self.auth_frame = QFrame(self.user_contentFrame)
        self.auth_frameLayout = self.gridTemplate(self.auth_frame)
        self.auth_frame.setLayout(self.auth_frameLayout)
        
        self.search_frame = QFrame(self.user_contentFrame)
        self.search_frameLayout = self.gridTemplate(self.search_frame)
        self.search_frame.setLayout(self.search_frameLayout)
        self.search_frame.setStyleSheet("border-right: 1px solid black")
        self.search_frame.setParent(None)
        
        self.user_wrapperLayout.addWidget(self.files_frame, 0, 0)
        self.user_wrapperLayout.addWidget(self.auth_frame, 0, 1)
        

        # Create buttons and inputs and set their size
        self.button_open = QPushButton("Open", self.files_frame)
        self.button_open.setFixedSize(70, 25)
        
        
        self.button_save = QPushButton("Save", self.files_frame)
        self.button_save.setFixedSize(70, 25)
        
        self.button_logIn = QPushButton("Log in", self.auth_frame)
        self.button_logIn.setFixedSize(100, 25)
        
        self.button_signUp = QPushButton("Sign Up", self.auth_frame)
        self.button_signUp.setFixedSize(100, 25)

        self.button_logOut = QPushButton("Log Out", self.search_frame)
        self.button_logOut.setFixedSize(100, 25)
        
        self.label_user = QLabel()
        self.label_user.setFixedSize(180, 25)
        
        self.input_searchBar = QLineEdit(self.search_frame)
        self.input_searchBar.setFixedSize(250, 25)
        self.input_searchBar.setPlaceholderText('Search')
        
        self.input_username = QLineEdit(self.auth_frame)
        self.input_username.setFixedSize(150, 25)
        self.input_username.setPlaceholderText('Login')
        self.input_username.setMaxLength(20)
        
        self.input_password = QLineEdit(self.auth_frame)
        self.input_password.setFixedSize(150, 25)
        self.input_password.setPlaceholderText('Password')
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setMaxLength(20)
        
        # Add elements to User section Frame's Layout
        self.files_frameLayout.setColumnMinimumWidth(0, 20)
        self.files_frameLayout.addWidget(self.button_open, 0, 1)
        self.files_frameLayout.addWidget(self.button_save, 0, 2)
        self.files_frameLayout.setColumnMinimumWidth(3, 20)
        
        self.search_frameLayout.setColumnMinimumWidth(0, 10)
        self.search_frameLayout.addWidget(self.input_searchBar, 0, 1)
        self.search_frameLayout.setColumnMinimumWidth(2, 10)
        
        self.auth_frameLayout.setColumnMinimumWidth(0, 10)
        self.auth_frameLayout.addWidget(self.input_username, 0, 1)
        self.auth_frameLayout.addWidget(self.input_password, 0, 2)
        self.auth_frameLayout.addWidget(self.button_logIn, 0, 3)
        self.auth_frameLayout.addWidget(self.button_signUp, 0, 4)
        self.auth_frameLayout.setColumnMinimumWidth(5, 20)
        
###############################################################################
        # Edit section
        # Edit section Frame
        self.edit_contentFrame = QFrame(self.main_contentFrame)
        self.edit_contentFrame.setFixedSize(300, 560)
        self.edit_contentFrame.setStyleSheet('QFrame \
                                { border-right: 1px solid black; }')
        
        # Edit section layout
        self.edit_contentLayout = self.gridTemplate(self.edit_contentFrame)
        self.edit_contentFrame.setLayout(self.edit_contentLayout)
        
        #Control panel section
        # Control panel section Frame
        self.controlPanel_contentFrame = QFrame(self.edit_contentFrame)
        self.controlPanel_contentFrame.setFixedSize(300, 40)
        self.controlPanel_contentFrame.setStyleSheet('QFrame \
                                        { border-bottom: 1px solid black; }')
        
        # Control panel section Layout
        self.controlPanel_contentLayout = self.gridTemplate(self.controlPanel_contentFrame)
        self.controlPanel_contentFrame.setLayout(self.controlPanel_contentLayout)
        
        # Add buttons to the control panel
        self.button_addNew = QPushButton("Add New",
                                         self.controlPanel_contentFrame)
        self.button_addNew.setFixedSize(70, 25)
        
        self.button_remove = QPushButton("Remove",
                                         self.controlPanel_contentFrame)
        self.button_remove.setFixedSize(70, 25)
        self.button_remove.setEnabled(False)
        
        self.button_editContent = QPushButton("Edit",
                                              self.controlPanel_contentFrame)
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
        self.inputAndInfo_contentFrame.setStyleSheet("QFrame \
                                        {background-color: orange;}")
        
        # # Input and info section Layout
        inputAndInfo_contentLayout = self.gridTemplate(self.inputAndInfo_contentFrame)
        self.inputAndInfo_contentFrame.setLayout(inputAndInfo_contentLayout)
        
        self.addForm = QWidget(self.inputAndInfo_contentFrame)
        self.addForm.setFixedSize(300, 520)
        self.addForm_layout = self.gridTemplate(self.addForm)
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
        
        self.label_beerPoints = QLabel("Points:")
        
        self.label_beerIngr = QLabel("Ingredients:")
        
        self.label_beerTaste = QLabel("Taste description:")
        
        self.input_beerName = QLineEdit(self.addForm)
        self.input_beerName.setFixedSize(170, 25)
        
        self.input_beerAlco = QLineEdit(self.addForm)
        self.input_beerAlco.setFixedSize(40, 25)
        
        self.input_beerPoints = QLineEdit(self.addForm)
        self.input_beerPoints.setFixedSize(40, 25)
        
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
        
        # Add validator to alcohol percentage
        rx_alco = QRegularExpression(r'^\d$|^(?:\d\.\d){0,1}$')
        alcoRegEx = QRegularExpressionValidator(rx_alco)
        self.input_beerAlco.setValidator(alcoRegEx)
        
        # Add validation to points input
        rx_points = QRegularExpression(r'^\d$|^(?:\d\.\d){0,1}$')
        pointsRegEx = QRegularExpressionValidator(rx_points)
        self.input_beerPoints.setValidator(pointsRegEx)
        
        self.addForm_layout.addWidget(self.img_placeholder, 0 ,0, 1, 5,
                                      Qt.AlignmentFlag.AlignHCenter)
        self.addForm_layout.addWidget(self.button_addImage, 1, 0, 1, 5,
                                      Qt.AlignmentFlag.AlignHCenter)
        self.addForm_layout.addWidget(self.label_beerName, 2, 0)
        self.addForm_layout.addWidget(self.input_beerName, 2, 1, 1, 4)
        self.addForm_layout.addWidget(self.label_beerAlco, 3, 0)
        self.addForm_layout.addWidget(self.input_beerAlco, 3, 1)
        self.addForm_layout.addWidget(self.label_beerPoints, 3, 3)
        self.addForm_layout.addWidget(self.input_beerPoints, 3, 4)
        self.addForm_layout.setColumnMinimumWidth(5, 10)
        self.addForm_layout.addWidget(self.label_beerIngr, 4, 0)
        self.addForm_layout.addWidget(self.input_beerIngr, 4, 1, 1, 4)
        self.addForm_layout.addWidget(self.label_beerTaste, 5, 0)
        self.addForm_layout.addWidget(self.input_beerTaste, 5, 1, 1, 4)
        self.addForm_layout.addWidget(self.button_confirmForm, 6, 0, 1, 5,
                                      Qt.AlignmentFlag.AlignHCenter)
        
        inputAndInfo_contentLayout.addWidget(self.addForm, 0, 0)
        

        
        self.edit_contentLayout.addWidget(self.controlPanel_contentFrame, 0, 0)
        self.edit_contentLayout.addWidget(self.inputAndInfo_contentFrame, 1, 0)
             
###############################################################################
        # List output section
        # List output section Frame
        listOutput_contentFrame = QFrame(self.main_contentFrame)
        listOutput_contentFrame.setFixedSize(500, 560)
        listOutput_contentLayout = self.gridTemplate(listOutput_contentFrame)
        listOutput_contentFrame.setLayout(listOutput_contentLayout)
        
        self.table = QTableWidget(listOutput_contentFrame)

        self.table.setRowCount(1)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Alc %", "Rating",
                                              "Ingridients", "Description"])
        # self.table.setModel()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.table.setSortingEnabled(True)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.table.setCornerButtonEnabled(False)
        self.table.setColumnWidth(0, 120)
        self.table.setColumnWidth(1, 46)
        self.table.setColumnWidth(2, 50)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(3, 150)
        
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        listOutput_contentLayout.addWidget(self.table, 0, 0)
        
        # Connect all Signals to Slots
        self.button_open.clicked.connect(self.openDB)
        self.button_save.clicked.connect(self.saveFile)
        self.button_logIn.clicked.connect(self.login)
        self.button_signUp.clicked.connect(self.rForm.show)
        self.button_logOut.clicked.connect(self.logout)
        self.input_searchBar.textEdited.connect(self.search)
        self.button_addNew.clicked.connect(self.addNew)
        self.button_remove.clicked.connect(self.removeItem)
        self.button_editContent.clicked.connect(self.editItem)
        self.button_addImage.clicked.connect(partial(self.setImage, "button"))
        self.button_confirmForm.clicked.connect(partial(self.addItemToTable,
                                                        "new"))
        
        self.table.itemClicked.connect(self.getDataFromTable)
        
        # Add layouts to Main Frame
        self.main_contentLayout.addWidget(self.user_contentFrame, 0, 0)
        self.main_contentLayout.addWidget(self.edit_contentFrame, 1, 0)
        self.main_contentLayout.addWidget(listOutput_contentFrame, 1, 1, 1, 2)
        

app = QApplication(sys.argv)
window = MainWindow()
app.exec()