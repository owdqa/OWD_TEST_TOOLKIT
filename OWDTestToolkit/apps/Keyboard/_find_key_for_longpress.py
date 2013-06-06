from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def _find_key_for_longpress(self, input_value):
        for key_to_press, extended_values in self.lookup_table.iteritems():
            if input_value in extended_values:
                return key_to_press

    # trying to switch to right layout
