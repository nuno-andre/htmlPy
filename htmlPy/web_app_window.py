class WebAppWindow:

    def __init__(self, title="Application", width=800, height=600, x_pos=10, y_pos=10, maximized=False):
        from PyQt4 import QtGui, QtWebKit

        self.app = QtGui.QApplication([])
        # self.window = QtGui.QMainWindow()
        web_app = QtWebKit.QWebView()
        web_app.windowTitle = title

        if maximized:
            web_app.showMaximized()
        else:
            web_app.resize(int(width), int(height))
            web_app.move(int(x_pos), int(y_pos))
        self.web_app = web_app

    def set_url(self, link):
        from PyQt4.QtCore import QUrl
        self.web_app.load(QUrl(link))

    def start(self, onstart_callback=None, onclose_callback=None):
        import sys
        self.web_app.show()
        if onstart_callback is not None:
            onstart_callback()

        if onclose_callback is None:
            sys.exit(self.app.exec_())
        else:
            def close_function(callback, app, sys):
                callback()
                sys.exit(app.exec_())

            close_function(onclose_callback, self.app, sys)
