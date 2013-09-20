from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def trayCounterIs(self, p_num):
        #
        # Compares p_num to the tray counter and returns True or False.
        # Assumes we are in the main browser iframe.
        #
        x = self.UTILS.getElement(DOM.Browser.tab_tray_counter, "Tab tray counter")
        _counter = x.text.encode('ascii', 'ignore') #(contains weird characters)
        return _counter == str(p_num)

