from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def typeThis(self, 
                 p_element_array, 
                 p_desc, 
                 p_str, 
                 p_no_keyboard=False, 
                 p_clear=True, 
                 p_enter=True, 
                 p_validate=True, 
                 p_remove_keyboard=True):        
        #
        # Types this string into this element.
        # If p_no_keyboard = True then it doesn't use the keyboard.
        # <b>NOTE:</b> If os variable "NO_KEYBOARD" is set (to anything), 
        # then regardless of what you send to this method, it will never 
        # use the keyboard.
        #
        NOKEYBOARD = self.get_os_variable("NO_KEYBOARD", False)
        
        #
        # Make sure the string is a string!
        #
        p_str = str(str(p_str))
        
        #
        # Remember the current frame.
        #
        orig_frame = self.currentIframe()
         
        x = self.getElement(p_element_array, p_desc)
        
        #
        # Need to click in a lot of these or the field isn't located correctly (esp. SMS).
        #
        x.click()
        
        if p_clear: x.clear()

        if NOKEYBOARD or p_no_keyboard:
            #
            # Don't use the keyboard.
            #
            self.logResult("info", "(Sending '" + p_str + "' to this field without using the keyboard.)")
            x.send_keys(p_str)
            
            #
            # There's a weird 'quirk' in Marionette just now:
            # if you send_keys() an underscore ("_") then the
            # screen is locked. No idea who thought that was a
            # good idea, but it seems it's here to stay, so unlock()
            # if necessary.
            #
            if "_" in p_str:
                self.parent.lockscreen.unlock()
                self.marionette.switch_to_frame()
                self.switchToFrame("src", orig_frame)
                
        else:
            #
            # Tap the element to get the keyboard to popup.
            #
            self.logResult("info", "(Sending '" + p_str + "' to this field using the keyboard.)")
            x.tap()

            #
            # Type the string.
            #
            self.parent.keyboard.send(p_str)
        
             
        #
        # Tap ENTER on the keyboard (helps to remove the kayboard even if
        # you didn't use it to type)?
        #
        if p_enter:
            self.parent.keyboard.tap_enter()
               
        #
        # Switch back to the frame we were in and get the element again.
        #
        self.marionette.switch_to_frame()
        self.switchToFrame("src", orig_frame)
         
        #
        # Validate that the field now has the value we sent it.
        #
        if p_validate:            
            x = self.marionette.find_element(*p_element_array)
            y = x.get_attribute("value")
    
            if p_clear:
                fieldText = y
            else:
                fieldText = y[-(len(p_str)):]
            
            self.TEST(p_str == fieldText, 
                      "The field contains the correct string ...|" + fieldText + "|- vs. -|" + p_str)
            
        if p_remove_keyboard:
            #
            # Try to tap the header to remove the keyboard now that we've finished.
            #
            try:
                x = self.marionette.find_element(*DOM.GLOBAL.app_head)
                x.tap()
                time.sleep(0.5)
            except:
                pass
        
