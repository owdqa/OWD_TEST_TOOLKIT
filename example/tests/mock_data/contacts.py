class MockContacts(dict):
    #
    # The key values here match the data structure in the contacts db
    # so that the json output of this mock can be inserted directly 
    # into the device's db.
    #
    def __init__(self):
        self.Contact_1 = {
                "givenName" : "John",
                "familyName": "Smith",
                "name"      : "John Smith",
                "email"     : {"type": "", "value": "john.smith@nowhere.com"},
                "tel"       : {"type": "Mobile", "value": "111111111"},
                "adr"       : {"streetAddress"    : "One Street",
                               "postalCode"       : "00001",
                               "locality"      : "City One",
                               "countryName"   : "Country One"},
                "bday"      : "1981-01-21",
                "jobTitle"  : "Runner number one",
                "comment"   : "Mock test contact 1"
            }

    # allow getting items as if they were attributes
    def __getattr__(self, attr):
        return self[attr]
