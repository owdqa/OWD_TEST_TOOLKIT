from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def search(self, p_val):
        #
        # Searches the 'all contacts' screen for p_val
        # (assumes we're currently in the 'all contacts' screen).
        #
        
        #
        # Tap the search area.
        #
        x = self.UTILS.getElement(DOM.Contacts.search_field, "Search field")
        # x.tap()
        #
        # Tap method of marionette does not seem to work here. JS solution instead.
        #
        self.marionette.execute_script("""
            arguments[0].click();
        """, script_args=[x])
         
        # problems with this just now - seems to mess up marionette somehow ...
#         self.parent.keyboard.send(p_val)
#         self.marionette.switch_to_frame()
#         self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

#         # ... so using this instead:
#         self.marionette.switch_to_frame()
#         self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
#         x = self.UTILS.getElement(DOM.Contacts.search_contact_input, "Search input")
#         x.send_keys(p_val)

        self.UTILS.typeThis(DOM.Contacts.search_contact_input, "Search input", p_val, 
                            p_no_keyboard=True,
                            p_validate=False,
                            p_clear=False,
                            p_enter=False)

