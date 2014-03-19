from OWDTestToolkit import DOM
import time


class Facebook(object):

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS

    def launch(self):
        #
        # Launch the app.
        #
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        return self.app

    def importAll(self):
        #
        # Import all contacts after enabling fb via Contacts Settings.
        #

        #
        # Get the count of friends that will be imported.
        #
        x = self.UTILS.getElements(DOM.Facebook.friends_list, "Facebook 'import friends' list")
        friend_count = len(x)

        #
        # Tap "Select all".
        #
        x = self.UTILS.getElement(DOM.Facebook.friends_select_all, "'Select all' button")
        # x.tap()
        self.UTILS.simulateClick(x)

        #
        # Tap "Import".
        #
        x = self.UTILS.getElement(DOM.Facebook.friends_import, "Import button")
        # x.tap()
        self.UTILS.simulateClick(x)

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
        self.UTILS.logComment("Friend count: {}".format(friend_count))
        return friend_count

    def LinkContact(self, contact_email):
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
                if thisContact.text == contact_email:
                    email = contact_email
                    self.UTILS.simulateClick(thisContact)
                    break

        self.UTILS.TEST(email, "Desired link contact's email address is displayed.")

        if email:
            self.UTILS.logComment("Linked FB contact email: " + email + ".")

        #
        # Switch back and wait for contact details page to re-appear.
        #
        time.sleep(2)
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

    def login(self, user, passwd):
        #
        # Log into facebook (and navigate to the facebook login frame ... sometimes!!).
        #
        self.UTILS.switchToFrame(*DOM.Facebook.import_frame)

        x = self.UTILS.getElement(DOM.Facebook.email, "User field", True, 60)
        x.clear()
        x.send_keys(user)

        x = self.UTILS.getElement(DOM.Facebook.password, "Password field")
        x.clear()
        x.send_keys(passwd)

        x = self.UTILS.getElement(DOM.Facebook.login_button, "Login button")
        x.tap()
