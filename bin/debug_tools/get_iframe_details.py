#!/usr/bin/python2.7
#
# Script to capture screenshots / html and attribute info.
# about all current iframes on a device.
#
import base64, sys, os, time
from marionette import Marionette

class current_frame():
    
    filename_screenshot = ""
    filename_htmldump   = ""
    LOGDIR              = ""
    
    errNum      = 0
    _framepath  = []
    _MAXLOOPS   = 20
    _old_src    = ""
    
    def main(self, LOGDIR):
        #
        # The first variable is the log directory.
        #
        ucount  = 0
        self.marionette = Marionette(host='localhost', port=2828)  
        self.marionette.start_session()
        self.marionette.set_search_timeout(1000)
        
        #
        # Now loop through all the iframes, gathering details about each one.
        #
        self.LOGDIR = LOGDIR
        self.viewAllIframes()



    def viewAllIframes(self):
        #
        # Dumps details of all iframes (recursively) into the run log.
        #
        
        # Just in case we end up in an endless loop ...
        self._MAXLOOPS = self._MAXLOOPS - 1
        if self._MAXLOOPS < 0: return
        
        #
        # Climb up from 'root level' iframe to the starting position ...
        #
        srcSTR=""
        self.marionette.switch_to_frame()
        time.sleep(0.5)
        frame_dets = "<i>(unknown)</i>"
        if len(self._framepath) > 0:
            for i in self._framepath:
                
                if i == self._framepath[-1]:
                    # We're at the target iframe - record its "src" value.
                    new_src = self.marionette.find_elements("tag name", "iframe")[int(i)].get_attribute("src")
                    
                    if new_src != "" and new_src == self._old_src:
                        # This is an endless loop (some iframes seem to do this) - ignore it and move on.
                        return

                    self._old_src   = new_src
                    new_src         = new_src if len(new_src) > 0 else "<i>(nothing)</i>"
                    srcSTR          = "value of 'src'      = \"%s\"" % new_src
                    
                self.marionette.switch_to_frame(int(i))
            
        self.screenShotOnErr()

        #
        # Do the same for all iframes in this iframe 
        #
        ignoreme = -1
        x = self.marionette.find_elements("tag name", "iframe")
        
        if len(x) > 0:
                
            for i2 in range(0, len(x)):                 
                # Add this iframe number to the array.
                self._framepath.extend(str(i2))
                 
                # Process this iframe.
                self.viewAllIframes()
                 
                # Remove this iframe number from the array.
                del self._framepath[-1]
                
    def _framePathStr(self):
        #
        # Private method to return the iframe path in a 'nice' format.
        #
        pathStr = "<i>(root level)</i><b>"
        for i in self._framepath:
            pathStr = "%s -> %s" % (pathStr, i)
            
        return pathStr + "</b>"
                

    def screenShot(self, p_fileSuffix):
        #
        # Take a screenshot.
        #
        outFile = "%s/DEBUG_%s.png" % (self.LOGDIR,p_fileSuffix)
        
        try:
            screenshot = self.marionette.screenshot()[22:] 
            with open(outFile, 'w') as f:
                f.write(base64.decodestring(screenshot))        
            return outFile
        except:
            return "(Unable to capture screenshot: possible Marionette issue.)"


    def savePageHTML(self, p_fileSuffix):
        #
        # Save the HTML of the current page to the specified file.
        #
        outFile = "%s/DEBUG_%s.html" % (self.LOGDIR, p_fileSuffix)
        f = open(outFile, 'w')
        f.write( self.marionette.page_source.encode('ascii', 'ignore') )



    def screenShotOnErr(self):
        #
        # Take a screenshot on error (increments the file number).
        #

        #
        # Build the error filename.
        #
        self.errNum = self.errNum + 1
        
        #
        # Record the screenshot.
        #
        screenDump = self.screenShot(self.errNum)
        
        #
        # Dump the current page's html source too.
        #
        self.savePageHTML(self.errNum)
            



#########################################
#
# Staring point.
#

# Make sure we're connected to the device.
os.system(". $HOME/.OWD_TEST_TOOLKIT_LOCATION; $OWD_TEST_TOOLKIT_BIN/connect_device.sh")

# Set up the dir.
LOGDIR = False
try:
    LOGDIR = sys.argv[1] + "/"
except:
    pass

if not LOGDIR:
    LOGDIR  = "/tmp/tests/current_screen/"
    os.system("mkdir -p " + LOGDIR + " > /dev/null")
    os.system("rm " + LOGDIR + "* > /dev/null 2>&1")

# Do it!
current_frame().main(LOGDIR)

