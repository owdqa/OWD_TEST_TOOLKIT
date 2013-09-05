from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def viewContact(self, p_contactName, p_HeaderCheck=True):
                #
        # Navigate to the 'view details' screen for a contact (assumes we are in the
        # 'view all contacts' screen).
        # <br>
        # In some cases you don't want this to check the header (if the contact has no name,
        # or you're just using the given name etc..). In that case, set p_HeaderCheck=False.
        #
        time.sleep(1)
        self.UTILS.checkMarionetteOK()

        if self.apps.displayed_app.name == "Phone":
            self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)
            self.UTILS.switchToFrame(*DOM.Dialer.call_log_contact_name_iframe, p_viaRootFrame=False)

        else:
            self.UTILS.switchToFrame(*DOM.Contacts.frame_locator, p_quitOnError=False)

        time.sleep(1)
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
        

        if self.apps.displayed_app.name == "Phone":
            self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)
            self.UTILS.switchToFrame(*DOM.Dialer.call_log_contact_name_iframe, p_viaRootFrame=False)
            x = self.UTILS.getElement(DOM.Contacts.view_details_title,"View details title")
            self.UTILS.TEST(p_contactName in x.text, "Name is in the title")
        else:
            #
            # This shouldn't be necessary, but for some reason it is!
            #
            self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)