from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def timeOfLastMessageInThread(self):
        #
        # Returns the time of the last message in the current thread.
        #
        time.sleep(2)
        x = self.UTILS.getElements(DOM.Messages.message_timestamps, "Message timestamps")
        return x[-1].text
        
