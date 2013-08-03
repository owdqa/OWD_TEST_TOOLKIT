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
#         contnam = p_contact_name.replace(" ","")
#         matcher = DOM.Contacts.view_all_contact_xpath % contnam
#         x = ("xpath", matcher)
#         
#         self.UTILS.logResult("info", "Using '%s' ..." % matcher)
#         contact_found = self.UTILS.getElement(x, "Contact '%s'" % p_contact_name)
#         contact_found.tap()
#         
#         self.UTILS.waitForElements(DOM.Contacts.view_details_title, "'View contact details' title")
        self.selectContactFromAll(p_contact_name)

        # 
        # TEST: Correct contact name is in the page header.
        #
        if p_HeaderCheck:
            self.UTILS.headerCheck(p_contact_name)
            
        time.sleep(2)
