import unittest
import htmlPy
import general_test

class TestAppWindow(unittest.TestCase, general_test.GeneralTest):

    def setUp(self):
        self.app = htmlPy.AppWindow(title="Test", width=40, height=80, x_pos=10, y_pos=20)
        self.max_app = htmlPy.AppWindow(title="Test maximized", maximized=True)
        self.flash_app = htmlPy.AppWindow(flash=True)
        self.dev_app = htmlPy.AppWindow(developer_mode=True)
        self.test_html = "<html><head></head><body></body></html>"
        self.test_javascript = "document.write('Written from python');"

    def test_flash_enable(self):
        # QtWebKit.QWebSettings.PluginsEnabled == 3
        # http://qt-project.org/doc/qt-4.8/qwebsettings.html
        flag = 3
        assert self.flash_app.web_app.settings().testAttribute(flag) == True

    def test_flash_disable(self):
        # QtWebKit.QWebSettings.PluginsEnabled == 3
        # http://qt-project.org/doc/qt-4.8/qwebsettings.html
        flag = 3
        assert self.app.web_app.settings().testAttribute(flag) == False

    def test_dev_enable(self):
        # QtWebKit.QWebSettings.DeveloperExtrasEnabled == 7
        # http://qt-project.org/doc/qt-4.8/qwebsettings.html
        flag = 7
        assert self.dev_app.web_app.settings().testAttribute(flag) == True

    def test_dev_disable(self):
        # QtWebKit.QWebSettings.DeveloperExtrasEnabled == 7
        # http://qt-project.org/doc/qt-4.8/qwebsettings.html
        flag = 7
        assert self.app.web_app.settings().testAttribute(flag) == False

    def test_dev_enabled_context_free(self):
        self.dev_app.set_html(self.test_html)
        assert "document.oncontextmenu=function(){return false;}" not in self.dev_app.get_html()

    def test_dev_disabled_context_blocked(self):
        self.app.set_html(self.test_html)
        assert "document.oncontextmenu=function(){return false;}" in self.app.get_html()

    def test_script_inclusion(self):
        self.app.set_html(self.test_html)
        assert "<script>/* Compressed using http://jscompress.com/ */" in self.app.get_html()

    def test_execute_javascript(self):
        self.app.set_html(self.test_html)
        self.app.execute_javascript(self.test_javascript)
        assert "Written from python" in self.app.get_html()

if __name__ == '__main__':
    unittest.main()
