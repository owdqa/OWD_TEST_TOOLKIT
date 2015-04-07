from gaiatest import GaiaTestCase


class FireCTestCase(GaiaTestCase):
    
    def setUp(self):
        super(FireCTestCase, self).setUp()
        self.data_layer.set_setting('ums.enabled', False)
        self.data_layer.set_setting('ums.mode', 0)
        self.data_layer.set_setting('ums.status', 0)
        self.data_layer.set_setting('keyboard.current', 'es')
        self.data_layer.set_setting('language.current', 'es')