from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def checkAirplaneModeWarning(self):
        #
        # Checks for the presence of the popup
        # warning message if you just sent a message
        # while in 'airplane mode' (also removes
        # the message so you can continue).
        #
        x = self.UTILS.getElement(DOM.Messages.airplane_warning_header, "Airplane mode warning message",
                                  True, 5, False)
        if x:
            _popup_title = "Airplane mode activated"
            self.UTILS.TEST(x.text == _popup_title, 
                            "Warning message title = '" + _popup_title + "'.")
            
            x = self.UTILS.getElement(DOM.Messages.airplane_warning_ok, "OK button")
            x.tap()


