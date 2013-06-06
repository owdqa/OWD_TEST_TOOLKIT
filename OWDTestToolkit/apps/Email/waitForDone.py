from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def waitForDone(self):
        #
        # Wait until any progress icon goes away.
        #
        self.UTILS.waitForNotElements(('tag name', 'progress'), "Progress icon", True, 60);
        time.sleep(2) # (just to be sure!)

