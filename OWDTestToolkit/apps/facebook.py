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

        # Launch the app.
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        return self.app

    def importAll(self):
        """
        Import all contacts after enabling fb via Contacts Settings.
        """

        # Get the count of friends that will be imported.
        friends_list = self.UTILS.element.getElements(DOM.Facebook.friends_list, "Facebook 'import friends' list")
        friend_count = len(friends_list)

        # Tap "Select all".
        select_all_btn = self.UTILS.element.getElement(DOM.Facebook.friends_select_all, "'Select all' button")
        self.UTILS.element.simulateClick(select_all_btn)

        # Tap "Import".
        import_all = self.UTILS.element.getElement(DOM.Facebook.friends_import, "Import button")
        self.UTILS.element.simulateClick(import_all)

        # Switch back to the contacts frame.
        #
        # (The 'importing ..' splash screen that appears confuses the frame switch
        # so the simplest thing is to just wait for a long time to make sure it's
        # gone.)
        time.sleep(5)
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        return friend_count

    def link_contact(self, contact_email):
        """
        After clicking the link contact button, use this to click on a contact.
        """

        # (For some reason this only works if I get all matching elements regardless of visibility,
        # THEN check for visibility. There must be a matching element that never becomes visible.)
        fb_link_list = self.UTILS.element.getElements(DOM.Facebook.link_friends_list, "Facebook 'link friends' list", True, 20)
    
        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult('info', "Screenshot", screenshot)
    
        found = False
        for link in fb_link_list:
            # if link.is_displayed():
            # Keep the name and email details for this contact.
            this_contact = link.find_elements("css selector", "p")[1]
            if this_contact.text == contact_email:
                found = True
                parent = self.UTILS.element.getParent(link)
                self.UTILS.reporting.logResult('info', "Trying to tap the li")
                # self.UTILS.element.simulateClick(parent)
                self.marionette.execute_script(""" arguments[0].click(); """, script_args=[parent])
                break

        self.UTILS.test.test(found, "Desired link contact's email address is displayed.")

        if found:
            self.UTILS.reporting.logComment("Linked FB contact email: " + contact_email + ".")

        # Switch back and wait for contact details page to re-appear.
        time.sleep(2)
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

    def login(self, user, passwd):
        """
        Log into facebook (and navigate to the facebook login frame ... sometimes!!).
        """
        self.UTILS.iframe.switchToFrame(*DOM.Facebook.import_frame)

        user_field = self.UTILS.element.getElement(DOM.Facebook.email, "User field", True, 60)
        user_field.clear()
        user_field.send_keys(user)

        passwd_field = self.UTILS.element.getElement(DOM.Facebook.password, "Password field")
        passwd_field.clear()
        passwd_field.send_keys(passwd)

        login_btn = self.UTILS.element.getElement(DOM.Facebook.login_button, "Login button")
        login_btn.tap()
