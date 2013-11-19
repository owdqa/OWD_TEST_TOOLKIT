#!/usr/bin/python2.7
#
# Script to capture screenshots / html and attribute info.
# about all current iframes on a device.
#
import base64, sys, os
from marionette import Marionette

class current_frame():
    
    filename_screenshot = ""
    filename_htmldump   = ""
    
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
        print ""
        print "Iframe for 'top level' () ..."
        self.filename_screenshot = LOGDIR + "top_level" + ".png"
        self.filename_htmldump   = LOGDIR + "top_level" + ".html"
        self.marionette.switch_to_frame()
        self.record_frame()

        frames = self.marionette.find_elements("tag name", "iframe")
        for fnum in range (0, len(frames)):
          
            #
            # App name is usually in the "src" attribute, so it's worth a shot..
            #
            frame_src = frames[fnum].get_attribute("src")
              
            if frame_src != "":
                startpos = frame_src.index('/') + 2
                stoppos  = frame_src.index('.')
                appname  = frame_src[startpos:stoppos]
                filename = appname
            else:
                ucount = ucount + 1
                appname  = "(unknown)"
                filename = "unknown_" + str(ucount)
            
            #
            # Because we call this script sometimes when we hit a Marionette issue,
            # these filenames may already exist (and we'd overwrite them!), so
            # add 'DEBUG_' to the start of the filename.
            #
            filename = "DEBUG_" + filename
                 
            filename_details         = LOGDIR + filename + "_iframe_details.txt"
            self.filename_screenshot = LOGDIR + filename + ".png"
            self.filename_htmldump   = LOGDIR + filename + ".html"
            
            #
            # This iframe gives me problems sometimes, so I'm ignoring it for now.
            #
            if appname == "costcontrol":
                continue
            
            print ""
            print "Iframe for app \"" + appname + "\" ..."
        
            #
            # Record the iframe details (pretty verbose, but 'execute_script' 
            # wasn't letting me use 'for' loops in js for some reason).
            #
            print "    |_ iframe details saved to : " + filename_details
            f = open(filename_details, 'w')
            f.write("Attributes for this iframe ...\n")
            num_attribs = self.marionette.execute_script("return document.getElementsByTagName('iframe')[" + str(fnum) + "].attributes.length;")
            for i in range(0,num_attribs):
                attrib_name  = self.marionette.execute_script("return document.getElementsByTagName('iframe')[" + str(fnum) + "].attributes[" + str(i) + "].nodeName;")
                attrib_value = self.marionette.execute_script("return document.getElementsByTagName('iframe')[" + str(fnum) + "].attributes[" + str(i) + "].nodeValue;")
        
                f.write("    |_ " + attrib_name.ljust(20) + ": \"" + attrib_value + "\"\n")   
            f.close()
            
            #
            # Switch to this frame.
            #
            self.marionette.switch_to_frame(fnum)
                   
            self.record_frame()
         
            self.marionette.switch_to_frame()


    def record_frame(self):
        #
        # Take the screenshot and save it to the file.
        #
        print "    |_ screenshot saved to     : " + self.filename_screenshot
        screenshot = self.marionette.screenshot()[22:]
        #with open(self.filename_screenshot, 'w') as f:
        #    f.write(base64.decodestring(screenshot))
        #f.close()
              
        #
        # Take the html dump and save it to the file.
        #
        print "    |_ html dump saved to      : " + self.filename_htmldump
        f = open(self.filename_htmldump, 'w')
        f.write(self.marionette.page_source.encode('ascii', 'ignore') )
        f.close()


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

