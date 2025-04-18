import sys
from PyQt5 import QtWidgets
from gui.integration_window import IntegrationWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = IntegrationWindow()
    win.show()
    sys.exit(app.exec_())
