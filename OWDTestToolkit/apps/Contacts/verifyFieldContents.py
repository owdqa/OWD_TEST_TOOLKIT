from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def verifyFieldContents(self, p_contact_json_obj):
        #
        # Verify the contents of the contact fields in this screen (assumes
        # you are in the correct screen since this could be view or edit).
        # <br><br>
        # <b>p_contact_json_obj</b> must be an object in the same format as the
        # one in ./example/tests/mock_data/contacts.py.
        #
        contFields = self.getContactFields()      # Get the contact's fields again.
        
        self.checkMatch(contFields['givenName' ] , p_contact_json_obj['givenName']            , "Given name")
        self.checkMatch(contFields['familyName'] , p_contact_json_obj['familyName']           , "Family name")
        self.checkMatch(contFields['tel'       ] , p_contact_json_obj['tel']['value']         , "Telephone")
        self.checkMatch(contFields['email'     ] , p_contact_json_obj['email']['value']       , "Email")
        self.checkMatch(contFields['street'    ] , p_contact_json_obj['adr']['streetAddress'] , "Street")
        self.checkMatch(contFields['zip'       ] , p_contact_json_obj['adr']['postalCode']    , "Zip")
        self.checkMatch(contFields['city'      ] , p_contact_json_obj['adr']['locality']      , "City")
        self.checkMatch(contFields['country'   ] , p_contact_json_obj['adr']['countryName']   , "Country")
        self.checkMatch(contFields['comment'   ] , p_contact_json_obj['comment']              , "COMMENTS")

