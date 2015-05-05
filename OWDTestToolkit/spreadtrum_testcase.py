from gaiatest import GaiaTestCase


class SpreadtrumTestCase(GaiaTestCase):

    def setUp(self):
        super(SpreadtrumTestCase, self).setUp()
        # self.data_layer.set_setting('keyboard.current', 'es')
        # self.data_layer.set_setting('language.current', 'es')
        self.device.storage_path = "/storage/sdcard"
        self.device._set_storage_path()