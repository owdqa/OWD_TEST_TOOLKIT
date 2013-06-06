from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def is_element_present(self, by, locator, timeout=600):
        try:
            self.marionette.set_search_timeout(timeout)
            self.marionette.find_element(by, locator)
            return True
        except:
            return False
        finally:
            # set the search timeout to the default value
            self.marionette.set_search_timeout(10000)

    # do a long press on a character
