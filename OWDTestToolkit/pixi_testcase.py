from gaiatest import GaiaTestCase


class PixiTestCase(GaiaTestCase):

    def setUp(self):
        super(PixiTestCase, self).setUp()
        self.data_layer.set_setting('ums.enabled', False)
        self.data_layer.set_setting('ums.mode', 0)
        self.data_layer.set_setting('ums.status', 0)
        self.data_layer.set_setting('keyboard.current', 'en-US')
        self.data_layer.set_setting('language.current', 'en-US')
