from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def import_ImportAll(self):
        #
        # Assumes you're already in the gmail import screen (after logging in etc...).
        #
        self.UTILS.logResult("info", "Tapping the 'Select All' button ...")
        self.marionette.execute_script("document.getElementById('%s').click()" % DOM.Contacts.import_select_all[1])
        time.sleep(1)
        
        self.marionette.execute_script("document.getElementById('%s').click()" % DOM.Contacts.import_import_btn[1])
        time.sleep(1)

        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        
