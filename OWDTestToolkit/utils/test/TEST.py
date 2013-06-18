from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def TEST(self, p_result, p_msg, p_stop = False):
        #
        # Test that p_result is true.
        #
        # One advantage of this over the standard 'assert's is that
        # this continues past a failure if p_stop is False.
        # However, it also takes a screenshot and dumps the html source
        # if p_result is False.
        #
        fnam = False
        if not p_result:
            fnam = self.screenShotOnErr()
            self.logResult(p_result, p_msg, fnam)

            if p_stop:
                self.quitTest()
        else:
            self.logResult(p_result, p_msg)
        

