from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def switchToFacebook(self):
        #
        # <i>Private</i> function to handle the iframe hop-scotch involved in 
        # finding the facebook app launched via contacts app.
        #
        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)        
        self.UTILS.switchToFrame(*DOM.Contacts.settings_fb_frame)        

        #
        # Wait for the fb page to start.
        #
        self.UTILS.waitForElements(DOM.Facebook.friends_header, "Facebook friends header")
        time.sleep(2)

