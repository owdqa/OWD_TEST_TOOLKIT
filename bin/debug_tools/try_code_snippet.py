#!/usr/bin/python2.7
#
# Script to test a code snippet against the current state of the device
# (saves you having to run through the test each time to get the device
# into the correct state to test your code).
#
# Takes one MANDATORY parameter:
#
# 1. the name of your code snippet file (just a ".py" python script, including
#    the path), containing just something like this for example:
#
#    x = self.marionette.find_element('id', 'settings-button')
#    x.tap()
#
#
# (it will inherit everything from here automatically, such as "self.marionette" etc...)
#
# ... and the following OPTIONAL parameters:
#
# 1. iframe identifier type
# 2. iframe identifier value
# 3. ... repeat for child iframes ...
#
# If you need to reach an iframe within another iframe, you can just specify the next frame too:
#
#     check_element.py <snippet file> <iframe def> <child iframe def> <child iframe def> ...
# 
# For example:
#
#    One iframe deep - contacts application:
#    ---------------------------------------
#    ./DEBUG_try_code_snippet.py \
#                     "/tmp/snippet.py" \                                               <-- snippet file
#                     "src" "app://communications.gaiamobile.org/contacts/index.html"   <-- iframe
#
#    Two iframes deep - facebook app from contacts application (for linking contacts):
#    ---------------------------------------------------------------------------------
#    ./DEBUG_try_code_snippet.py \
#                     "/tmp/snippet.py" \                                               <-- snippet file
#                     "src" "app://communications.gaiamobile.org/contacts/index.html" \ <-- iframe
#                     "id"  "fb-extensions"                                             <-- child iframe
#
#    No iframes - just using the top-level "()" frame:
#    --------------------------------------------------
#    ./DEBUG_try_code_snippet.py "/tmp/snippet.py"                                      <-- snippet file
#
import base64, sys, os
from marionette import Marionette
from marionette import Actions

class current_frame():
    
    def main(self, p_snippet, p_frame_array=False):
        #
        # p_el is an array for the element.
        # p_frame_array is a list of iframes to iterate through (optional).
        #
        self.marionette = Marionette(host='localhost', port=2828)  
        self.marionette.start_session()
        self.marionette.set_search_timeout(1000)
        self.actions    = Actions(self.marionette)
        
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
            
        
        # Run the code snippet.
        print ""
        print "Running code snippet from this location ..."
        print ""
        execfile(p_snippet)

#########################################
#
# Staring point.
#

# Make sure we're connected to the device.
os.system(". $HOME/.OWD_TEST_TOOLKIT_LOCATION; $OWD_TEST_TOOLKIT_BIN/connect_device.sh")


# Set up the parameters.
p_snippet= sys.argv[1]
i        = 2
p_iframe = []
while i:
    try:
        p_iframe.append( (sys.argv[i], sys.argv[i+1]) )
        i      = i + 2
    except:
        break

# Switch to the relevant frame and run the snippet.
current_frame().main(p_snippet, p_iframe)

