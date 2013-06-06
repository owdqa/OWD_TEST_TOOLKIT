from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def countMessagesInThisThread(self):
        #
        # Returns the number of messages in this thread
        # (assumes you're already in the thread).
        #
        x = self.UTILS.getElements(DOM.Messages.thread_messages,"Messages")
        x = len(x)
        
        return x


