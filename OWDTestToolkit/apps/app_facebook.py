import time
from gaiatest   import GaiaTestCase
from marionette import Marionette
from OWDTestToolkit import *

class AppFacebook(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.marionette = p_parent.marionette
        self.UTILS      = p_parent.UTILS

    def importAll(self):
        #
        # Import all contacts after enabling fb via Contacts Settings.
        #

        #
        # Get the count of friends that will be imported.
        #
        x = self.UTILS.getElements(DOM.Facebook.friends_list, "Facebook friends list")
        friend_count = len(x)
        
        #
        # Tap "Select all".
        #
        x = self.UTILS.getElement(DOM.Facebook.friends_select_all, "'Select all' button")
        x.tap()
        
        #
        # Tap "Import".
        #
        x = self.UTILS.getElement(DOM.Facebook.friends_import, "Import button")
        x.tap()
        
        #
        # Switch back to the contacts frame.
        #
        # (The 'importing ..' splash screen that appears confuses the frame switch
        # so the simplest thing is to just wait for a long time to make sure it's
        # gone.)
        #
        time.sleep(5)
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        
        #
        # Return the number of friends we imported.
        #
        return friend_count
    
    def LinkContact(self, p_contactEmail):
        #
        # After clicking the link contact button, use this to click on a contact.
        #
        
        # (For some reason this only works if I get all matching elements regardless of visibility,
        # THEN check for visibility. There must be a matching element that never becomes visible.)
        x = self.UTILS.getElements(DOM.Facebook.link_friends_list, "facebook friends list", False, 20)
        
        email = False
        
        for i in x:
            if i.is_displayed():
                #
                # Keep the name and email detais for this contact.
                #
                thisContact = i.find_elements("tag name", "p")[1]
                if thisContact.text == p_contactEmail:
                    i.tap()
                    email = p_contactEmail
                    break

        self.UTILS.TEST(email, "Desired link contact's email address is displayed.")
        
        if email:
            self.UTILS.logComment("Linked FB contact email: " + email + ".")
        
        #
        # Switch back and wait for contact details page to re-appear.
        #
        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Facebook.friends_iframe_1)

    def login(self, p_user, p_pass):
        #
        # Log into facebook (and navigate to the facebook login frame ... sometimes!!).
        #
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Facebook.import_frame)

        x = self.UTILS.getElement(DOM.Facebook.email, "User field", True, 180)
        x.clear()
        x.send_keys(p_user)
        
        x = self.UTILS.getElement(DOM.Facebook.password, "Password field")
        x.clear()
        x.send_keys(p_pass)
        
        x = self.UTILS.getElement(DOM.Facebook.login_button, "Login button")
        x.tap()
        
        time.sleep(3)