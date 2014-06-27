import unittest
import htmlPy
import os
import json
from nose.plugins.attrib import attr

class TestAppWindowBridge(unittest.TestCase):

    def setUp(self):
        self.app = htmlPy.AppWindow(developer_mode=True)
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

            @htmlPy.attach(str)
            def form_batman(self, data):
                data = json.loads(str(data))
                app.set_template(template, {"appname": data["name"]})

            @htmlPy.attach(str, str)
            def form_joker(self, data, params):
                data = json.loads(str(data))
                app.set_template(template, {"appname": data["name"] + ", " + str(params)})

        self.app.register(BridgeCheck())

    def manually_execute_bridge_helper_javascript(self, appl):
        # In automated testing, this has to be done manually
        # When in dev or production, the function loads 100ms after
        # the window starts. It is done by javascript setInterval
        script_path = "htmlPy/bridge_helper.js"
        try:
            f = open(script_path, "r")
        except:
            f = open("../" + script_path, "r")
        script = f.read()
        script = script.replace("setInterval(function(){", "")
        script = script.replace("}, 100);", "")
        appl.execute_javascript(script)

    def test_register(self):
        self.app.set_template(self.test_template, self.test_context)
        self.app.execute_javascript("BridgeCheck.change_superman()")
        assert "<h1>Superman" in self.app.get_html()

    def test_bridge_retention(self):
        self.app.set_template(self.test_template, self.test_context)
        self.app.execute_javascript("BridgeCheck.change_superman()")
        self.app.execute_javascript("BridgeCheck.change_batman()")
        assert "<h1>Batman" in self.app.get_html()

    def test_bridge_function_arguments(self):
        self.app.set_template(self.test_template, self.test_context)
        self.app.execute_javascript("BridgeCheck.change_custom('Iron man')")
        assert "<h1>Iron man" in self.app.get_html()

    def test_bridge_function_return_vals(self):
        self.app.set_template(self.test_template, self.test_context)
        self.app.execute_javascript("document.write(BridgeCheck.change_deathstroke())")
        assert "Deathstroke" in self.app.get_html()

    @attr("no-coverage")
    # Have to disable some tests due to automation incompatibilities of Qt
    # The results of these test vary python/qt version to version
    # However, this should not be an issue in dev/production, only in testing.
    def test_link_click(self):
        self.app.set_template(self.test_template, self.test_context)
        self.manually_execute_bridge_helper_javascript(self.app)
        self.app.execute_javascript("document.getElementById('test_link_click').click()")
        assert "<h1>Superman" in self.app.get_html()

    @attr("no-coverage")
    # Have to disable some tests due to automation incompatibilities of Qt
    # The results of these test vary python/qt version to version
    # However, this should not be an issue in dev/production, only in testing.
    def test_link_click_params(self):
        self.app.set_template(self.test_template, self.test_context)
        self.manually_execute_bridge_helper_javascript(self.app)
        self.app.execute_javascript("document.getElementById('test_link_click_params').click()")
        assert "<h1>Iron man" in self.app.get_html()

    @attr("no-coverage")
    # Have to disable some tests due to automation incompatibilities of Qt
    # The results of these test vary python/qt version to version
    # However, this should not be an issue in dev/production, only in testing.
    def test_link_click_404(self):
        self.app.set_template(self.test_template, self.test_context)
        self.manually_execute_bridge_helper_javascript(self.app)
        html = self.app.get_html()
        self.app.execute_javascript("document.getElementById('test_link_click_404').click()")
        assert html == self.app.get_html()

    def test_form_submit(self):
        self.app.set_template(self.test_template, self.test_context)
        self.manually_execute_bridge_helper_javascript(self.app)
        self.app.execute_javascript("document.getElementById('test_form_submit_input').value='Python'")
        self.app.execute_javascript("document.getElementById('test_form_submit_button').click()")
        assert "<h1>Python" in self.app.get_html()

    def test_form_submit_params(self):
        self.app.set_template(self.test_template, self.test_context)
        self.manually_execute_bridge_helper_javascript(self.app)
        self.app.execute_javascript("document.getElementById('test_form_submit_params_input').value='Batman'")
        self.app.execute_javascript("document.getElementById('test_form_submit_params_button').click()")
        # Note: Javascript form.submit() does not call onsubmit callback
        assert "<h1>Batman, Why so serious?" in self.app.get_html()


if __name__ == '__main__':
    unittest.main()
