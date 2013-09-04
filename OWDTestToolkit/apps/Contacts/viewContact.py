from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def viewContact(self, p_contactName, p_HeaderCheck=True):
        #
        # Navigate to the 'view details' screen for a contact (assumes we are in the
        # 'view all contacts' screen, either from Contacts app, or Dialer app).
        # <br>
        # In some cases you don't want this to check the header (if the contact has no name,
        # or you're just using the given name etc..). In that case, set p_HeaderCheck=False.
        #
        time.sleep(1)
        self.UTILS.checkMarionetteOK()
        
        self._findThisFrame()

        y = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "All contacts list", False, 10)
        
        self.UTILS.logResult("info", "%s contacts listed." % str(len(y)))
        ymax=len(y)
        boolFound=False
        for i in range(0,ymax):   
            self.UTILS.logResult("info", "'%s'" % y[i].text)
            if p_contactName.lower() in y[i].text.lower():
                boolFound = True
                self.UTILS.logResult("info", "Contact '%s' found in all contacts - selecting this contact ..." % p_contactName)
                self.marionette.execute_script("document.getElementsByClassName('contact-item')[%s].click()" % i)
                time.sleep(2)
                break

            #
            # Marionette seems to crash here occasionally, so make sure we're okay before
            # the next loop!
            #
            self.UTILS.checkMarionetteOK()
            self.UTILS.switchToFrame(*DOM.Contacts.frame_locator, p_quitOnError=False)
            y = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "All contacts list", False)
            
        if not boolFound:
            self.UTILS.logResult("info", "FYI: Contact '%s' was <b>not</b> found in the contacts list." % p_contactName)
            return
        
        #
        # TEST: Correct contact name is in the page header.
        #
        if p_HeaderCheck:
            self.UTILS.headerCheck(p_contactName)
        
        x = self._findThisFrame()

        if x == "Dialer":
            x = self.UTILS.getElement(DOM.Contacts.view_details_title,"View details title")
            self.UTILS.TEST(p_contactName in x.text, "Name is in the title")

        time.sleep(2)
        
    def _findThisFrame(self):
        #
        # Private method to cater for the fact that *SOMETIMES* the 
        # frame is different if coming from Dialer.
        #
        try:
            self.marionette.switch_to_frame()
            self.marionette.switch_to_frame("xpath", 
                                            "//iframe[contains(@%s,'%s')]" % \
                                            (DOM.Dialer.frame_locator[0],
                                             DOM.Dialer.frame_locator[1]))
            self.marionette.switch_to_frame("xpath", 
                                            "//iframe[contains(@%s,'%s')]" % \
                                            (DOM.Dialer.call_log_contact_name_iframe[0],
                                             DOM.Dialer.call_log_contact_name_iframe[1]))
            self.UTILS.logResult("info", "<i>Switched to dialer -> contacts iframe.)</i>")
            _frame = "Dialer"
        except:
            self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
            _frame = "Contacts"
            
        return _frame

        
        
        