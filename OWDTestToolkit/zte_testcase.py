from gaiatest import GaiaTestCase


class ZTETestCase(GaiaTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(ZTETestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        super(ZTETestCase, self).setUp()
