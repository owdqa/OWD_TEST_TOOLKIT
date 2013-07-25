from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def goto_folder_from_list(self, p_name):
        #
        # Goto a specific folder in the folder list screen.
        #
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screen shot:", x)
        x = self.UTILS.getElement(('xpath', DOM.Email.folderList_name_xpath % p_name), "Link to folder '" + p_name + "'")
        x.tap()
        
        self.UTILS.waitForElements(("xpath", DOM.GLOBAL.app_head_specific % p_name), "Header for '" + p_name + "' folder")
        
    
