from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def verifyLinked(self, p_contact_name, p_fb_email):
        #
        # Verifies that this contact is linked
        # (assumes we're in the 'all contacts' screen).
        #
        
        self.launch()
        
        #
        # Check that our contact is now listed as a facebook contact (icon by the name in 'all contacts' screen).
        #
        x = self.UTILS.getElements(DOM.Contacts.social_network_contacts, "Social network contacts")
        self.UTILS.TEST(len(x) > 0, "Contact is listed as a facebook contact after linking.")

        #
        # View the details for this contact.
        #
        self.viewContact(p_contact_name)
        
        #
        # Check the expected elements are now visible. 
        #
        # I'm having serious problems finding buttons based on 'text' directly, so here's
        # the 'brute-force' method ...
        boolViewFbProfile   = False
        boolWallPost        = False
        boolLinkedEmail     = False
        boolUnLink          = False
        x = self.UTILS.getElements(("tag name", "button"), "All buttons on this page")
        for i in x:
            if i.text == "View Facebook profile": boolViewFbProfile = True
            if i.text == "Wall post"            : boolWallPost      = True
            if i.text == p_fb_email             : boolLinkedEmail   = True
            if i.text == "Unlink contact"       : boolUnLink        = True
            
        self.UTILS.TEST(boolViewFbProfile   , "'View Facebook profile' button is displayed after contact linked to fb contact.")
        self.UTILS.TEST(boolWallPost        , "'Wall post' button is displayed after contact linked to fb contact.")
        self.UTILS.TEST(boolUnLink          , "'Unlink contact' button is displayed after contact linked to fb contact.")
        self.UTILS.TEST(boolLinkedEmail     , "Linked facebook email address is displayed after contact linked to fb contact.")
        
