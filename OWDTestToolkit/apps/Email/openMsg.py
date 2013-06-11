from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def openMsg(self, p_subject):
        #
        # Opens a specific email in the current folder
        # (assumes we're already in the folder we want).
        #

        myEmail = self.emailIsInFolder(p_subject)
        self.UTILS.TEST(myEmail != False, "Found email with subject '" + p_subject + "'.")
        if myEmail:
            #
            # We found it - open the email.
            #
            myEmail.tap()
            
            #
            # Check it opened.
            #
            boolOK = True
            try:
                self.wait_for_element_displayed(*DOM.Email.open_email_from)
                boolOK=True
            except:
                boolOK=False
                
            return boolOK
            
        else:
            return False

    
