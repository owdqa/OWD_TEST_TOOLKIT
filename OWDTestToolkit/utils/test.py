import sys


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
        self.parent.iframe.viewAllIframes()

        #
        # Report the results.
        #
        self.parent.reporting.reportResults()

        #
        # Exit immediately without throwing an exception
        # (otherwise it looks like Marionette hit a problem).
        #
        sys.exit(1)

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
