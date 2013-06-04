from global_imports import *
from gaiatest import GaiaTestCase

class main(GaiaTestCase):
    #################################################################################
    #
    # Methods which deal with reporting the results.
    #
    def screenShot(self, p_fileSuffix):
        #
        # Take a screenshot.
        #
        outFile = os.environ['RESULT_DIR'] + "/" + p_fileSuffix + ".png"
        screenshot = self.marionette.screenshot()[22:] 
        with open(outFile, 'w') as f:
            f.write(base64.decodestring(screenshot))        
        return outFile

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

    def savePageHTML(self, p_outfile):
        #
        # Save the HTML of the current page to the specified file.
        #
        f = open(p_outfile, 'w')
        f.write( self.marionette.page_source.encode('ascii', 'ignore') )


