from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def scrollHomescreenLeft(self):
        #
        # Scroll to previous page (left).
        # Should change this to use marionette.flick() when it works.
        #
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToPreviousPage()')
    
