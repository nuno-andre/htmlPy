from htmlPy import Bridge, attach
from PyQt4 import QtGui
from PyQt4.QtCore import QString

class BridgeHelper(Bridge):

    @attach(str)
    def alert(self, text):
        print text


    @attach(str, result=str)
    def file_dialog(self, filter=""):
        win = QtGui.QMainWindow()
        return QtGui.QFileDialog.getOpenFileName(win, 'Open file', ".", QString(filter))


bridge_helper = BridgeHelper()