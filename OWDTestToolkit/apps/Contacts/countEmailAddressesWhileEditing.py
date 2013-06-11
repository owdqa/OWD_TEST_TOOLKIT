from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def countEmailAddressesWhileEditing(self):
        #
        # Count the emails and return the number - assumes you 
        # are currently EDITING the contact (not viewing).
        #
        
        #
        # (for some reason these are flagged as not displayed, so
        # you have to get them as 'present').
        #
        x = self.UTILS.getElements(DOM.Contacts.email_fields, "Email fields", False, 2)
        self.UTILS.logResult("info", 
                             "NOTE: Contact's email addresses:")
        counter = 0
        for i in x:
            if i.get_attribute("value") != "#value#":
                counter = counter + 1
                self.UTILS.logResult("info", "    - " + str(counter) + ": " + i.get_attribute("value"))
            
        return counter

