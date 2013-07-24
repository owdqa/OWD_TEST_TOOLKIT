from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def enterNumber(self, p_num):
        #
        # Enters a number into the dialler using the keypad.
        #
        for i in str(p_num):
        	x = self.UTILS.getElement( ("xpath", DOM.Dialer.dialler_button_xpath % i),
									"keypad number %s." % i)
        	x.tap()
        
        #
        # Verify that the number field contains the expected number.
        #
        x = self.UTILS.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = x.get_attribute("value")
        self.UTILS.TEST(str(p_num) in dialer_num, "'%s' contains '%s'." % (dialer_num, str(p_num)))
