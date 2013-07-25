from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def _complete_addNumberToContact(self, p_num, p_name):
        #
        # PRIVATE function - finishes the process of adding a number to an existing contact
        # (used bu addThisNumberToContact() etc...).<br>
        # Handles switching frames etc... and finishes with you back in the dialer.
        #
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.waitForElements( ("xpath", "//h1[text()='Select contact']"), "'Select contact' header")
        
        y = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "All contacts list")
        boolOK = False
        for i in y:
            if p_name in i.text:
                self.UTILS.logResult("info", "Contact '%s' found in all contacts." % p_num)
                i.tap()
                boolOK = True
                break
            
        self.UTILS.TEST(boolOK, "Succesfully selected contact from list.")
        self.UTILS.waitForElements(DOM.Contacts.edit_contact_header, "'Edit contact' header")

        # Test for an input field for number_<x> contaiing our number.
        self.UTILS.waitForElements( ("xpath", DOM.Contacts.phone_field_xpath % p_num),
                                    "Phone field contaiing %s" % p_num)
        
        #
        # Hit 'update' to save the changes to this contact.
        #
        done_button = self.UTILS.getElement(DOM.Contacts.edit_update_button, "'Update' button")
        done_button.tap()
 
        #
        # Verify that the contacts app is closed and we are returned to the call log.
        #
        self.marionette.switch_to_frame()
        self.UTILS.waitForNotElements( ("xpath", "//iframe[contains(@%s, '%s')]" % \
                                                (DOM.Contacts.frame_locator[0], DOM.Contacts.frame_locator[1])),
                                        "COntacts frame")
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)
