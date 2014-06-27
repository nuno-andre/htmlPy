class WebAppWindow:

    def __init__(self, title="Application", width=800, height=600, x_pos=10, y_pos=10, maximized=False, flash=False, developer_mode=False):
        """ Constructor for WebAppWindow class. Initialized the application

        Keyword arguments:
        title   -- Title of the window of the app. Default = "Application"
        width   -- Width of the window of the app in pixels. Default = 800
        height  -- height of the window of the app in pixels. Default = 600
        x_pos   -- X-coordinate of the top left corner of the window in pixels. Default = 10
        y_pos   -- Y-coordinate of the top left corner of the window in pixels. Default = 10
        maximized -- Boolean variable to initialize window as maximized. Default = False
        flash   -- Boolean variable to use flash plugin in the app. Default = False
        developer_mode -- Boolean variable to use developer tools in the app. Default = False
        """
        from PyQt4 import QtGui, QtWebKit, QtCore

        self.app = QtGui.QApplication([])
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

        self.developer_mode = developer_mode
        self.flash = flash

        # Initialize flash and developer mode
        web_app.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, flash)
        web_app.settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, developer_mode)
        web_app.settings().setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)

        self.web_app = web_app
        self.window = window
        self.link = None

    def set_url(self, link):
        """ Renders the HTML of the link in the application window

        Arguments:
        link -- The web link of the HTML to be rendered.
        """
        from PyQt4.QtCore import QUrl
        self.link = link
        self.web_app.load(QUrl(link))

    def get_url(self):
        """ Returns the link which is currently rendered in the application window."""
        return self.link

    def start(self, onstart_callback=None, onclose_callback=None):
        """ Starts the application window.

        Keyword arguments:
        onstart_callback -- Function to be called when application window is loaded. Default = None
        onstart_callback -- Function to be called when application window is closed. Default = None
        """
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
