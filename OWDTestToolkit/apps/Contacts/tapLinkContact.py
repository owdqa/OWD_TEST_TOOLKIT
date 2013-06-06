from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def tapLinkContact(self):
        #
        # Press the 'Link contact' button in the view contact details screen.
        #
        
        #
        # NOTE: there is more than one button with this ID, so make sure we use the right one!
        # (One of them isn't visible, so we need to check for visibility this way or the
        # 'invisible' one will cause 'getElements()' to fail the test).
        #
        time.sleep(2)
        x = self.UTILS.getElements(DOM.Contacts.link_button, "Link contact button", False)
        for i in x:
            if i.is_displayed():
                i.tap()
                break
            
        self.switchToFacebook()
        
