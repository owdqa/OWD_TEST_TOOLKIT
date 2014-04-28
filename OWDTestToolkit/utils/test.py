import sys
import os


class test(object):

    def __init__(self, parent):
        self.parent = parent

    def quitTest(self, msg=False):
        #
        # Quit this test suite.
        #
        if not msg:
            msg = "CANNOT CONTINUE PAST THIS ERROR - ABORTING THIS TEST CASE!"
        else:
            msg = msg

        self.parent.reporting.logResult("info", " ")
        self.parent.reporting.logResult(False, msg)

        #
        # Collect info on every iframe for debugging ...
        #
        
        self.parent.reporting.logResult("info", "<b style='color: #62E3C5'>Starting frame dump...</b>")
        self.parent.iframe.view_all_iframes()

        #
        # Report the results.
        #
        self.parent.reporting.reportResults()

        #
        # Exit immediately without throwing an exception
        # (otherwise it looks like Marionette hit a problem).
        #
        # sys.exit(1)
        # 
        
        #
        # By definition, sys.exit() raises a ExitValue exception.
        # If we don't want an exception to be raised at this point,
        # then we should use os._exit().
        # 
        # **** NOTE **** : The call to os._exit() is dangerous, so
        # if thing go odd, please go back to sys.exit()
        #
        os._exit(1)

    def TEST(self, result, msg, stop_on_error=False):
        #
        # Test that result is true.
        #
        # One advantage of this over the standard 'assert's is that
        # this continues past a failure if stop_on_error is False.
        # However, it also takes a screenshot and dumps the html source
        # if result is False.
        #
        fnam = False
        if not result:
            fnam = self.parent.debug.screenShotOnErr()
            self.parent.reporting.logResult(result, msg, fnam)
            self.parent.debug.getStackTrace()

            if stop_on_error:
                self.quitTest()
        else:
            self.parent.reporting.logResult(result, msg)
