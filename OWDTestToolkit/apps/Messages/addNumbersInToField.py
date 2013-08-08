from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def addNumbersInToField(self, p_nums):
        #
        # Add the numbers (or contact name) in the 'To'
        # field of this sms message.
        # Assumes you are in 'create sms' screen.
        # <br>
        # <b>p_nums</b> must be an array.
        #
        for i in p_nums:
            x = self.UTILS.screenShotOnErr()
            
            #
            # Even though we don't use the kayboard for putting the number in, 
            # we need it for the ENTER button (which allows us to put more than
            # one number in).
            #
            # So check that the keyboard appears when we tap the "TO" field if we have
            # more than one number.
            #
            if len(p_nums) > 1:
                self.UTILS.logResult("info", "Checking the keyboard appears when I tap the 'To' field ...")
                x = self.UTILS.getElement(DOM.Messages.target_numbers_empty, "Target number field")
                x.tap()
    
                boolKBD=False
                self.marionette.switch_to_frame()
                
                try:
                    #
                    # A 'silent' check to see if the keyboard iframe appears.
                    elDef = ("xpath", "//iframe[contains(@%s, '%s')]" % \
                             (DOM.Keyboard.frame_locator[0],DOM.Keyboard.frame_locator[1]))
                    self.wait_for_element_displayed(*elDef, timeout=2)
                    boolKBD = True
                except:
                    boolKBD=False
                    
                self.UTILS.TEST(boolKBD, "Keyboard is displayed when 'To' field is clicked.")
    
                self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
            
            #
            # Seems okay, so proceed ...
            #
            self.UTILS.typeThis(DOM.Messages.target_numbers_empty, 
	                            "Target number field", 
	                            i, 
	                            p_no_keyboard=True,
	                            p_validate=False,
	                            p_clear=False,
	                            p_enter=True)

        for i in p_nums:
            self.checkIsInToField(i)
        
