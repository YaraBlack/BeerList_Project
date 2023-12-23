import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton,\
    QDialog, QGridLayout, QWidget, QFrame, QLineEdit, QScrollArea, QVBoxLayout

def gridTemplate(parent):
    layout = QGridLayout(parent)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    return layout


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("BeerList")
        self.setFixedSize(800, 600)
        
        self.createContent()
        
        self.show()
        
    def createContent(self):
            
        # Create Main Frame
        main_contentFrame = QFrame(self)
        self.setCentralWidget(main_contentFrame)
        
        # Create Main Layout
        main_contentLayout = gridTemplate(main_contentFrame)
        main_contentFrame.setLayout(main_contentLayout)
        main_contentFrame.setStyleSheet('QFrame {background-color: #F9D7AF; },\
            font-family: Arial; font-size: 8;')
        
        # User section
        # Create User section Frame
        user_contentFrame = QFrame(main_contentFrame)
        user_contentFrame.setFixedSize(800, 40)
        
        user_contentFrame.setStyleSheet('QFrame { border-bottom: 1px solid black;\
            background-color: #DCAE77;}')
        
        # Create User section Layout
        user_contentLayout = gridTemplate(user_contentFrame)
        user_contentFrame.setLayout(user_contentLayout)

        

        # Create buttons and inputs and set their size
        button_open = QPushButton("Open", user_contentFrame)
        button_open.setFixedSize(50, 20)
        
        button_save = QPushButton("Save", user_contentFrame)
        button_save.setFixedSize(50, 20)
        
        button_logIn = QPushButton("Log in", user_contentFrame)
        button_logIn.setFixedSize(100, 20)
        
        button_signUp = QPushButton("Sign Up", user_contentFrame)
        button_signUp.setFixedSize(100, 20)
        
        input_username = QLineEdit(user_contentFrame)
        input_username.setFixedSize(150, 20)
        
        input_password = QLineEdit(user_contentFrame)
        input_password.setFixedSize(150, 20)
        
        # Add elements to User section Frame's Layout
        user_contentLayout.setColumnMinimumWidth(0, 20)
        user_contentLayout.addWidget(button_open, 0, 1)
        user_contentLayout.setColumnMinimumWidth(2, 10)
        user_contentLayout.addWidget(button_save, 0, 3)
        user_contentLayout.setColumnMinimumWidth(4, 110)
        user_contentLayout.addWidget(input_username, 0, 5)
        user_contentLayout.setColumnMinimumWidth(6, 10)
        user_contentLayout.addWidget(input_password, 0, 7)
        user_contentLayout.setColumnMinimumWidth(8, 10)
        user_contentLayout.addWidget(button_logIn, 0, 9)
        user_contentLayout.setColumnMinimumWidth(10, 10)
        user_contentLayout.addWidget(button_signUp, 0, 11)
        
        # Edit section Frame
        edit_contentFrame = QFrame(main_contentFrame)
        edit_contentFrame.setFixedSize(300, 560)
        edit_contentFrame.setStyleSheet('QFrame { border-right: 1px solid black; }')
        
        # Edit section layout
        edit_contentLayout = gridTemplate(edit_contentFrame)
        edit_contentFrame.setLayout(edit_contentLayout)
        
        # Control panel section Frame
        controlPanel_contentFrame = QFrame(edit_contentFrame)
        controlPanel_contentFrame.setFixedSize(300, 40)
        controlPanel_contentFrame.setStyleSheet('QFrame { border-bottom: 1px solid black; }')
        
        # Control panel section Layout
        controlPanel_contentLayout = gridTemplate(controlPanel_contentFrame)
        controlPanel_contentFrame.setLayout(controlPanel_contentLayout)
        
        # Add buttons to the control panel
        button_addNew = QPushButton(controlPanel_contentFrame)
        button_addNew.setFixedSize(70, 20)
        
        button_remove = QPushButton(controlPanel_contentFrame)
        button_remove.setFixedSize(50, 20)
        
        
        controlPanel_contentLayout.setColumnMinimumWidth(0, 20)
        controlPanel_contentLayout.addWidget(button_addNew, 0, 1)
        controlPanel_contentLayout.setColumnMinimumWidth(2, 10)
        controlPanel_contentLayout.addWidget(button_remove, 0, 1)
        controlPanel_contentLayout.setColumnMinimumWidth(4, 150)
        

        
        
        # Input and info section Frame
        inputAndInfo_contentFrame = QFrame(edit_contentFrame)
        inputAndInfo_contentFrame.setFixedSize(300, 520)
        
        
        edit_contentLayout.addWidget(controlPanel_contentFrame, 0, 0)
        edit_contentLayout.addWidget(inputAndInfo_contentFrame, 1, 0)
        
        
        
        
        
        
        
        
        
        # List output section
        listOutput_contentFrame = QFrame(main_contentFrame)
        listOutput_contentFrame.setFixedSize(500, 560)
        
        # Add scroll bar to List output section
        listScrollBar = QScrollArea()
        listScrollBar.setWidget(listOutput_contentFrame)
        
        # Add layouts to Main Frame
        main_contentLayout.addWidget(user_contentFrame, 0, 0)
        main_contentLayout.addWidget(edit_contentFrame, 1, 0)
        main_contentLayout.addWidget(listOutput_contentFrame, 1, 1)
        

app = QApplication(sys.argv)
window = MainWindow()
app.exec()