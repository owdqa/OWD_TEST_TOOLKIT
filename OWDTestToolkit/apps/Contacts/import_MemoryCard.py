from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def import_MemoryCard(self):
        #
        # Presses the Settings button, then memory card
        #

        x = self.UTILS.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()

        time.sleep(1)
        
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