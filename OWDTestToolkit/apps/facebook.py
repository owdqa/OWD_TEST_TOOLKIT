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

        """Switch back to the contacts frame.
        The 'importing ..' splash screen that appears confuses the frame switch
        so the simplest thing is to just wait for a long time to make sure it's
        gone.
        """
        time.sleep(5)
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        return friend_count

    def link_contact(self, contact_email):
        contact = self.UTILS.element.getElement(('xpath', DOM.Facebook.friend_link_path.format(contact_email)),
                                                "Searching contact")
        self.UTILS.element.simulateClick(contact)
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
