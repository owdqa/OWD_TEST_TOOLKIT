from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def callLog_addToContact(self, p_num, p_name, p_openCallLog=True):
    #
    # Adds this number in the call log to an existing contact
    # (and returns you to the call log).
        # If p_openCallLog is set to False it will assume you are
        # already in the call log.
        #
        if p_openCallLog:
            self.openCallLog()

        time.sleep(1)

        x = self.UTILS.getElement( ("xpath", DOM.Dialer.call_log_number_xpath % p_num),
                               "The call log for number %s" % p_num)
        x.tap()

        x = self.UTILS.getElement( DOM.Dialer.call_log_numtap_add_to_existing, "Add to existing contact button")
        x.tap()

        self._complete_addNumberToContact(p_num, p_name)