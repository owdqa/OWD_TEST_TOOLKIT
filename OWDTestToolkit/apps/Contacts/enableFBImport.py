from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def enableFBImport(self):
        #
        # Enable fb import.
        #
        x = self.UTILS.getElement(DOM.Contacts.settings_fb_enable, "Enable facebook button")
        x.tap()
        time.sleep(1)

        #
        # Were we already connected to facebook?
        #
        boolFound = False
        try:
            self.parent.wait_for_element_displayed('xpath', "//button[text()='Remove']", timeout=5)
            boolFound = True
        except:
            pass
        
        if boolFound:
            self.UTILS.logResult("info", "Logging out of facebook so I can re-enable the FB import ...")
            x = self.UTILS.getElement(('xpath', "//button[text()='Remove']"), "Remove button")
            x.tap()
            
            self.UTILS.waitForElements(DOM.Contacts.settings_fb_logout_wait, "FB logout message", True, 5)
            self.UTILS.waitForNotElements(DOM.Contacts.settings_fb_logout_wait, "FB logout message", True, 60)
            
            self.marionette.switch_to_frame()
            self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

            #
            # Now relaunch and click the 'enable facebook' button again.
            #
            # For some reason I need to relaunch the Contacts app first.
            # If I don't then after I log in again the 'Please hold on ...'
            # message stays forever.
            # (This is only a problem when automating - if you do this
            # manually it works fine.)
            #
            self.launch()
            self.tapSettingsButton()

            self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

            x = self.UTILS.getElement(DOM.Contacts.settings_fb_enable, "Enable facebook button")
            x.tap()

        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

        time.sleep(2) # Just to be sure!

