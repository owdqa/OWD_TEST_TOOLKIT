from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def trayCounterValue(self):
        #
        # Returns the tray counter value (filtering weird characters out).
        # Assumes we are in the main browser iframe.
        #
        x = self.UTILS.getElement(DOM.Browser.tab_tray_counter, "Tab tray counter")
        return x.text.encode('ascii', 'ignore') #(contains weird characters)

