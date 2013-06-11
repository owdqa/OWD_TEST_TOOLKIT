from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def threadType(self):
        #
        # Returns the 'type' being used by this thread.
        #
        x = self.UTILS.getElement(DOM.Messages.type_and_carrier_field, "Type and carrier information")
        return x.text.split("|")[0].strip()
        
