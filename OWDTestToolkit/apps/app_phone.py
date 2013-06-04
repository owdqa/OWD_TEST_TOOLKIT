import time
from gaiatest   import GaiaTestCase
from marionette import Marionette
from OWDTestToolkit import *

class AppPhone(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.marionette = p_parent.marionette
        self.UTILS      = p_parent.UTILS



    def launch(self):
        #
        # Launch the app.
        #
        self.apps.kill_all()
        self.app = self.apps.launch('Phone')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Phone app - loading overlay", False);

    def createContactFromThisNum(self):
        #
        # Creates a new contact from this number 
        # (doesn't fill in the contact details).
        #
        
        x = self.UTILS.getElement(DOM.Phone.add_to_contacts_button, "Add to contacts button")
        x.tap()

        x = self.UTILS.getElement(DOM.Phone.create_new_contact_btn, "Create new contact button")
        x.tap()
        
        #
        # Switch to the contacts frame.
        #
        self.marionette.switch_to_frame()
        x = (DOM.Contacts.frame_locator[0],
             DOM.Contacts.frame_locator[1] + "?new")
        self.UTILS.switchToFrame(*x)
        
    def callThisNumber(self):
        #
        # Calls the current number.
        #
        x = self.UTILS.getElement(DOM.Phone.call_number_button, "Call number button")
        x.tap()
        
        time.sleep(2)
        
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Phone.frame_locator_calling)
        self.UTILS.waitForElements(DOM.Phone.outgoing_call_locator, "Outgoing call element")
        
    def hangUp(self):
        #
        # Hangs up (assuming we're in the 'calling' frame).
        #
        x = self.UTILS.getElement(DOM.Phone.hangup_bar_locator, "Hangup bar")
        x.tap()