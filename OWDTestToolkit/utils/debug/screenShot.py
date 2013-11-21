from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def screenShot(self, p_fileSuffix):
        #
        # Take a screenshot.
        #
        outFile = os.environ['RESULT_DIR'] + "/" + p_fileSuffix + ".png"
        
        try:
            screenshot = self.marionette.screenshot()
            with open(outFile, 'w') as f:
                f.write(base64.decodestring(screenshot))        
            return outFile
        except:
            return "(Unable to capture screenshot: possible Marionette issue.)"

