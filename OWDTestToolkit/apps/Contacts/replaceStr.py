from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def replaceStr(self, p_field, p_str):
        #
        # Replace text in a field (as opposed to just appending to it).
        #
        p_field.clear()
        p_field.send_keys(p_str)
        
        #
        # Verify this value is now in this field.
        #
        self.UTILS.TEST(p_field.text == p_str, "This field now contains '%s'." % p_str)

