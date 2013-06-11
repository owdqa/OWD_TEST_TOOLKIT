from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def tapSettingsButton(self):
        #
        # Tap the settings button.
        #
        x = self.UTILS.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()
        
        self.UTILS.waitForElements(DOM.Contacts.settings_header, "Settings header")
