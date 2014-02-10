from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def export_Bluetooth(self):
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
        # Press the Bluetooth.
        #
        x = self.UTILS.getElement(DOM.Contacts.export_bluetooth, "Export Bluetooth")
        self.UTILS.TEST(x.get_attribute("disabled") == "false", "Bluetooth button is enabled.")
        
        x.tap()
        time.sleep(2)