from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def getContactFields(self):
        #
        # Return 3-d array of contact details (from view or edit contacts screen
        # - the identifiers should be the same ... *should* ...)
        #
        
        return {
        'givenName' : self.UTILS.getElement(DOM.Contacts.given_name_field, "Given name field", True, 5, False),
        'familyName': self.UTILS.getElement(DOM.Contacts.family_name_field, "Family name field", True, 5, False),
        'tel'       : self.UTILS.getElement(DOM.Contacts.phone_field, "Phone number field", True, 5, False),
        'email'     : self.UTILS.getElement(DOM.Contacts.email_field, "Email field", True, 5, False),
        'street'    : self.UTILS.getElement(DOM.Contacts.street_field, "Street field", True, 5, False),
        'zip'       : self.UTILS.getElement(DOM.Contacts.zip_code_field, "Zip code field", True, 5, False),
        'city'      : self.UTILS.getElement(DOM.Contacts.city_field, "City field", True, 5, False),
        'country'   : self.UTILS.getElement(DOM.Contacts.country_field, "Country field", True, 5, False),
        'comment'   : self.UTILS.getElement(DOM.Contacts.comment_field, "Comment field", True, 5, False)
        }
        
