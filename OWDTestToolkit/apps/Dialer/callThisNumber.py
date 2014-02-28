from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def callThisNumber(self):
        #
        # Get the current number.
        #
        x = self.UTILS.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = x.get_attribute("value")

        #
        # Get own number.
        #
        own_num = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")

        #
        # Calls the current number.
        #
        x = self.UTILS.getElement(DOM.Dialer.call_number_button, "Call number button")
        x.tap()

        self.UTILS.checkMarionetteOK()
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)
        self.UTILS.waitForElements(DOM.Dialer.outgoing_call_locator, "Outgoing call element", True, 5)
