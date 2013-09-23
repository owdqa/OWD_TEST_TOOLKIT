from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def trayCounterValue(self):
        #
        # Returns the tray counter value (filtering weird characters out).
        # Assumes we are in the main browser iframe.<br>
        # <b>NOTE: </b> The value returned from this is a <i>string</i>, not an <i>int</i>.
        #
        x = self.UTILS.getElement(DOM.Browser.tab_tray_counter, "Tab tray counter")
        y = x.text.encode('ascii', 'ignore').strip()
        z = ""
        for i in y:
            if i in "0123456789":
                z = z + i

        return z

