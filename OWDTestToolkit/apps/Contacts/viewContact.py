from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def viewContact(self, p_contact_name, p_HeaderCheck=True):
        #
        # Navigate to the 'view details' screen for a contact (assumes we are in the
        # 'view all contacts' screen).
        # <br>
        # In some cases you don't want this to check the header (if the contact has no name
        # for example). In that case, set p_HeaderCheck=False.
        #
        y = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "All contacts list", False)
        time.sleep(1)
        i_count=-1
        for i in y:
            i_count = i_count + 1
            self.UTILS.logResult("info", "'%s'" % i.text)
            if p_contactName in i.text:
                self.UTILS.logResult("info", "Contact '%s' found in all contacts." % p_contactName)
                self.marionette.execute_script("document.getElementsByClassName('contact-item')[%s].click()" %\
                                               i_count)
#                 i.tap()
                return
                
        self.UTILS.logResult("info", "Contact '%s' was <b>not</b> found in the contacts list." % p_contactName)
        
        self.UTILS.waitForElements(DOM.Contacts.view_details_title, "'View contact details' title")

        # 
        # TEST: Correct contact name is in the page header.
        #
        if p_HeaderCheck:
            self.UTILS.headerCheck(p_contact_name)
            
        time.sleep(2)
