from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def import_MemoryCard(self):
        #
        # Presses the Settings button, then Gmail, then logs in using
        # p_name and p_pass (to begin the process of importing contacts).
        # <br>
        # If p_clickSignIn is set to True then this method will also click
        # the Sign in button (defaults to true).
        # <br>
        # Returns False if the login failed, else True.
        #
        

        x = self.UTILS.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()

        
        x = self.UTILS.getElement(DOM.Contacts.import_contacts, "Import button")
        x.tap()

        time.sleep(1)

        #
        # Press the MemoryCard button.
        #
        x = self.UTILS.getElement(DOM.Contacts.memorycard_button, "Import button")
        
        self.UTILS.TEST(x.get_attribute("disabled") == "false", "Memory Card button is enabled.")
        
        
        x = self.UTILS.getElement(DOM.Contacts.memorycard_button, "Import button")
        x.tap()