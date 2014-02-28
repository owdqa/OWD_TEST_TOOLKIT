import json
from OWDTestToolkit.global_imports import *


class main(GaiaTestCase):

    def insertContact(self, contact):
        self.marionette.switch_to_frame()
        mozcontact = contact.create_mozcontact()
        result = self.marionette.execute_async_script('return GaiaDataLayer.insertContact(%s);' % json.dumps(mozcontact), special_powers=True)
        assert result, 'Unable to insert contact %s' % contact