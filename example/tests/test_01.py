#
# (MANDATORY) Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#
from tests.mock_data.contacts import MockContacts

class test_main(GaiaTestCase):
    #
    # Things that will happen before "test_()" methods are run.
    #
    def setUp(self):
    
        #
        # (MANDATORY) Classes used by all tests.
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
    
        #
        # Classes particular to this test case.
        #
        self.contacts   = Contacts(self)
    
        #
        # Set the timeout for element searches.
        #
        self.marionette.set_search_timeout(50)
        self.lockscreen.unlock()

        #
        # Get details of our test contact.
        #
        self.Contact_1 = MockContacts().Contact_1
    
    #
    # Things that will happen after "test_()" methods are run.
    #
    def tearDown(self):
        #
        # (MANDATORY) for reporting the test results.
        #
        self.UTILS.reportResults()

    #
    # The test itself.
    #
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
    
        #
        # Create new contact.
        #
        self.contacts.createNewContact(self.Contact_1, './tests/resources/contact_face.jpg')
    
        #
        # TEST: The 'view contact' page shows the correct details for this new contact.
        #
        self.contacts.checkViewContactDetails(self.Contact_1, True)
