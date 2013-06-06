from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def waitForThumbnails(self, p_count, p_failOnErr=False):
        #
        # Waits until p_count thumbnails are present
        # (because it can take a few seconds).
        # Since there could be a bug in the Gallery app
        # which prevents this, there is a 10s timeout.
        #
        x = 0
        y = 0
        boolOK = True
        while x < p_count:
            time.sleep(1)
            x = self.thumbCount()
            
            # Added a timeout of 10s in case the gallery app has a bug.
            y = y + 1
            if y > 10:
                boolOK = False
                break
        self.UTILS.TEST(boolOK, str(p_count) + " thumbnails appear in under 10s (" + str(x) + " found).", p_failOnErr)
        
        return boolOK

