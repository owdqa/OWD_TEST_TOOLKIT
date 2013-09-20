from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def searchUsingUrlField(self, p_searchStr):
        #
        # Searches for p_searchStr using the URL field.
        #
		x = self.UTILS.getElement(DOM.Browser.url_input, "Search input field")
		x.send_keys(p_searchStr)
		x = self.UTILS.getElement(DOM.Browser.url_go_button, "'Go' button")
		x.tap()
		self.waitForPageToFinishLoading()
        
