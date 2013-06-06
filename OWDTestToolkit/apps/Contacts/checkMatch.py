from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def checkMatch(self, p_el, p_val, p_name):
        #
        # Test for a match between an element and a string
        # (found I was doing this rather a lot so it's better in a function).
        #
        test_str = str(p_el.get_attribute("value"))

        self.UTILS.TEST(
            (test_str == p_val),
            p_name + " = \"" + p_val + "\" (it was \"" + test_str + "\")."
            )

