from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def goSound(self):
        #
        # Go to Sound menu.
        #
        self.launch()
        x = self.UTILS.getElement(DOM.Settings.sound, "Sound setting link")
        x.tap()


