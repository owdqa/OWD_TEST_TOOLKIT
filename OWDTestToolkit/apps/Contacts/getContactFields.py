from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def getContactFields(self, p_view=False):
        #
        # Return 3-d array of contact details.
        # if p_view is set, it will use the DOM specs for the view screen. Otherwise
        # it will assume you are in the edit screen.
        #
        if p_view:
            return {
            'name'      : self.UTILS.getElement(DOM.Contacts.view_details_title, "Name in title field", True, 5, False),
            'tel'       : self.UTILS.getElement(DOM.Contacts.view_contact_tel_field, "Phone number field", True, 5, False),
            'email'     : self.UTILS.getElement(DOM.Contacts.view_contact_email_field, "Email field", True, 5, False),
            'address'   : self.UTILS.getElement(DOM.Contacts.view_contact_address, "Address field", True, 5, False),
            }
        else:
            return {
            'givenName' : self.UTILS.getElement(DOM.Contacts.given_name_field, "Given name field", True, 5, False),
            'familyName': self.UTILS.getElement(DOM.Contacts.family_name_field, "Family name field", True, 5, False),
            'tel'       : self.UTILS.getElement(DOM.Contacts.phone_field, "Phone number field", True, 5, False),
            'email'     : self.UTILS.getElement(DOM.Contacts.email_field, "Email field", True, 5, False),
            'street'    : self.UTILS.getElement(DOM.Contacts.street_field, "Street field", True, 5, False),
            'zip'       : self.UTILS.getElement(DOM.Contacts.zip_code_field, "Zip code field", True, 5, False),
            'city'      : self.UTILS.getElement(DOM.Contacts.city_field, "City field", True, 5, False),
            'country'   : self.UTILS.getElement(DOM.Contacts.country_field, "Country field", True, 5, False),
            }