from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def addContactToThisSMS(self, p_contactName):
        #
        # Uses the 'add contact' button to add a contact to SMS.
        #
        self.UTILS.logResult("info", "Trying to add '" + p_contactName  + "' to the SMS via search button ...")
        
        orig_iframe = self.selectAddContactButton()
        
        #
        # Search the contacts list for our contact.
        #
        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        for i in x:
            if i.text.lower() == p_contactName.lower():
                i.tap()
                break
            
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame("src",orig_iframe)
        
        #
        # Now check the correct name is in the 'To' list.
        #
        return self.checkIsInToField(p_contactName)

