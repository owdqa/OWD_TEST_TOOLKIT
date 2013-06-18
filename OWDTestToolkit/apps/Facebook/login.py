from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def login(self, p_user, p_pass):
        #
        # Log into facebook (and navigate to the facebook login frame ... sometimes!!).
        #
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Facebook.import_frame)

        x = self.UTILS.getElement(DOM.Facebook.email, "User field", True, 60)
        x.clear()
        x.send_keys(p_user)
        
        x = self.UTILS.getElement(DOM.Facebook.password, "Password field")
        x.clear()
        x.send_keys(p_pass)
        
        x = self.UTILS.getElement(DOM.Facebook.login_button, "Login button")
        x.tap()
        
