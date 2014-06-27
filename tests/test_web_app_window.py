import unittest
import htmlPy
import general_test

class TestWebAppWindow(unittest.TestCase, general_test.GeneralTest):

    def setUp(self):
        self.app = htmlPy.WebAppWindow(title="Test", width=40, height=80, x_pos=10, y_pos=20)
        self.max_app = htmlPy.WebAppWindow(title="Test maximized", maximized=True)

    def test_linking(self):
        self.app.set_url("http://www.example.com/")
        assert self.app.get_url() == "http://www.example.com/"
        # Direct HTML comparison cannot be done without starting the app

if __name__ == '__main__':
    unittest.main()
