import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton,\
    QGridLayout, QWidget, QFrame, QLineEdit, QDialog, QPlainTextEdit,\
    QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtGui import QPixmap

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
        
        self.createContent()
        self.show()
        
    
    def callDialogWindow(self):
        self.window = RegistrationForm()
        self.window.show()
        
    def createContent(self):
            
        # Create Main Frame
        main_contentFrame = QFrame(self)
        self.setCentralWidget(main_contentFrame)
        
        # Create Main Layout
        main_contentLayout = gridTemplate(main_contentFrame)
        main_contentFrame.setLayout(main_contentLayout)
        main_contentFrame.setStyleSheet('QFrame {background-color: #F9D7AF; }')
        
###############################################################################
        
        # User section
        # Create User section Frame
        user_contentFrame = QFrame(main_contentFrame)
        user_contentFrame.setFixedSize(800, 40)
        
        user_contentFrame.setStyleSheet('QFrame { border-bottom: 1px solid black;\
            background-color: #DCAE77;}')
        
        # Create User section Layout
        user_contentLayout = gridTemplate(user_contentFrame)
        user_contentFrame.setLayout(user_contentLayout)

        # Create registration form to call later
        rForm = RegistrationForm()

        # Create buttons and inputs and set their size
        button_open = QPushButton("Open", user_contentFrame)
        button_open.setFixedSize(70, 25)
        
        button_save = QPushButton("Save", user_contentFrame)
        button_save.setFixedSize(70, 25)
        
        button_logIn = QPushButton("Log in", user_contentFrame)
        button_logIn.setFixedSize(100, 25)
        
        button_signUp = QPushButton("Sign Up", user_contentFrame)
        button_signUp.setFixedSize(100, 25)

        button_signUp.clicked.connect(self.callDialogWindow)
        
        input_username = QLineEdit(user_contentFrame)
        input_username.setFixedSize(150, 25)
        input_username.setPlaceholderText('Login')
        
        input_password = QLineEdit(user_contentFrame)
        input_password.setFixedSize(150, 25)
        input_password.setPlaceholderText('Password')
        
        # Add elements to User section Frame's Layout
        user_contentLayout.setColumnMinimumWidth(0, 20)
        user_contentLayout.addWidget(button_open, 0, 1)
        user_contentLayout.setColumnMinimumWidth(2, 10)
        user_contentLayout.addWidget(button_save, 0, 3)
        user_contentLayout.setColumnMinimumWidth(4, 70)
        user_contentLayout.addWidget(input_username, 0, 5)
        user_contentLayout.setColumnMinimumWidth(6, 10)
        user_contentLayout.addWidget(input_password, 0, 7)
        user_contentLayout.setColumnMinimumWidth(8, 10)
        user_contentLayout.addWidget(button_logIn, 0, 9)
        user_contentLayout.setColumnMinimumWidth(10, 10)
        user_contentLayout.addWidget(button_signUp, 0, 11)
        user_contentLayout.setColumnMinimumWidth(12, 20)
        
###############################################################################
        # Edit section
        # Edit section Frame
        edit_contentFrame = QFrame(main_contentFrame)
        edit_contentFrame.setFixedSize(300, 560)
        edit_contentFrame.setStyleSheet('QFrame { border-right: 1px solid black; }')
        
        # Edit section layout
        edit_contentLayout = gridTemplate(edit_contentFrame)
        edit_contentFrame.setLayout(edit_contentLayout)
        
        #Control panel section
        # Control panel section Frame
        controlPanel_contentFrame = QFrame(edit_contentFrame)
        controlPanel_contentFrame.setFixedSize(300, 40)
        controlPanel_contentFrame.setStyleSheet('QFrame { border-bottom: 1px solid black; }')
        
        # Control panel section Layout
        controlPanel_contentLayout = gridTemplate(controlPanel_contentFrame)
        controlPanel_contentFrame.setLayout(controlPanel_contentLayout)
        
        # Add buttons to the control panel
        button_addNew = QPushButton("Add New", controlPanel_contentFrame)
        button_addNew.setFixedSize(70, 25)
        
        button_remove = QPushButton("Remove", controlPanel_contentFrame)
        button_remove.setFixedSize(70, 25)
        
        button_editContent = QPushButton("Edit", controlPanel_contentFrame)
        button_editContent.setFixedSize(70, 25)
        
        controlPanel_contentLayout.setColumnMinimumWidth(0, 20)
        controlPanel_contentLayout.addWidget(button_addNew, 0, 1)
        controlPanel_contentLayout.setColumnMinimumWidth(2, 20)
        controlPanel_contentLayout.addWidget(button_remove, 0, 3)
        controlPanel_contentLayout.setColumnMinimumWidth(4, 20)
        controlPanel_contentLayout.addWidget(button_editContent, 0, 5)
        controlPanel_contentLayout.setColumnMinimumWidth(6, 70)
        
        # Input and info section
        # Input and info section Frame
        inputAndInfo_contentFrame = QFrame(edit_contentFrame)
        inputAndInfo_contentFrame.setFixedSize(300, 520)
        inputAndInfo_contentFrame.setStyleSheet("QFrame {background-color: orange; }")
        
        # # Input and info section Layout
        inputAndInfo_contentLayout = gridTemplate(inputAndInfo_contentFrame)
        inputAndInfo_contentFrame.setLayout(inputAndInfo_contentLayout)
        
        addForm = QWidget(inputAndInfo_contentFrame)
        addForm.setFixedSize(300, 520)
        addForm_layout = gridTemplate(addForm)
        addForm.setLayout(addForm_layout)
        addForm.setStyleSheet(" QLabel {border: 0px}")
        addForm_layout.setContentsMargins(10, 10, 10, 10)
        addForm_layout.setSpacing(5)
        
        
        button_addImage = QPushButton("Add image", addForm)
        button_addImage.setFixedSize(80, 25)
        
        button_confirmForm = QPushButton("Confirm", addForm)
        button_confirmForm.setFixedSize(80, 25)
        
        label_beerName = QLabel("Name of the beer:")
        
        label_beerAlco = QLabel("Alcohol in %:")
        
        label_beerIngr = QLabel("Ingredients:")
        
        label_beerTaste = QLabel("Taste description:")
        
        input_beerName = QLineEdit(addForm)
        input_beerName.setFixedSize(170, 25)
        
        input_beerAlco = QLineEdit(addForm)
        input_beerAlco.setFixedSize(170, 25)
        
        input_beerIngr = QPlainTextEdit(addForm)
        input_beerIngr.setFixedSize(170, 80)
        input_beerIngr.setStyleSheet("background-color: white")
        
        input_beerTaste = QPlainTextEdit(addForm)
        input_beerTaste.setFixedSize(170, 80)
        input_beerTaste.setStyleSheet("background-color: white")
        
        label_image = QLabel("Some text", addForm)
        original_image = QPixmap('resources/imgs/3.jpg').scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        label_image.setPixmap(original_image)
        
        img_placeholder = QFrame(addForm)
        img_placeholder.setFixedSize(200, 200)
        img_placeholder.setStyleSheet("border: 1px solid black")
        
        
        addForm_layout.addWidget(img_placeholder, 0 ,0, 1, 3, Qt.AlignmentFlag.AlignHCenter)
        addForm_layout.removeWidget(img_placeholder)
        addForm_layout.addWidget(label_image, 0, 0, 1, 3, Qt.AlignmentFlag.AlignHCenter)
        addForm_layout.addWidget(button_addImage, 1, 0, 1, 3, Qt.AlignmentFlag.AlignHCenter)
        addForm_layout.addWidget(label_beerName, 2, 0)
        addForm_layout.addWidget(input_beerName, 2, 1, 1, 2)
        addForm_layout.addWidget(label_beerAlco, 3, 0)
        addForm_layout.addWidget(input_beerAlco, 3, 1, 1, 2)
        addForm_layout.addWidget(label_beerIngr, 4, 0)
        addForm_layout.addWidget(input_beerIngr, 4, 1, 1, 2)
        addForm_layout.addWidget(label_beerTaste, 5, 0)
        addForm_layout.addWidget(input_beerTaste, 5, 1, 1, 2)
        addForm_layout.addWidget(button_confirmForm, 6, 0, 1, 3, Qt.AlignmentFlag.AlignHCenter)
        
        inputAndInfo_contentLayout.addWidget(addForm, 0, 0)
        
        
        edit_contentLayout.addWidget(controlPanel_contentFrame, 0, 0)
        edit_contentLayout.addWidget(inputAndInfo_contentFrame, 1, 0)
        
        
        
        
        
        
###############################################################################
        
        # List output section
        # List output section Frame
        listOutput_contentFrame = QFrame(main_contentFrame)
        listOutput_contentFrame.setFixedSize(500, 560)
        listOutput_contentLayout = gridTemplate(listOutput_contentFrame)
        listOutput_contentFrame.setLayout(listOutput_contentLayout)
        
        
        table = QTableWidget(listOutput_contentFrame)

        table.setRowCount(2)
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Name", "Alc %", "Ingridients", "Description"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        table.setCornerButtonEnabled(False)
        table.setColumnWidth(0, 120)
        table.setColumnWidth(1, 46)
        table.setColumnWidth(2, 150)
        table.setColumnWidth(3, 150)
        
        
        listOutput_contentLayout.addWidget(table, 0, 0)
        
        
        
        
        # Add layouts to Main Frame
        main_contentLayout.addWidget(user_contentFrame, 0, 0)
        main_contentLayout.addWidget(edit_contentFrame, 1, 0)
        main_contentLayout.addWidget(listOutput_contentFrame, 1, 1, 1, 2)
        

app = QApplication(sys.argv)
window = MainWindow()
app.exec()