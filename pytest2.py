import sys, os
sys.path.append(os.pardir)
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from PyQt5.QtWidgets import QMainWindow, QApplication
from tc_lib.common import *
from tc_lib.BTCclass import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()