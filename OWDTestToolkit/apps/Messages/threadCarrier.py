from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def threadCarrier(self):
        #
        # Returns the 'carrier' being used by this thread.
        #
        x = self.UTILS.getElement(DOM.Messages.type_and_carrier_field, "Type and carrier information")
        return x.text.split("|")[1].strip()
        
