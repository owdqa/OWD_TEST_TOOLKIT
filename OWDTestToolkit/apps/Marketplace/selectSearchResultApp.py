from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def selectSearchResultApp(self, p_app, p_author):
        #
        # Select the application we want from the list returned by
        # searchForApp().
        #
        self.UTILS.waitForElements(DOM.Market.search_results_area, "Search results area")
        results = self.UTILS.getElements(DOM.Market.search_results, "Search results")
        
        if len(results) <= 0:
            return False
        
        for app in results:
            if  app.find_element(*DOM.Market.app_name).text == p_app and \
                app.find_element(*DOM.Market.author).text == p_author:
                app.tap()
                return True
            
        return False


