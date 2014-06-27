import jinja2, os

class AppWindow:

    def __init__(self, title="Application", width=800, height=600, x_pos=10, y_pos=10, maximized=False, flash=False, developer_mode=False):
        """ Constructor for AppWindow class. Initialized the application.

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

        web_app.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, flash)
        web_app.settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, developer_mode)
        web_app.settings().setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)
        self.web_app = web_app
        self.window = window

        from bridge_helper import bridge_helper
        self.bridges = []
        self.register(bridge_helper)

        self.asset_path = "./"
        self.template_path = "./"
        self.__template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.template_path))

        with open(os.path.join(os.path.abspath(os.path.dirname(__file__))), "bridge_helper.min.js") as f:
            self.script = f.read().strip()

        if not self.developer_mode:
            self.script = self.script + ";document.oncontextmenu=function(){return false;};"
        self.template = None


    def set_asset_path(self, absolute_file_path):
        """ Sets directory for loading assets (CSS, JS, Images etc.) with relative path.

        Arguments:
        absolute_file_path -- Absolute path to the directory containing all assets.
        """
        self.asset_path = absolute_file_path

    def set_template_path(self, absolute_file_path):
        """ Sets directory for loading templates with relative path using Jinja.

        Arguments:
        absolute_file_path -- Absolute path to the directory containing all templates.
        """
        self.template_path = absolute_file_path
        self.__template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.template_path))

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

    def __add_asset_link__(self, html):
        """ Processes HTML to change htmlPy asset tags to filepath URLs. Not to be called directly.
        In HTML, htmlPy asset tags will be like
        $asset$ css/bootstrap.css $endasset$

        Arguments:
        html -- The HTML to be processed.
        """
        if "$asset$" not in html:
            return html

        fragments = html.split("$asset$", 1)
        fragments = [fragments[0]] + fragments[1].split("$endasset$", 1)
        fragments[1] = "file:///" + self.asset_path + fragments[1].strip()

        return self.__addAssetLink__("".join(fragments))

    def set_html(self, html, onset_callback=None):
        """ Processes and sets HTML in application window.
        This function does asset tags processing, adds bridge helper scripts, adds previously added bridges

        Arguments:
        html -- The HTML to be processed and set.

        Keyword arguments:
        onset_callback -- The function to be called after setting HTML. Default = None
        """
        from PyQt4.QtCore import QString

        modified_html = html.replace("</body>", "<script>" + self.script + "</script></body>")

        self.web_app.setHtml(QString(self.__addAssetLink__(modified_html)))

        for c in self.bridges:
            self.register(c)

        self.web_app.show()
        if onset_callback is not None:
            onset_callback()

    def get_html(self):
        """ Returns the processed HTML set in current window. """
        frame = self.web_app.page().mainFrame()
        return unicode(frame.toHtml()).encode('utf-8')

    def set_template(self, template_relative_path, context={}, onset_callback=None):
        """ Sets HTML template to the window after parsing it with Jinja and htmlPy processers.

        Arguments:
        template_relative_path -- The path to the Jinja template file relative to the base template path.

        Keyword arguments:
        context -- The dictionary to be used as context while rendering Jinja template. Default = {}
        onset_callback -- The function to be called after setting HTML. Default = None
        """
        html = self.render_template(template_relative_path, context)
        self.set_html(html, onset_callback=onset_callback)
        self.template = template_relative_path

    def get_template(self):
        """ Returns the path of the Jinja template file relative the to base tempalte path. """
        return self.template

    def render_template(self, template_relative_path, context={}):
        """ Returns parsed HTML of the Jinja HTML template after parsing it with Jinja parser.

        Arguments:
        template_relative_path -- The path to the Jinja template file relative to the base template path.

        Keyword arguments:
        context -- The dictionary to be used as context while rendering Jinja template. Default = {}
        """
        t = self.__template_env.get_template(template_relative_path)
        return t.render(**context)

    def register(self, class_instance):
        """ Adds a class instance to the application bridge for calling from javascript.

        Arguments:
        class_instance -- Instance of a class which inherits htmlPy.Bridge
        """
        self.web_app.page().mainFrame().addToJavaScriptWindowObject(class_instance.__class__.__name__, class_instance)

        if class_instance not in self.bridges:
            self.bridges.append(class_instance)

    def execute_javascript(self, JS):
        """ Execute javascript in current window.

        Arguments:
        JS -- The javascript to be executed as string.
        """
        self.web_app.page().mainFrame().evaluateJavaScript(JS)
