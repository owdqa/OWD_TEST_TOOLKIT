from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def export_SDcard(self):
        #
        # Presses the Settings button, then memory card
        #

        x = self.UTILS.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()

        time.sleep(1)
        
        x = self.UTILS.getElement(DOM.Contacts.export_contacts, "Export button")
        x.tap()
        time.sleep(1)

        #
        # Press the SD Card.
        #
        x = self.UTILS.getElement(DOM.Contacts.export_sd_card, "Export SD Card")
        self.UTILS.TEST(x.get_attribute("disabled") == "false", "SD card button is enabled.")
        
        x.tap()
        time.sleep(2)
        
        

        