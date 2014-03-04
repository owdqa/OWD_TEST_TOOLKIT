from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def openThread(self, p_num):
        #
        # Opens the thread for this number (assumes we're looking at the
        # threads in the messaging screen).
        #
        try:
            thread_el = ("xpath", DOM.Messages.thread_selector_xpath.format(p_num))
            x = self.UTILS.getElement(thread_el,"Message thread for " + p_num)
            
            x.tap()
            
            self.UTILS.waitForElements(DOM.Messages.send_message_button, "'Send' button")
        except:
        	x = self.UTILS.screenShotOnErr()
        	self.UTILS.logResult("info", "<b>NOTE:</b> The thread <i>may</i> have failed to open.", x)
        	
