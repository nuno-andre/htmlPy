class GeneralTest:
    def test_app_geometry(self):
        assert self.app.width == 40
        assert self.app.height == 80
        assert self.app.x_pos == 10
        assert self.app.y_pos == 20
        assert self.app.maximized == False

        assert int(self.app.window.width()) == 40
        assert int(self.app.window.height()) == 80
        assert int(self.app.window.pos().x()) == 10
        assert int(self.app.window.pos().y()) == 20

    def test_max_app_geometry(self):
        assert self.max_app.width == -1
        assert self.max_app.height == -1
        assert self.max_app.x_pos == -1
        assert self.max_app.y_pos == -1
        assert self.max_app.maximized == True

        assert int(self.max_app.window.windowState()) == 2

    def test_app_title(self):
        assert str(self.app.window.windowTitle()) == "Test"

    def test_max_app_title(self):
        assert str(self.max_app.window.windowTitle()) == "Test maximized"
