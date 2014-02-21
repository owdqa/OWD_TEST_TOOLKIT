from OWDTestToolkit.global_imports import *
from OWDTestToolkit.apps.Dialer import *

class main(GaiaTestCase):

    def callID_verify(self):

        x = self.UTILS.getElement(DOM.Settings.call_settings, "Call number button")
        x.tap()
        self.UTILS.logResult("info", "Call number presses")
        time.sleep(20)

        x = self.UTILS.getElement(DOM.Settings.call_button, "Call ID button")
        x.tap()
        self.UTILS.logResult("info", "Call ID button presses")

        #Change Frame
        self.marionette.switch_to_frame()

        #Get option selected
        x = self.UTILS.getElement(DOM.Settings.call_show_number, "Call Option value")
        y = x.get_attribute("aria-selected")

        self.UTILS.logResult("info", "Screen shot of the result of tapping call button", y)
        self.UTILS.TEST( y=="true", "Checking Call ID value")