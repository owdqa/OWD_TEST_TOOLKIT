from global_imports import *
from gaiatest import GaiaTestCase

class main(GaiaTestCase):
    def TEST(self, p_result, p_msg, p_stop = False):
        #
        # Test that p_result is true.
        #
        # One advantage of this over the standard 'assert's is that
        # this continues past a failure if p_stop is False.
        # However, it also takes a screenshot and dumps the html source
        # if p_result is False.
        #
        fnam = False
        if not p_result:
            fnam = self.screenShotOnErr()
            self.failed = self.failed + 1
            self.logResult(p_result, p_msg, fnam)

            if p_stop:
                self.quitTest()
        else:
            self.passed = self.passed + 1
            self.logResult(p_result, p_msg)
        

    def quitTest(self, p_msg=False):
        #
        # Quit this test suite.
        #
        if not p_msg:
            msg = "CANNOT CONTINUE PAST THIS ERROR - ABORTING THIS TEST CASE!"
        else:
            msg = p_msg

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
        