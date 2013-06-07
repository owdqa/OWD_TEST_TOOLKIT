from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def screenShotOnErr(self):
        #
        # Take a screenshot on error (increments the file number).
        #

        #
        # Build the error filename.
        #
        self.errNum = self.errNum + 1
        fnam = self.testNum + "_err_" + str(self.errNum)
        
        #
        # Record the screenshot.
        #
        screenDump = self.screenShot(fnam)
        
        #
        # Dump the current page's html source too.
        #
        htmlDump = os.environ['RESULT_DIR'] + "/" + fnam + ".html"
        self.savePageHTML(htmlDump)
        return (htmlDump, screenDump)

