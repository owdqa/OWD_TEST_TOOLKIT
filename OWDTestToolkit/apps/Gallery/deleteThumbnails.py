from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def deleteThumbnails(self, p_num_array):
        #
        # Deletes the thumbnails listed in p_num_array
        # (following an index starting at number 0).<br>
        # The list must be numeric, i.e "deleteThumbnails( (0,1,2) )".
        #
        
        #
        # Get the amount of thumbnails we currently have.
        #
        before_thumbcount = self.thumbCount()
        delete_thumbcount = len(p_num_array)
        target_thumbcount = before_thumbcount - delete_thumbcount
        
        #
        # Click the 'select' button.
        #
        x = self.UTILS.getElement(DOM.Gallery.thumbnail_select_mode_btn, "Select button")
        x.tap()
        
        #
        # Report 'the plan'.
        #
        self.UTILS.logResult("info", 
                             "Delete " + str(delete_thumbcount) + " of the " + str(before_thumbcount) + " thumbnails ...")
        
        #
        # Select 3 of them.
        #
        x = self.UTILS.getElements(DOM.Gallery.thumbnail_items, "Thumbnails")
        for i in p_num_array:
            x[i].tap()
            
        #
        # Press the trash icon.
        #
        x = self.UTILS.getElement(DOM.Gallery.thumbnail_trash_icon, "Trash icon")
        x.tap()
        
        #
        # Confirm.
        #
        myIframe = self.UTILS.currentIframe()
        self.marionette.switch_to_frame()
        self.marionette.execute_script("document.getElementById('%s').click()" % DOM.GLOBAL.modal_confirm_ok[1])
        self.UTILS.switchToFrame("src", myIframe)
        
        #
        # Now report how many thumbnails there are (should be 2).
        #
        if target_thumbcount < 1:
            self.UTILS.waitForElements(DOM.Gallery.no_thumbnails_message, 
                                       "Message saying there are no thumbnails", False, 5)
        else:
            #
            # Come out of 'select' mode.
            #
            x = self.UTILS.getElement(DOM.Gallery.thumbnail_cancel_sel_mode_btn, "Exit select mode button")
            x.tap()
            
            x = self.thumbCount()
            self.UTILS.TEST(x == target_thumbcount, 
                            str(target_thumbcount) + " thumbnails after deletion (there were " + str(x) + ").")
