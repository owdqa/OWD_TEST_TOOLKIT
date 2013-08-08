from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def waitForReceivedMsgInThisThread(self, p_timeOut=30):
        #
        # Waits for the last message in this thread to be a 'received' message
        # and returns the element for this message.
        #
        pollTime=2
        pollReps=(p_timeOut / pollTime)
        lastEl  = False
        for i in range(1,pollReps):
            # Get last message in this thread.
            x = self.lastMessageInThisThread()
            
            # Is this a received message?
            if "incoming" in x.get_attribute("class"):
                # Yep.
                lastEl = x
                break
            
            # Nope - sleep then try again.
            time.sleep(pollTime)
            
        self.UTILS.TEST(lastEl,
                        "Last message in thread is a 'received' message within " + str(p_timeOut) + " seconds.")
        return lastEl
            
    
