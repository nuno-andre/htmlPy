class AppWindow:
    
    def __init__(self, title="Application", width=800, height=600, x_pos=10, y_pos=10, maximized=False, flash=False, developer_mode=False):
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

        self.developer_mode = developer_mode
        self.flash = flash

        web_app.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, flash)
        web_app.settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, developer_mode)
        web_app.settings().setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)
        self.web_app = web_app
        self.window = window

        self.bridges = []

        from bridge_helper import bridge_helper
        self.register(bridge_helper)

        self.asset_path = "./"
        self.template_path = "./"


    def setAssetPath(self, absolute_file_path):
        self.asset_path = absolute_file_path

    def setTemplatePath(self, absolute_file_path):
        self.template_path = absolute_file_path

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

    def __addAssetLink__(self, html):
        if "$asset$" not in html:
            return html

        fragments = html.split("$asset$", 1)
        fragments = [fragments[0]] + fragments[1].split("$endasset$", 1)
        fragments[1] = "file:///" + self.asset_path + fragments[1].strip()

        return self.__addAssetLink__("".join(fragments))

    def setHTML(self, html, onset_callback=None):
        from PyQt4.QtCore import QString
        script = """var anchors=document.getElementsByTagName("a");var forms=document.getElementsByTagName("form");var stripslashes=function(e){if(e.substr(-1)==="/"){return stripslashes(e.substr(0,e.length-1))}if(e.substr(0,1)==="/"){return stripslashes(e.substr(1,e.length))}return e};var link_catch=function(e){e.preventDefault();var elem=e.target||e.srcElement;var call=elem.getAttribute("data-href");if(call===null)return;var params=elem.getAttribute("data-params");params=params!==null?params:"";call=stripslashes(call);var exec=call.replace("/",".");eval(exec+"('"+params+"')")};var form_catch=function(e){e.preventDefault();var elem=e.target||e.srcElement;var action=elem.getAttribute("data-action");if(action===null)return;window.formdata={};for(var i=0,ii=elem.length;i<ii;++i){var input=elem[i];if(input.name){window.formdata[input.name]=input.value;if(input.type==="file"){}}}action=stripslashes(action);var params=elem.getAttribute("data-params");var exec=action.replace("/",".");exec=exec+"('"+JSON.stringify(window.formdata);exec=params!==null?exec+"', '"+params+"')":exec+"')";eval(exec)};var file_dialog=function(e){e.preventDefault();var t=e.target.getAttribute("data-display");var n=e.target.getAttribute("data-filter");n=n!==null&&n!=="null"?n:"Any file (*.*)";var r=BridgeHelper.file_dialog(n);document.getElementById(t).value=r;return false};for(var i=anchors.length-1;i>=0;i--){anchors[i].onclick=link_catch}for(var fi=forms.length-1;fi>=0;fi--){forms[fi].onsubmit=form_catch;elem=forms[fi];for(var i=0,ii=elem.length;i<ii;++i){var input=elem[i];if(input.type==="file"){var fileboxname=input.getAttribute("name");var filter=input.getAttribute("data-filter");var disabledInput=document.createElement("input");disabledInput.setAttribute("disabled","disabled");disabledInput.setAttribute("name",fileboxname);disabledInput.setAttribute("id",fileboxname+"_path");input.parentNode.insertBefore(disabledInput,input.nextSibling);var button=document.createElement("button");button.innerHTML="Choose file";button.setAttribute("data-display",fileboxname+"_path");button.setAttribute("data-filter",filter);button.onclick=file_dialog;input.parentNode.insertBefore(button,disabledInput.nextSibling);input.style.display="none";elem[i].remove()}}}"""
        
        if not self.developer_mode:
            script = script + ";document.oncontextmenu=function(){return false;};"

        modified_html = html.replace("</body>", "<script>" + script + "</script></body>")

        self.web_app.setHtml(QString(self.__addAssetLink__(modified_html)))

        for c in self.bridges:
            self.register(c)
        
        self.web_app.show()
        if onset_callback is not None:
            onset_callback()

    def setTemplate(self, filename, context={}, onset_callback=None):
        import jinja2

        template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.template_path))
        t = template_env.get_template(filename)

        self.setHTML(t.render(**context), onset_callback=onset_callback)

    def register(self, class_instance):
        self.web_app.page().mainFrame().addToJavaScriptWindowObject(class_instance.__class__.__name__, class_instance)

        if class_instance not in self.bridges:
            self.bridges.append(class_instance)
