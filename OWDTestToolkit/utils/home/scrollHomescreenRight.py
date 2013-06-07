from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def scrollHomescreenRight(self):
        #
        # Scroll to next page (right).
        # Should change this to use marionette.flick() when it works.
        #
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToNextPage()')
    
