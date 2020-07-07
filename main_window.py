import sys
import os
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QDialog, QPushButton, QLineEdit, QComboBox, QToolButton, QTextEdit, QCalendarWidget, QVBoxLayout, QGridLayout, QLabel, QFileDialog
from PySide2.QtCore import QFile, QObject, Qt, QPoint, QRect
from PySide2.QtGui import QImage, QPainter
from PySide2.QtPrintSupport import QPrintDialog, QPrinter
from datetime import datetime
# from tr import tr
from pdf2image import convert_from_path
from PIL import Image

from event_handlers import Handlers
from helpers import Helpers as H

# import popplerqt5


class MainWindow(QObject):
    global global_dict
    global_dict = {
        'eftpos 1': '',
        'eftpos 2': '',
        'eftpos 3': '',
        'eftpos prev': '',
        'instants cash': '',
        'free instants': '',
        'total prizes': '',
        'gross sales': '',
        'instants comm': '',
        'instants net': ''
    }

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
        self.dateSelectButton = self.window.findChild(QToolButton, 'dateSelectButton')
        self.dateSelectButton.setArrowType(Qt.DownArrow)
        self.dateSelectButton.clicked.connect(self.handle_dateSelectButton)

            # eft input button
        self.eftEnterButton = self.window.findChild(QPushButton, 'eftEnterButton')
        self.eftEnterButton.clicked.connect(self.handle_eftEnterButton)

            # scratchie payouts input button
        self.scratchiesPayEnterButton = self.window.findChild(QPushButton, 'scratchiesPayEnterButton')
        self.scratchiesPayEnterButton.clicked.connect(self.handle_scratchiesPayEnterButton)

            # lotto payouts input button
        self.lottoPayEnterButton = self.window.findChild(QPushButton, 'lottoPayEnterButton')
        self.lottoPayEnterButton.clicked.connect(self.handle_lottoPayEnterButton)

            # lotto input button
        self.lottoEnterButton = self.window.findChild(QPushButton, 'lottoEnterButton')
        self.lottoEnterButton.clicked.connect(self.handle_lottoEnterButton)

            # generate button
        self.generateButton = self.window.findChild(QPushButton, 'generateButton')
        self.generateButton.clicked.connect(self.handle_generateButton)

            # print button
        self.printButton = self.window.findChild(QPushButton, 'printButton')
        self.printButton.clicked.connect(self.handle_printButton)

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
            # scratchie payouts register input box
        self.scratchiesPayRegisterEdit = self.window.findChild(QLineEdit, 'scratchiesPayRegisterEdit')
            # lotto payouts register input box
        self.lottoPayRegisterEdit = self.window.findChild(QLineEdit, 'lottoPayRegisterEdit')
            # lotto register edit
        self.lottoRegisterEdit = self.window.findChild(QLineEdit, 'lottoRegisterEdit')
            # notes text box
        self.notesEdit = self.window.findChild(QTextEdit, 'notesEdit')


        ## show the window
        self.window.show()
    
    def handle_eftEnterButton(self):
        ## method to handle the okay button when it is pressed
        def handle_okayButton():
            machine_1_value = H.char_remover(self, machine_1.text())
            machine_2_value = H.char_remover(self, machine_2.text())
            machine_3_value = H.char_remover(self, machine_3.text())
            machine_prev_value = H.char_remover(self, machine_prev.text())

            global_dict['eftpos 1'] = H.dollar_adder(self, machine_1_value)
            global_dict['eftpos 2'] = H.dollar_adder(self, machine_2_value)
            global_dict['eftpos 3'] = H.dollar_adder(self, machine_3_value)
            global_dict['eftpos prev'] = H.dollar_adder(self, machine_prev_value)

            eft_arr = [machine_1_value, machine_2_value, machine_3_value]

            eft_total = 0
            for value in eft_arr:
                if value != None:
                    eft_total += value

            if machine_prev_value != None:
                eft_total -= machine_prev_value

            ftd_eft_total = H.dollar_adder(self, eft_total)

            if ftd_eft_total == '-':
                self.eftEnterButton.setText('Enter Values')
            else:
                self.eftEnterButton.setText(ftd_eft_total)

            popup.accept()
            
        
        ## method to handle the cancel button when it is pressed
        def handle_cancelButton():
            popup.reject()

        
        ## initialise the dialog
        popup = QDialog()
        popup.setWindowTitle('Enter Eftpos Machine Values')

        ## create the widgets and connect them to functions
        machine_1_label = QLabel()
        machine_1_label.setText('Eftpos Machine 1')
        machine_1 = QLineEdit()
        machine_2_label = QLabel()
        machine_2_label.setText('Eftpos Machine 2')
        machine_2 = QLineEdit()
        machine_3_label = QLabel()
        machine_3_label.setText('Eftpos Machine 3')
        machine_3 = QLineEdit()
        machine_prev_label = QLabel()
        machine_prev_label.setText('Previous Day\'s Eftpos (if applicable)')
        machine_prev = QLineEdit()

        okayButton = QPushButton('Okay')
        okayButton.clicked.connect(handle_okayButton)
        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(handle_cancelButton)

        ## initialise values
        machine_1.setText(global_dict['eftpos 1'])
        machine_2.setText(global_dict['eftpos 2'])
        machine_3.setText(global_dict['eftpos 3'])
        machine_prev.setText(global_dict['eftpos prev'])

        ## initialise the layout manager
        layout = QGridLayout()

        ## add the widgets to the layout manager
        layout.addWidget(machine_1_label, 0, 0)
        layout.addWidget(machine_1, 0, 1)
        layout.addWidget(machine_2_label, 1, 0)        
        layout.addWidget(machine_2, 1, 1)
        layout.addWidget(machine_3_label, 2, 0)
        layout.addWidget(machine_3, 2, 1)
        layout.addWidget(machine_prev_label, 3, 0)        
        layout.addWidget(machine_prev, 3, 1)
        layout.addWidget(cancelButton, 4, 0, 1, 2)
        layout.addWidget(okayButton, 5, 0, 1, 2)
        popup.setLayout(layout)

        ## set the dialog as modal so that the user cannot interact with the main window when the dialog is open
        popup.setModal(True)

        popup.show()
        popup.exec_()   


    def handle_scratchiesPayEnterButton(self):
        ## method to handle the okay button when it is pressed
        def handle_okayButton():
            instants_cash_value = H.char_remover(self, instants_cash.text())
            free_instants_value = H.char_remover(self, free_instants.text())

            global_dict['instants cash'] = H.dollar_adder(self, instants_cash_value)
            global_dict['free instants'] = H.dollar_adder(self, free_instants_value)

            scratchies_pay_arr = [instants_cash_value, free_instants_value]

            scratchies_pay_total = 0
            for value in scratchies_pay_arr:
                if value != None:
                    scratchies_pay_total += value

            ftd_scratchies_pay_total = H.dollar_adder(self, scratchies_pay_total)

            if ftd_scratchies_pay_total == '-':
                self.scratchiesPayEnterButton.setText('Enter Values')
            else:
                self.scratchiesPayEnterButton.setText(ftd_scratchies_pay_total)

            popup.accept()
            
        
        ## method to handle the cancel button when it is pressed
        def handle_cancelButton():
            popup.reject()

        ## initialise the dialog
        popup = QDialog()
        popup.setWindowTitle('Enter Scratchies Payout Values')

        ## create the widgets and connect them to functions
        instants_cash_label = QLabel()
        instants_cash_label.setText('Instants Cash')
        instants_cash = QLineEdit()
        free_instants_label = QLabel()
        free_instants_label.setText('Free Instants')
        free_instants = QLineEdit()

        okayButton = QPushButton('Okay')
        okayButton.clicked.connect(handle_okayButton)
        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(handle_cancelButton)

        ## initialise values
        instants_cash.setText(global_dict['instants cash'])
        free_instants.setText(global_dict['free instants'])

        ## initialise the layout manager
        layout = QGridLayout()

        ## add the widgets to the layout manager
        layout.addWidget(instants_cash_label, 0, 0)
        layout.addWidget(instants_cash, 0, 1)
        layout.addWidget(free_instants_label, 1, 0)        
        layout.addWidget(free_instants, 1, 1)
        layout.addWidget(cancelButton, 2, 0, 1, 2)
        layout.addWidget(okayButton, 3, 0, 1, 2)
        popup.setLayout(layout)

        ## set the dialog as modal so that the user cannot interact with the main window when the dialog is open
        popup.setModal(True)

        popup.show()
        popup.exec_()   


    def handle_lottoPayEnterButton(self):
         ## method to handle the okay button when it is pressed
        def handle_okayButton():
            instants_cash_value = H.char_remover(self, instants_cash.text())
            prizes_paid_value = H.char_remover(self, prizes_paid.text())

            global_dict['instants cash'] = H.dollar_adder(self, instants_cash_value)
            global_dict['total prizes'] = H.dollar_adder(self, prizes_paid_value)

            if (prizes_paid_value and instants_cash_value) != None:
                lotto_pay_total = prizes_paid_value - instants_cash_value

                ftd_lotto_pay_total = H.dollar_adder(self, lotto_pay_total)

                if ftd_lotto_pay_total == '-':
                    self.lottoPayEnterButton.setText('Enter Values')
                else:
                    self.lottoPayEnterButton.setText(ftd_lotto_pay_total)

                popup.accept()
            else:
                self.lottoPayEnterButton.setText('Enter Values')
                popup.reject()
            
        
        ## method to handle the cancel button when it is pressed
        def handle_cancelButton():
            popup.reject()

        ## initialise the dialog
        popup = QDialog()
        popup.setWindowTitle('Enter Lotto Payout Values')

        ## create the widgets and connect them to functions
        instants_cash_label = QLabel()
        instants_cash_label.setText('Instants Cash')
        instants_cash = QLineEdit()
        prizes_paid_label = QLabel()
        prizes_paid_label.setText('Total Prizes Paid')
        prizes_paid = QLineEdit()

        okayButton = QPushButton('Okay')
        okayButton.clicked.connect(handle_okayButton)
        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(handle_cancelButton)

        ## initialise values
        instants_cash.setText(global_dict['instants cash'])
        prizes_paid.setText(global_dict['total prizes'])

        ## initialise the layout manager
        layout = QGridLayout()

        ## add the widgets to the layout manager
        layout.addWidget(prizes_paid_label, 0, 0)        
        layout.addWidget(prizes_paid, 0, 1)
        layout.addWidget(instants_cash_label, 1, 0)
        layout.addWidget(instants_cash, 1, 1)
    

        layout.addWidget(cancelButton, 2, 0, 1, 2)
        layout.addWidget(okayButton, 3, 0, 1, 2)
        popup.setLayout(layout)

        ## set the dialog as modal so that the user cannot interact with the main window when the dialog is open
        popup.setModal(True)

        popup.show()
        popup.exec_()     


    def handle_lottoEnterButton(self):
         ## method to handle the okay button when it is pressed
        def handle_okayButton():
            gross_sales_value = H.char_remover(self, gross_sales.text())
            instants_comm_value = H.char_remover(self, instants_comm.text())
            instants_net_value = H.char_remover(self, instants_net.text())

            global_dict['gross sales'] = H.dollar_adder(self, gross_sales_value)
            global_dict['instants comm'] = H.dollar_adder(self, instants_comm_value)
            global_dict['instants net'] = H.dollar_adder(self, instants_net_value)

            if (gross_sales_value and instants_comm_value and instants_net_value) != None:
                lotto_total = gross_sales_value - instants_comm_value - instants_net_value

                ftd_lotto_total = H.dollar_adder(self, lotto_total)

                if ftd_lotto_total == '-':
                    self.lottoEnterButton.setText('Enter Values')
                else:
                    self.lottoEnterButton.setText(ftd_lotto_total)

                popup.accept()
            else:
                self.lottoEnterButton.setText('Enter Values')
                popup.reject()
            
        
        ## method to handle the cancel button when it is pressed
        def handle_cancelButton():
            popup.reject()

        ## initialise the dialog
        popup = QDialog()
        popup.setWindowTitle('Enter Lotto Values')

        ## create the widgets and connect them to functions
        gross_sales_label = QLabel()
        gross_sales_label.setText('Gross Sales')
        gross_sales = QLineEdit()
        instants_comm_label = QLabel()
        instants_comm_label.setText('Instants Commission')
        instants_comm = QLineEdit()
        instants_net_label = QLabel()
        instants_net_label.setText('Instants Net')
        instants_net = QLineEdit()

        okayButton = QPushButton('Okay')
        okayButton.clicked.connect(handle_okayButton)
        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(handle_cancelButton)

        ## initialise values
        gross_sales.setText(global_dict['gross sales'])
        instants_comm.setText(global_dict['instants comm'])
        instants_net.setText(global_dict['instants net'])

        ## initialise the layout manager
        layout = QGridLayout()

        ## add the widgets to the layout manager
        layout.addWidget(gross_sales_label, 0, 0)
        layout.addWidget(gross_sales, 0, 1)
        layout.addWidget(instants_comm_label, 1, 0)        
        layout.addWidget(instants_comm, 1, 1)
        layout.addWidget(instants_net_label, 2, 0)        
        layout.addWidget(instants_net, 2, 1)
        
    

        layout.addWidget(cancelButton, 3, 0, 1, 2)
        layout.addWidget(okayButton, 4, 0, 1, 2)
        popup.setLayout(layout)

        ## set the dialog as modal so that the user cannot interact with the main window when the dialog is open
        popup.setModal(True)

        popup.show()
        popup.exec_()

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
            'eftpos actual': self.eftEnterButton.text(),
            'eftpos register': self.eftRegisterEdit.text(),
            'epay actual': self.epayActualEdit.text(),
            'epay register': self.epayRegisterEdit.text(),
            'scratchies actual': self.scratchiesActualEdit.text(),
            'scratchies register': self.scratchiesRegisterEdit.text(),
            'scratchies pay actual': self.scratchiesPayEnterButton.text(),
            'scratchies pay register': self.scratchiesPayRegisterEdit.text(),
            'lotto pay actual': self.lottoPayEnterButton.text(),
            'lotto pay register': self.lottoPayRegisterEdit.text(),
            'lotto actual': self.lottoEnterButton.text(),
            'lotto register': self.lottoRegisterEdit.text(),
            'notes': self.notesEdit.toPlainText()
        }

        ## bring up save dialog
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setViewMode(QFileDialog.Detail)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilter('Portable Document Format (*.pdf)')

        if dialog.exec_():
            file_path = dialog.selectedFiles()
            
        ## call the button handler and pass the dictionary to it
        Handlers.generateButton_handler(self, data_dict, file_path[0])

    ## method that's called when the print button is pressed
    def handle_printButton(self):
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
            'eftpos actual': self.eftEnterButton.text(),
            'eftpos register': self.eftRegisterEdit.text(),
            'epay actual': self.epayActualEdit.text(),
            'epay register': self.epayRegisterEdit.text(),
            'scratchies actual': self.scratchiesActualEdit.text(),
            'scratchies register': self.scratchiesRegisterEdit.text(),
            'scratchies pay actual': self.scratchiesPayEnterButton.text(),
            'scratchies pay register': self.scratchiesPayRegisterEdit.text(),
            'lotto pay actual': self.lottoPayEnterButton.text(),
            'lotto pay register': self.lottoPayRegisterEdit.text(),
            'lotto actual': self.lottoEnterButton.text(),
            'lotto register': self.lottoRegisterEdit.text(),
            'notes': self.notesEdit.toPlainText()
        }

        save_path = 'eod_final_toprint.pdf'
        image_path = 'eod_final_toprint.jpg'
        work_path = os.getcwd()
        # print(work_path)

        Handlers.generateButton_handler(self, data_dict, save_path)

        # printer = QPrinter(QPrinter.HighResolution)
        printer = QPrinter()
        printer.setResolution(200)
        printer.setPaperSize(QPrinter.A4)
        printer.setFullPage(True)

        print('Resultion: ', printer.resolution)

        # print('Screen resolution: ', QPrinter.ScreenResolution)
        # print('High resolution: ', QPrinter.HighResolution)

        dialog = QPrintDialog(printer)

        if dialog.exec_() == QPrintDialog.Accepted:
            image = convert_from_path(work_path + '/' + save_path)
            image[0].save(image_path)
            qimage = QImage(work_path + '/' + image_path, 'jpg')

            painter = QPainter()
            painter.begin(printer)

            image_rect = QRect(qimage.rect())
            paint_rect = QRect(0, 0, painter.device().width(), painter.device().height())

            image_rect.moveCenter(paint_rect.center())

            # painter.drawImage(0, 0, qimage, sw=1, sh=1)
            painter.drawImage(paint_rect.topLeft(), qimage)
            painter.end()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window_ui = H.resource_locator(__name__, 'main_window.ui')
    print(window_ui)
    form = MainWindow(window_ui)
    sys.exit(app.exec_())