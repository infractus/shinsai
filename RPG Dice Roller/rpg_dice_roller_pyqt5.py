import sys, random
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

class MainWindow(qtw.QWidget):
    def __init__(self):
        """MainWindow constructor."""
        super().__init__()
        self.setWindowTitle("Shinsai's RPG Dice Roller")
        self.resize(750, 150)
        # Main UI code goes here
        main_layout = qtw.QVBoxLayout()
        self.setLayout(main_layout)
        self.text_box = qtw.QLineEdit(
            self, readOnly=True,
            placeholderText="Welcome to Shinsai's Dice Roller!"
        )
        self.result_box = qtw.QLineEdit(
            self, readOnly=True,
            placeholderText="Select the number of dice to roll, which dice to "
            "roll, and the modifier."
        )
        main_layout.addWidget(self.text_box)
        main_layout.addWidget(self.result_box)

        grid_layout = qtw.QGridLayout()
        main_layout.addLayout(grid_layout)

        self.num_roll_label = qtw.QLabel('# of dice to roll:', self)
        self.num_roll = qtw.QSpinBox(self, value=1, minimum=1, maximum=50)
        self.d_roll_label = qtw.QLabel('Dice to Roll:', self)
        self.d_list = qtw.QComboBox(self)
        self.d_list.addItems(['d4', 'd6', 'd8', 'd10', 'd12', 'd20', 'd100'])
        self.mod_label = qtw.QLabel('Modifier:', self)
        self.plus_mod = qtw.QRadioButton('+', self, checkable=True)
        self.minus_mod = qtw.QRadioButton('-', self, checkable=True)
        self.num_mod = qtw.QSpinBox(self, value=0, minimum=0, maximum=50)
        self.roll_btn = qtw.QPushButton(
            'Roll the dice!', self, shortcut=qtg.QKeySequence("Space"),
            clicked=self.display_results
        )

        grid_layout.addWidget(self.num_roll_label, 0, 0, 1, 1)
        grid_layout.addWidget(self.num_roll, 0, 2, 1, 1)
        grid_layout.addWidget(self.d_roll_label, 0, 5, 1, 1)
        grid_layout.addWidget(self.d_list, 0, 7, 1, 1)
        grid_layout.addWidget(self.mod_label, 0, 9, 1, 1)
        grid_layout.addWidget(self.plus_mod, 0, 11, 1, 1)
        grid_layout.addWidget(self.minus_mod, 0, 10, 1, 1)
        grid_layout.addWidget(self.num_mod, 0, 12 , 1, 1)
        grid_layout.addWidget(self.roll_btn, 2, 0, 2, 14)

        self.num_dice, self.dice_val = 1, "d4"
        self.mod_type, self.mod_val = "+", 0
        self.num_roll.valueChanged.connect(self.set_num_dice)
        self.d_list.currentTextChanged.connect(self.set_dice_val)
        self.num_mod.valueChanged.connect(self.set_mod_val)

        # End main UI code
        self.show()

    @qtc.pyqtSlot(int)
    def set_num_dice(self, value):
        self.num_dice = value
        self.update_textbox()

    @qtc.pyqtSlot(str)
    def set_dice_val(self, value):
        self.dice_val = value
        self.update_textbox()

    @qtc.pyqtSlot(int)
    def set_mod_val(self, value):
        self.mod_val = value
        self.update_textbox()

    def update_textbox(self):
        if self.plus_mod.isChecked():
            self.mod_type = '+'
        elif self.minus_mod.isChecked():
            self.mod_type = '-'
        self.text_box.setText(
            f"{self.num_dice}d{self.dice_val[1:]}{self.mod_type}{self.mod_val}"
        )

    @qtc.pyqtSlot(bool)
    def display_results(self):
        subtotal = 0
        results = []
        for i in range(self.num_dice):
            result = random.randint(1, int(self.dice_val[1:]))
            result = int(result)
            results.append(result)
            subtotal = result + subtotal
        if self.mod_type == '-':
            resultmod = subtotal - self.mod_val
        else:
            resultmod = subtotal + self.mod_val
        self.result_box.setText(
            f'Rolled {self.num_dice}d{self.dice_val[1:]}{self.mod_type}'
            f'{self.mod_val} | Rolled natural {subtotal}: {results} | Final '
            f'result: {resultmod}'
        )

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())