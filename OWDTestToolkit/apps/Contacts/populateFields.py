from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def populateFields(self, p_contact_json_obj):
        #
        # Put the contact details into the fields (assumes you are in the correct
        # screen already since this could be create or edit).
        # <br><br>
        # <b>p_contact_json_obj</b> must be an object in the same format as the
        # one in ./example/tests/mock_data/contacts.py.
        #
        contFields = self.getContactFields()
        
        #
        # Put the contact details into each of the fields (this method
        # clears each field first).
        #
        self.replaceStr(contFields['givenName'  ] , p_contact_json_obj["givenName"])
        self.replaceStr(contFields['familyName' ] , p_contact_json_obj["familyName"])
        self.replaceStr(contFields['tel'        ] , p_contact_json_obj["tel"]["value"])
        self.replaceStr(contFields['email'      ] , p_contact_json_obj["email"]["value"])
        self.replaceStr(contFields['street'     ] , p_contact_json_obj["adr"]["streetAddress"])
        self.replaceStr(contFields['zip'        ] , p_contact_json_obj["adr"]["postalCode"])
        self.replaceStr(contFields['city'       ] , p_contact_json_obj["adr"]["locality"])
        self.replaceStr(contFields['country'    ] , p_contact_json_obj["adr"]["countryName"])