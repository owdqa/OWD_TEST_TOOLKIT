from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def quitTest(self, p_msg=False):
        #
        # Quit this test suite.
        #
        if not p_msg:
            msg = "CANNOT CONTINUE PAST THIS ERROR - ABORTING THIS TEST CASE!"
        else:
            msg = p_msg

        self.logResult("info", " ") #(blank line)
        self.logResult(False, msg)

        #
        # Collect info on every iframe for debugging ...
        #
        self.viewAllIframes()
        
        #
        # Report the results.
        #
        self.reportResults()
        
        #
        # Exit immediately without throwing an exception
        # (otherwise it looks like Marionette hit a problem).
        #
        import os
        os._exit(1)
