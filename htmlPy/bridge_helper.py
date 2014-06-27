from htmlPy import Bridge, attach
from PyQt4 import QtGui
from PyQt4.QtCore import QString

class BridgeHelper(Bridge):
    """ A helpers class for added some functionalities in HTML and Javascript
    """

    @attach(str)
    def alert(self, text):
        """ Print some text to python console from javascript.

        Arguments:
        text -- The text to be printed.
        """
        print text

    @attach(str, result=str)
    def file_dialog(self, filter=""):
        """ A helper for creating file input in HTML.

        Keyword arguments:
        filter -- A string which defines file extension filter for the file dialog. The filter can be a string of format
        "All files (*.*);;JPEG (*.jpg *.jpeg);;TIFF (*.tif)"
         Default = "" (All files)
        """
        win = QtGui.QMainWindow()
        return QtGui.QFileDialog.getOpenFileName(win, 'Open file', ".", QString(filter))


bridge_helper = BridgeHelper()
