from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def viewContact(self, p_contactName, p_HeaderCheck=True):
        #
        # Navigate to the 'view details' screen for a contact (assumes we are in the
        # 'view all contacts' screen).
        # <br>
        # In some cases you don't want this to check the header (if the contact has no name
        # for example). In that case, set p_HeaderCheck=False.
        #
        time.sleep(1)
        self.UTILS.checkMarionetteOK()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator, p_quitOnError=False)
        y = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "All contacts list", False, 10)
        
        self.UTILS.logResult("info", "%s contacts listed." % str(len(y)))
        ymax=len(y)
        boolFound=False
        for i in range(0,ymax):   
            self.UTILS.logResult("info", "'%s'" % y[i].text)
            if p_contactName in y[i].text:
                boolFound = True
                self.UTILS.logResult("info", "Contact '%s' found in all contacts." % p_contactName)
                self.marionette.execute_script("document.getElementsByClassName('contact-item')[%s].click()" % i)
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
            
        time.sleep(2)
