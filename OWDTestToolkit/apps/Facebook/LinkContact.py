from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def LinkContact(self, p_contactEmail):
        #
        # After clicking the link contact button, use this to click on a contact.
        #
        
        # (For some reason this only works if I get all matching elements regardless of visibility,
        # THEN check for visibility. There must be a matching element that never becomes visible.)
        x = self.UTILS.getElements(DOM.Facebook.link_friends_list, "Facebook 'link friends' list", False, 20)
        
        email = False
        
        for i in x:
            if i.is_displayed():
                #
                # Keep the name and email details for this contact.
                #
                thisContact = i.find_elements("tag name", "p")[1]
                if thisContact.text == p_contactEmail:
                    email = p_contactEmail
                    thisContact.tap()
                    break

        self.UTILS.TEST(email, "Desired link contact's email address is displayed.")
        
        if email:
            self.UTILS.logComment("Linked FB contact email: " + email + ".")
        
        #
        # Switch back and wait for contact details page to re-appear.
        #
        time.sleep(2)
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

