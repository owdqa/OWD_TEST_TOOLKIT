from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def addAnotherEmailAddress(self, p_email_address):
        #
        # Add a new email address to the contact currnetly being viewed in Edit mode.
        #
        x = self.UTILS.getElement(DOM.Contacts.add_email_button, "Add email button")
        x.tap()
        
        # (Marionette currently messes up the screen, so correct this.)
        self.marionette.execute_script("document.getElementsByTagName('h1')[0].scrollIntoView();")
        
        #
        # Add the email.
        #
        x = self.UTILS.getElements(DOM.Contacts.email_fields, "Email fields", False, 2)
        for i in x:
            if i.get_attribute("value") == "":
                i.send_keys(p_email_address)
                
                # (if there's a "_" in the email address, the screen will lock.)
                if "_" in p_email_address:
                    orig_frame = self.UTILS.currentIframe()
                    self.lockscreen.unlock()
                    self.marionette.switch_to_frame()
                    self.UTILS.switchToFrame("src", orig_frame)

                break
            