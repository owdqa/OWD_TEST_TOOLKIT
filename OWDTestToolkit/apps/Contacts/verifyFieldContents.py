from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def _viewTest(self, desc, str1, str2):
        self.UTILS.TEST(str1 in str2, "%s field contains '%s' (it was '%s')." % (desc, str1, str2))

    def verifyFieldContents(self, p_contact_json_obj, p_view=False):
        #
        # Verify the contents of the contact fields in this screen (assumes
        # you are in the correct screen since this could be view or edit).
        # <br><br>
        # <b>p_contact_json_obj</b> must be an object in the same format as the
        # one in ./example/tests/mock_data/contacts.py.<br>
        # <b>p_view</b> selects whether this is the 'view contact' screen or not (defaults to False -> edit screen).
        #
        contFields = self.getContactFields(p_view) 
        
        if p_view:
            self._viewTest("Name"       , p_contact_json_obj['name']                , contFields['name'   ].text)
            self._viewTest("Telephone"  , p_contact_json_obj['tel']['value']        , contFields['tel'    ].text)
            self._viewTest("Email"      , p_contact_json_obj['email']['value']      , contFields['email'  ].text)
            self._viewTest("Comment"    , p_contact_json_obj['comment']             , contFields['comment'].text)
            self._viewTest("Street"     , p_contact_json_obj['adr']['streetAddress'], contFields['address'].text)
            self._viewTest("Post code"  , p_contact_json_obj['adr']['postalCode']   , contFields['address'].text)
            self._viewTest("Locality"   , p_contact_json_obj['adr']['locality']     , contFields['address'].text)
            self._viewTest("Country"    , p_contact_json_obj['adr']['countryName']  , contFields['address'].text)

        else:
            self.checkMatch(contFields['givenName' ] , p_contact_json_obj['givenName']            , "Given name")
            self.checkMatch(contFields['familyName'] , p_contact_json_obj['familyName']           , "Family name")
            self.checkMatch(contFields['tel'       ] , p_contact_json_obj['tel']['value']         , "Telephone")
            self.checkMatch(contFields['email'     ] , p_contact_json_obj['email']['value']       , "Email")
            self.checkMatch(contFields['street'    ] , p_contact_json_obj['adr']['streetAddress'] , "Street")
            self.checkMatch(contFields['zip'       ] , p_contact_json_obj['adr']['postalCode']    , "Zip")
            self.checkMatch(contFields['city'      ] , p_contact_json_obj['adr']['locality']      , "City")
            self.checkMatch(contFields['country'   ] , p_contact_json_obj['adr']['countryName']   , "Country")
            self.checkMatch(contFields['comment'   ] , p_contact_json_obj['comment']              , "COMMENTS")

