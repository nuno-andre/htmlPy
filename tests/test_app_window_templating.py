import unittest
import htmlPy
import os

class TestAppWindowTemplating(unittest.TestCase):

    def setUp(self):
        self.app = htmlPy.AppWindow(title="Test", width=40, height=80, x_pos=10, y_pos=20)
        self.test_template = "index.html"
        self.test_context = {"appname": "htmlPy"}
        self.app.set_template_path(os.path.abspath(os.path.dirname(__file__)))
        self.app.set_asset_path(os.path.abspath(os.path.dirname(__file__)))


    def test_template_rendering(self):
        html = self.app.render_template(self.test_template, self.test_context)
        assert "<h1>htmlPy" in html

    def test_template_setting(self):
        self.app.set_template(self.test_template, self.test_context)
        assert self.app.get_template() == self.test_template

    def test_template_display(self):
        self.app.set_template(self.test_template, self.test_context)
        assert "<h1>htmlPy" in self.app.get_html()

    def test_asset_tags_removal(self):
        self.app.set_template(self.test_template, self.test_context)
        assert "$asset$" not in self.app.get_html()

    def test_asset_path_processing(self):
        self.app.set_template(self.test_template, self.test_context)
        css_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "style.css")
        assert "file:///" + css_path in self.app.get_html()

if __name__ == '__main__':
    unittest.main()
