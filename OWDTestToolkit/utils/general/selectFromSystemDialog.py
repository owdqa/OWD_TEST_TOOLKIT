from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def selectFromSystemDialog(self, p_str):
        #
        # Selects an item from a system select box (such as country / timezone etc...).
        #
        
        #
        # Remember the current frame then switch to the system level one.
        #
        orig_iframe = self.currentIframe()
        self.marionette.switch_to_frame()

        #
        # Find and click the list item (it may be off the screen, so 'displayed' would be false, but
        # Marionette will scroll it into view automtically so it can be clicked just as it
        # would it real life).
        #
        xpath_val = "//section[@id='value-selector-container']//li[label[span[text()='%s']]]" % p_str
        list_item = self.getElement( ("xpath", xpath_val), "'" + p_str + "' in the selector", False) 
        list_item.click()
         
        #
        # A bug in Marionette just now moves the entire screen up, so the statusbar
        # dissappears off the top of the display. This hack corrects it.
        #
        self.marionette.execute_script("document.getElementById('statusbar').scrollIntoView();")
        
        #
        # Find and click OK.
        #
        close_button = self.getElement(DOM.GLOBAL.modal_valueSel_ok, "OK button", True, 30)
        close_button.click()

        #
        # Return to the orginal frame.
        #
        self.switchToFrame("src", orig_iframe)

