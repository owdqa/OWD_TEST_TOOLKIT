from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def export_SIMcard(self):
        #
        # Presses the Settings button, then memory card
        #

        x = self.UTILS.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()

        time.sleep(1)
        
        x = self.UTILS.getElement(DOM.Contacts.export_contacts, "Export button")
        x.tap()
        time.sleep(2)

        #
        # Press the SIM card.
        #
        x = self.UTILS.getElement(DOM.Contacts.export_sim_card, "Export SIM Card")
        self.UTILS.TEST(x.get_attribute("disabled") == "false", "SIM card button is enabled.")
        
        x.tap()
        time.sleep(2)