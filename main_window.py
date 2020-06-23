import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QDialog, QPushButton, QLineEdit, QComboBox, QToolButton, QTextEdit, QCalendarWidget, QVBoxLayout
from PySide2.QtCore import QFile, QObject, Qt
from datetime import datetime

from event_handlers import Handlers


class MainWindow(QObject):
    def __init__(self, ui_file, parent=None):
        super(MainWindow, self).__init__(parent)

        ## define and open QtCreator ui file
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        
        ## define the file loader and assign it to the window
        loader = QUiLoader()
        self.window = loader.load(ui_file)

        ## close the ui file
        ui_file.close()
        
        ## connect ui buttons to variables
            # date select button
        dateSelectButton = self.window.findChild(QToolButton, 'dateSelectButton')
        dateSelectButton.setArrowType(Qt.DownArrow)
        dateSelectButton.clicked.connect(self.handle_dateSelectButton)
            # generate button
        generateButton = self.window.findChild(QPushButton, 'generateButton')
        generateButton.clicked.connect(self.handle_generateButton)

            # print button
        printButton = self.window.findChild(QPushButton, 'printButton')
        printButton.clicked.connect(self.handle_printButton)

        ## connect ui inputs to variables
            # store combo
        self.storeCombo = self.window.findChild(QComboBox, 'storeCombo')
            # date
        self.dateDisplay = self.window.findChild(QLineEdit, 'dateDisplay')
        self.dateDisplay.setText(datetime.today().strftime('%d/%m/%Y'))
            # staff input box
        self.staffEdit = self.window.findChild(QLineEdit, 'staffEdit')
            # cash put aside input box
        self.cashAsideEdit = self.window.findChild(QLineEdit, 'cashAsideEdit')
            # cash 100's input box
        self.cash100Edit = self.window.findChild(QLineEdit, 'cash100Edit')
            # cash 50's input box
        self.cash50Edit = self.window.findChild(QLineEdit, 'cash50Edit')
            # cash 20's input box
        self.cash20Edit = self.window.findChild(QLineEdit, 'cash20Edit')
            # cash 10's input box
        self.cash10Edit = self.window.findChild(QLineEdit, 'cash10Edit')
        # cash 5's input box
        self.cash5Edit = self.window.findChild(QLineEdit, 'cash5Edit')
            # cash coins input box
        self.cashCoinsEdit = self.window.findChild(QLineEdit, 'cashCoinsEdit')
            # cash register input box
        self.cashRegisterEdit = self.window.findChild(QLineEdit, 'cashRegisterEdit')
            # eftpos actual input box
        self.eftActualEdit = self.window.findChild(QLineEdit, 'eftActualEdit')
            # eftpos register input box
        self.eftRegisterEdit = self.window.findChild(QLineEdit, 'eftRegisterEdit')
            # epay actual input box
        self.epayActualEdit = self.window.findChild(QLineEdit, 'epayActualEdit')
            # epay register input box
        self.epayRegisterEdit = self.window.findChild(QLineEdit, 'epayRegisterEdit')
            # scratchies actual input box
        self.scratchiesActualEdit = self.window.findChild(QLineEdit, 'scratchiesActualEdit')
            # scratchies register input box
        self.scratchiesRegisterEdit = self.window.findChild(QLineEdit, 'scratchiesRegisterEdit')
            # scratchie payouts actual input box
        self.scratchiesPayActualEdit = self.window.findChild(QLineEdit, 'scratchiesPayActualEdit')
            # scratchie payouts register input box
        self.scratchiesPayRegisterEdit = self.window.findChild(QLineEdit, 'scratchiesPayRegisterEdit')
            # lotto payouts actual input box
        self.lottoPayActualEdit = self.window.findChild(QLineEdit, 'lottoPayActualEdit')
            # lotto payouts register input box
        self.lottoPayRegisterEdit = self.window.findChild(QLineEdit, 'lottoPayRegisterEdit')
            # lotto actual edit
        self.lottoActualEdit = self.window.findChild(QLineEdit, 'lottoActualEdit')
            # lotto register edit
        self.lottoRegisterEdit = self.window.findChild(QLineEdit, 'lottoRegisterEdit')
            # notes text box
        self.notesEdit = self.window.findChild(QTextEdit, 'notesEdit')


        ## show the window
        self.window.show()

    ## method that's called when the date selection button is pressed
    def handle_dateSelectButton(self):
        ## method to handle the okay button when it is pressed
        def handle_okayButton():
            ## get date from calendar widget and create a string out of it
            q_date = calendar.selectedDate()

            if q_date.day() < 10:
                day = str(0) + str(q_date.day())
            else:
                day = str(q_date.day())

            if q_date.month() < 10:
                month = str(0) + str(q_date.month())
            else:
                month = str(q_date.month())

            year = str(q_date.year())

            date = day + '/' + month + '/' + year
            self.dateDisplay.setText(date)
            popup.accept()

        ## method to handle the cancel button when it is pressed
        def handle_cancelButton():
            popup.reject()

        ## initialise the dialog
        popup = QDialog()
        popup.setWindowTitle('Select Date')

        ## create the widgets and connect them to functions
        calendar = QCalendarWidget()
        okayButton = QPushButton('Okay')
        okayButton.clicked.connect(handle_okayButton)
        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(handle_cancelButton)

        ## initialise the layout manager
        layout = QVBoxLayout()

        ## add the widgets to the layout manager
        layout.addWidget(calendar)
        layout.addWidget(cancelButton)
        layout.addWidget(okayButton)
        popup.setLayout(layout)

        ## set the dialog as modal so that the user cannot interact with the main window when the dialog is open
        popup.setModal(True)

        popup.show()
        popup.exec_()   

    ## method that's called when the generate button is pressed
    def handle_generateButton(self):
        ## create a dictionary with inputted data
        data_dict = {
            'store': self.storeCombo.itemText(self.storeCombo.currentIndex()),
            'date': datetime.strptime(self.dateDisplay.text(), '%d/%m/%Y'),
            'staff': self.staffEdit.text(),
            'cash aside': self.cashAsideEdit.text(),
            'cash 100s': self.cash100Edit.text(),
            'cash 50s': self.cash50Edit.text(),
            'cash 20s': self.cash20Edit.text(),
            'cash 10s': self.cash10Edit.text(),
            'cash 5s': self.cash5Edit.text(),
            'cash coins': self.cashCoinsEdit.text(),
            'cash register': self.cashRegisterEdit.text(),
            'eftpos actual': self.eftActualEdit.text(),
            'eftpos register': self.eftRegisterEdit.text(),
            'epay actual': self.epayActualEdit.text(),
            'epay register': self.epayRegisterEdit.text(),
            'scratchies actual': self.scratchiesActualEdit.text(),
            'scratchies register': self.scratchiesRegisterEdit.text(),
            'scratchies pay actual': self.scratchiesPayActualEdit.text(),
            'scratchies pay register': self.scratchiesPayRegisterEdit.text(),
            'lotto pay actual': self.lottoPayActualEdit.text(),
            'lotto pay register': self.lottoPayRegisterEdit.text(),
            'lotto actual': self.lottoActualEdit.text(),
            'lotto register': self.lottoRegisterEdit.text(),
            'notes': self.notesEdit.toPlainText()
        }
            
        ## call the button handler and pass the dictionary to it
        Handlers.generateButton_handler(self, data_dict)

    ## method that's called when the print button is pressed
    def handle_printButton(self):
        Handlers.printButton_handler(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow('main_window.ui')
    sys.exit(app.exec_())