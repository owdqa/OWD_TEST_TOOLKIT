from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def importAll(self):
        #
        # Import all contacts after enabling fb via Contacts Settings.
        #

        #
        # Get the count of friends that will be imported.
        #
        x = self.UTILS.getElements(DOM.Facebook.friends_list, "Facebook 'import friends' list")
        friend_count = len(x)
        
        #
        # Tap "Select all".
        #
        x = self.UTILS.getElement(DOM.Facebook.friends_select_all, "'Select all' button")
        x.tap()
        
        #
        # Tap "Import".
        #
        x = self.UTILS.getElement(DOM.Facebook.friends_import, "Import button")
        x.tap()
        
        #
        # Switch back to the contacts frame.
        #
        # (The 'importing ..' splash screen that appears confuses the frame switch
        # so the simplest thing is to just wait for a long time to make sure it's
        # gone.)
        #
        time.sleep(5)
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        
        #
        # Return the number of friends we imported.
        #
        return friend_count
    
