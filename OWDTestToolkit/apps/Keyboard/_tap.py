from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def _tap(self, val):
        self.wait_for_element_displayed(*self._key_locator(val))
        key = self.marionette.find_element(*self._key_locator(val))
        key.tap()

    # This is for selecting special characters after long pressing
    # "selection" is the nth special element you want to select (n>=1)
