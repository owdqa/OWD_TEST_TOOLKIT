from assertions import AssertionManager


class test(object):

    def __init__(self, parent):
        self.parent = parent
        self.assertion_manager = AssertionManager()
        self.assertion_manager.reset_test()
        self.passed = self.assertion_manager.passed
        self.failed = self.assertion_manager.failed

    def test(self, result, msg, stop_on_error=False):
        #
        # Test that result is true.
        #
        # One advantage of this over the standard 'assert's is that
        # this continues past a failure if stop_on_error is False.
        # However, it also takes a screenshot and dumps the html source
        # if result is False.
        #
        self.parent.reporting.log_to_file(u"Testing with {} and message: {}. stop_on_error: {}".\
                                          format(result, msg, stop_on_error))

        details = False
        processed_msg = msg.split("|")
        if result:
            self.parent.reporting.logResult(result, processed_msg[0])
            self.assertion_manager.inc_passed()
        else:
            details = self.parent.debug.screenShotOnErr()
            # This has to be processed here due to the new behavior of reportResults
            if len(processed_msg) > 1:
                details.extend(processed_msg[1:])
                self.parent.reporting.logResult(result, processed_msg[0], details)
            else:
                self.parent.reporting.logResult(result, msg, details)
            self.assertion_manager.inc_failed()

        self.parent.parent.assertTrue(result)
