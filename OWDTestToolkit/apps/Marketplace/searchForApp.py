from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def searchForApp(self, p_app):
        #
        # Search for an app in the market.
        #

        #
        # Scroll a little to make the search area visible.
        #
# Changed to a frame-in-frame so can't be used like this just now.
#         self.marionette.execute_script('window.scrollTo(0, 10)')        
#         
#         self.UTILS.typeThis(DOM.Market.search_query, 
#                             "Search field",
#                             p_app + Keys.RETURN)
        
        
 		x = self.UTILS.getElement(DOM.Market.search_query, "Search field")
		x.send_keys(p_app + Keys.RETURN)


