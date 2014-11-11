#!/usr/bin/python2.7
#
# Script to check an element definition works.
#
# Takes the following parameters:
#
# 1. element identifier type.
# 2. element identifier value.
# 3. iframe identifier type (optional)
# 4. iframe identifier value (optional)
# 5. child iframe identifier type ... etc... (optional)
#
# If you need to reach an iframe within another iframe, you can just specify the next frame too:
#
#     check_element.py <element def> <iframe def> <child iframe def> <child iframe def> ...
# 
# For example:
#
#    One iframe deep - contacts application:
#    ---------------------------------------
#    ./DEBUG_get_element.py \
#                     "id" "ok-button" \                                                <-- element
#                     "src" "app://communications.gaiamobile.org/contacts/index.html"   <-- iframe
#
#    Two iframes deep - facebook app from contacts application (for linking contacts):
#    ---------------------------------------------------------------------------------
#    ./DEBUG_get_element.py \
#                     "id" "ok-button" \                                                <-- element
#                     "src" "app://communications.gaiamobile.org/contacts/index.html" \ <-- iframe
#                     "id"  "fb-extensions"                                             <-- child iframe
#
#    No iframes - just using the top-level "()" frame:
#    --------------------------------------------------
#    ./DEBUG_get_element.py "id" "ok-button"                                            <-- element
#
import base64, sys, os
from marionette import Marionette

class current_frame():

    def main(self, LOGDIR, p_el, p_frame_array=False):
        #
        # p_el is an array for the element.
        # p_frame_array is a list of iframes to iterate through (optional).
        #
        self.marionette = Marionette(host='localhost', port=2828)  
        self.marionette.start_session()
        self.marionette.set_search_timeout(1000)

        #
        # Switch to the correct iframe (unless it's "()").
        #
        self.marionette.switch_to_frame()

        first_iframe = True
        for x in p_frame_array:
            # (just to make it look nice ;)
            typ_str = "'" + x[0] + "'"

            if first_iframe:
                first_iframe = False
                print ""
                print "Switching to iframe with " + typ_str.rjust(10) + " = '" + x[1] + "'"
            else:
                print "... then to iframe with  " + typ_str.rjust(10) + " = '" + x[1] + "'"

            my_iframe = self.marionette.find_element("xpath", "//iframe[@" + x[0] + "='" + x[1] + "']")
            self.marionette.switch_to_frame(my_iframe)

        if first_iframe:
            print ""
            print "Using 'top level' iframe () ..."

        #
        # Grab a screenshot and html dump of this frame.
        #
        p_sfnam = LOGDIR + "screenshot.png"
        p_hfnam = LOGDIR + "html_dump.html"
        print ""
        print "Screenshot of this frame saved to: " + p_sfnam
        screenshot = self.marionette.screenshot()[22:]
        with open(p_sfnam, 'w') as f:
            f.write(base64.decodestring(screenshot))
        f.close()

        print "HTML dump of this frame saved to : " + p_hfnam
        f = open(p_hfnam, 'w')
        f.write(self.marionette.page_source.encode('ascii', 'ignore') )
        f.close()

        #
        # Test to see if the element is present / displayed / etc...
        #
        print ""
        print "Checking for element: " + str(p_el)
        b_present   = False
        b_displayed = False
        b_enabled   = False
        try:
            x = self.marionette.find_element(*p_el)
            if x:
                b_present = True

                if x.is_displayed():
                    b_displayed = True
    
                if x.is_enabled():
                    b_enabled = True
        except:
            pass

        print ""
        print "Present  : " + str(b_present)
        print "Displayed: " + str(b_displayed)
        print "Enabled  : " + str(b_enabled)
        print ""

#########################################
#
# Staring point.
#

# Make sure we're connected to the device.
os.system(". $HOME/.OWD_TEST_TOOLKIT_LOCATION; $OWD_TEST_TOOLKIT_BIN/connect_device.sh")

# Set up the parameters.
p_el     = (sys.argv[1], sys.argv[2])
i        = 3
p_iframe = []
while i:
    try:
        p_iframe.append( (sys.argv[i], sys.argv[i+1]) )
        i      = i + 2
    except:
        break

# Set up the dir.
LOGDIR  = "/tmp/tests/current_screen/"
os.system("mkdir -p " + LOGDIR + " 2> /dev/null")
os.system("rm " + LOGDIR + "* 2> /dev/null")

# Do it!
current_frame().main(LOGDIR, p_el, p_iframe)

