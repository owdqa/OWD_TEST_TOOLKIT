from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def closeThread(self):
        #
        # Closes the current thread (returns you to the
        # 'thread list' SMS screen).
        #
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        
        self.UTILS.waitForElements(("xpath", "//h1[text()='Messages']"), "Messages main header")
    
