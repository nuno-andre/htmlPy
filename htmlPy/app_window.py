class AppWindow:
    
    def __init__(self, title="Application", width=800, height=600, x_pos=10, y_pos=10, maximized=False):
        from PyQt4 import QtGui, QtWebKit

        self.app = QtGui.QApplication([])
        # self.window = QtGui.QMainWindow()
        web_app = QtWebKit.QWebView()
        web_app.setWindowTitle(title)

        if maximized:
            web_app.showMaximized()
        else:
            web_app.resize(int(width), int(height))
            web_app.move(int(x_pos), int(y_pos))
        self.web_app = web_app

        from PyQt4 import QtCore

        class connecter(QtCore.QObject):
            @QtCore.pyqtSlot()

            def __init__(self):
                pass

        self.connecter = connecter()

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

    def setHTML(self, html, onset_callback=None):
        from PyQt4.QtCore import QString

        self.web_app.setHtml(QString(html))
        self.web_app.show()
        if onset_callback is not None:
            onset_callback()

    def setTemplate(self, filename, context, onset_callback=None):
        from django import template

        f = open(filename, "r")

        t = template.Template(f.read())
        c = template.Context(context)
        self.setHTML(t.render(c), onset_callback=onset_callback)

    def __add_module_to_connecter(self, f):
        import types
        mod = __import__(f)

        for k, v in mod.__dict__.iteritems():
            if type(v) is types.MethodType or type(v) is types.FunctionType or type(v) is types.BuiltinFunctionType:
                self.connecter.__dict__[f.replace(".", "_") + "_" + k] = v
            elif type(v) is types.InstanceType or type(v) is types.ModuleType:
                self.__add_module_to_connecter(f + "." + k)

    def __add_functions_to_connecter(self, functions):
        import types
                
        for f in functions:
            mod = __import__(f)

            if type(mod) is types.MethodType or type(mod) is types.FunctionType or type(mod) is types.BuiltinFunctionType:
                self.connecter.__dict__[f.replace(".", "_")] = mod
            elif type(mod) is types.InstanceType or type(mod) is types.ModuleType:
                self.__add_module_to_connector(f)

    def register(self, arg, *args):
        if type(arg) is str:
            arg = [arg]

        functions = arg + args
        self.__add_functions_to_connecter(functions)

        self.web_app.page().mainFrame().addToJavaScriptWindowObject("python", self.connecter)
