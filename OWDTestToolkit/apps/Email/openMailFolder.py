from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def openMailFolder(self, p_folderName):
        #
        # Open a specific mail folder (must be called from "Inbox").
        #
        x = self.UTILS.getElement(DOM.Email.settings_menu_btn, "Settings menu button")        
        x.tap()        
        
        #
        # When we're looking at the folders screen ...
        #
        self.UTILS.waitForElements(DOM.Email.folderList_header, "Folder list header", True, 20, False)
        
        #
        # ... click on the folder were after.
        #
        self.goto_folder_from_list(p_folderName)
        
        #
        # Wait a while for everything to finish populating.
        #
        self.UTILS.waitForNotElements(DOM.Email.folder_sync_spinner,
                                       "Loading messages spinner", True, 60, False)
        
