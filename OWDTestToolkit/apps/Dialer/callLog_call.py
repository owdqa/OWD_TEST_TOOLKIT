from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def callLog_call(self, p_num):
        #
        # Get own number.
        #
        own_num = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")

        #
        # Calls a number from the call log.
        #
        try:
            self.wait_for_element_displayed(*DOM.Dialer.call_log_filter, timeout=1)
        except:
            self.openCallLog()

        x = self.UTILS.getElement( ("xpath", DOM.Dialer.call_log_number_xpath % p_num),
                                   "The call log for number %s" % p_num)
        x.tap()

        x = self.UTILS.getElement( DOM.Dialer.call_log_numtap_call, "Call button")
        x.tap()
        if own_num == p_num:
            time.sleep(2)
            #self.marionette.switch_to_frame()
            x = self.UTILS.getElement(DOM.Dialer.call_busy_button_ok, "OK button (callLog_call)")
            x.tap()
        else:
            time.sleep(1)
            self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)
            self.UTILS.waitForElements( ("xpath", DOM.Dialer.outgoing_call_numberXP % p_num),
                                    "Outgoing call found with number matching %s" % p_num)