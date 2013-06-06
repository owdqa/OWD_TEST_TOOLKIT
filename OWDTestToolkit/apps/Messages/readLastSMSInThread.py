from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def readLastSMSInThread(self):
        #
        # Read last message in the current thread.
        #
        received_message = self.UTILS.getElements(DOM.Messages.received_messages, "Received messages")[-1]
        return str(received_message.text)

