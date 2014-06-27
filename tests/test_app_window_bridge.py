import unittest
import htmlPy
import os

class TestAppWindowBridge(unittest.TestCase):

    def setUp(self):
        self.app = htmlPy.AppWindow(title="Test", width=40, height=80, x_pos=10, y_pos=20)
        self.test_template = "index.html"
        self.test_context = {"appname": "htmlPy"}
        self.app.set_template_path(os.path.abspath(os.path.dirname(__file__)))
        self.app.set_asset_path(os.path.abspath(os.path.dirname(__file__)))

        app = self.app
        template = self.test_template
        class BridgeCheck(htmlPy.Bridge):
            @htmlPy.attach()
            def change_superman(self):
                app.set_template(template, {"appname": "Superman"})

            @htmlPy.attach()
            def change_batman(self):
                app.set_template(template, {"appname": "Batman"})

            @htmlPy.attach(result=str)
            def change_deathstroke(self):
                return "Deathstroke"

            @htmlPy.attach(str)
            def change_custom(self, name):
                app.set_template(template, {"appname": name})

        self.test_bridge = BridgeCheck()

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

    def test_register(self):
        self.app.set_template(self.test_template, self.test_context)
        self.app.register(self.test_bridge)

        self.app.execute_javascript("BridgeCheck.change_superman()")
        assert "<h1>Superman" in self.app.get_html()

    def test_bridge_retention(self):
        self.app.set_template(self.test_template, self.test_context)
        self.app.register(self.test_bridge)

        self.app.execute_javascript("BridgeCheck.change_superman()")
        self.app.execute_javascript("BridgeCheck.change_batman()")
        assert "<h1>Batman" in self.app.get_html()

    def test_bridge_function_arguments(self):
        self.app.set_template(self.test_template, self.test_context)
        self.app.register(self.test_bridge)
        self.app.execute_javascript("BridgeCheck.change_custom('Iron man')")
        assert "<h1>Iron man" in self.app.get_html()

    def test_bridge_function_return_vals(self):
        self.app.set_template(self.test_template, self.test_context)
        self.app.register(self.test_bridge)
        self.app.execute_javascript("document.write(BridgeCheck.change_deathstroke())")
        assert "Deathstroke" in self.app.get_html()


    def test_link_click(self):
        pass

    def test_form_submit(self):
        pass


if __name__ == '__main__':
    unittest.main()
