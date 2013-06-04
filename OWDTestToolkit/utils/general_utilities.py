from global_imports import *
from gaiatest import GaiaTestCase

class main(GaiaTestCase):
    
    def clearGeolocPermission(self, p_allow=False):
        #
        # Since this appers all over the place I've added this
        # as a common method in UTILS.<br>
        # This method clears the Geolocation permission dialog
        # (if necessary) with p_allow.
        #
        orig_frame = self.currentIframe()
        self.marionette.switch_to_frame()
        try:
            if p_allow:
                x = self.marionette.find_element("id", "permission-yes")
            else:
                x = self.marionette.find_element("id", "permission-no")
                
            x.tap()
            
        except:
            pass
        
        self.switchToFrame("src", orig_frame)
        
    
    def typeThis(self, p_element_array, p_desc, p_str, p_no_keyboard=False, p_clear=True, p_enter=True, p_validate=True):        
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
            x.click()

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
            
        #
        # Try to tap the header to remove the keyboard now that we've finished.
        #
        try:
            x = self.marionette.find_element(*DOM.GLOBAL.app_head)
            x.tap()
            time.sleep(0.5)
        except:
            pass
        
    def setTimeToNow(self, p_continent=False, p_city=False):
        #
        # Set the phone's time (using gaia data_layer instead of the UI).
        #
        _continent = p_continent if p_continent else self.get_os_variable("GLOBAL_YOUR_CONTINENT")
        _city      = p_city      if p_city      else self.get_os_variable("GLOBAL_YOUR_CITY")
        
        self.logResult("info", "(Setting timezone and time based on " + _continent + " / " + _city + ".)")
        
        self.parent.data_layer.set_setting('time.timezone', _continent + "/" + _city)
        self.parent.data_layer.set_time(time.time() * 1000)
        
    def get_os_variable(self, p_name, p_validate=True):
        #
        # Get a variable from the OS.
        #
        if p_name == "ENTER":
            return ""
        else:
            try:
                x = os.environ[p_name]
            except:
                x = False
            
            if p_validate:
                self.TEST(x, "Variable '" + p_name + "' set to: " + str(x) + ".", True)
                
            return x

    #
    # (Can't use the 'push_resource' from gaiatest because I want to use
    # *any* directory specified by the caller.)
    #
    def addFileToDevice(self, p_file, count=1, destination=''):
        #
        # Put a file onto the device (path is relative to the dir
        # you are physically in when running the tests).
        #
        self.parent.device.push_file(p_file, count, '/'.join(['sdcard', destination]))

    
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
        # Find and click the list item (it may be off the scree, so 'displayed' would be false, but
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
        ok_btn = ('css selector', 'button.value-option-confirm')
        close_button = self.getElement(ok_btn, "OK button", True, 30)
        close_button.click()

        #
        # Return to the orginal frame.
        #
        self.switchToFrame("src", orig_iframe)



#         #
#         # This won't be around for too long hopefully, so just leave these
#         # DOM defs here.
#         #
#         options = self.getElements(('xpath', '//section[@id="value-selector-container"]//span'), 
#                                            "Item list (first attempt)", False, 20, False)
#         
#         ok_button = self.getElement(('css selector', 'button.value-option-confirm'), 
#                                           "Confirm selection button", False, 20, False)
# 
#         #
#         # Is the scroller visible?
#         #                
#         boolOK = False
#         if len(options) > 0:
#             # Loop options until we find the match
#             pos    = 0
#             for el in options:
#                 if el.text == p_str:
#                     #
#                     # Move the screen up to expose this element - a pretty brutal hack, 
#                     # but until I can get marionette.flick() to do it it'll have to do.
#                     #
#                     self.marionette.execute_script("document.getElementsByTagName('li')[" + str(pos) + "].scrollIntoView();")
#                     self.marionette.execute_script("document.getElementById('statusbar').scrollIntoView();")
#                     time.sleep(2)
#                     el.tap()
#                     time.sleep(2)
#                     boolOK = True
#                     break
# 
#                 pos = pos + 1
# 
#         #
#         # Did we find it?
#         #    
#         self.TEST(boolOK, "'" + p_str + "' found in selector", False)
# 
#         #
#         # Click the OK button.
#         #
#         ok_button.click()
# 
#         # Now back to app
#         self.switchToFrame("src", orig_iframe)