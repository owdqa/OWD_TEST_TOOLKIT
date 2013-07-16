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
        fnam = self.testNum + "_" + str(self.errNum)
        
        #
        # Record the screenshot.
        #
        screenDump = self.screenShot(fnam)
        
        #
        # Dump the current page's html source too.
        #
        htmlDump = os.environ['RESULT_DIR'] + "/" + fnam + ".html"
        
        try:
            self.savePageHTML(htmlDump)
        except:
            htmlDump = "(Unable to dump html for this page: possible Marionette issue.)"
            
        return (htmlDump, screenDump)

