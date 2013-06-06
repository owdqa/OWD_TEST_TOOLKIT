from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def pressDeleteContactButton(self):
        #
        # In it's own function just to save time figuring out
        # that you have to get the button into view before you
        # can press it, then re-align the screen again.
        #
        self.marionette.execute_script("document.getElementById('" + \
                                       DOM.Contacts.delete_contact_btn[1] + \
                                       "').scrollIntoView();")
        self.marionette.execute_script("document.getElementById('settings-button').scrollIntoView();")
        x = self.UTILS.getElement(DOM.Contacts.delete_contact_btn, "Delete contacts button", False) 
        x.tap()

