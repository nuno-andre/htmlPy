class WebAppWindow:

    def __init__(self, title="Application", width=800, height=600, x_pos=10, y_pos=10, maximized=False):
        from PyQt4 import QtGui, QtWebKit, QtCore

        self.app = QtGui.QApplication([])
        # self.window = QtGui.QMainWindow()
        web_app = QtWebKit.QWebView()

        window = QtGui.QMainWindow()
        window.setCentralWidget(web_app)

        window.setWindowTitle(title)

        if maximized:
            self.width = -1
            self.height = -1
            self.x_pos = -1
            self.y_pos = -1
            self.maximized = True
        else:
            self.maximized = False
            self.width = int(width)
            self.height = int(height)
            self.x_pos = int(x_pos)
            self.y_pos = int(y_pos)

        self.web_app = web_app
        self.window = window

    def set_url(self, link):
        from PyQt4.QtCore import QUrl
        self.web_app.load(QUrl(link))

    def start(self, onstart_callback=None, onclose_callback=None):
        import sys
        
        if self.maximized:
            self.window.showMaximized()
        else:
            self.window.resize(self.width, self.height)
            self.window.move(self.x_pos, self.y_pos)
            self.window.show()

        if onstart_callback is not None:
            onstart_callback()

        if onclose_callback is None:
            sys.exit(self.app.exec_())
        else:
            def close_function(callback, app, sys):
                callback()
                sys.exit(app.exec_())

            close_function(onclose_callback, self.app, sys)
