from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def screenShot(self, p_fileSuffix):
        #
        # Take a screenshot.
        #
        outFile = os.environ['RESULT_DIR'] + "/" + p_fileSuffix + ".png"
        screenshot = self.marionette.screenshot()[22:] 
        with open(outFile, 'w') as f:
            f.write(base64.decodestring(screenshot))        
        return outFile

