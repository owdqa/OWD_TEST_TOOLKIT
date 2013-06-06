from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def setLanguage(self, p_lang):
        #
        # Set the language (assume we're in the language screen).
        time.sleep(1)
        x = self.UTILS.getElements(DOM.FTU.language_list, "Language list", True, 20, False)
        
        if len(x) > 0:
            for i in x:
                if i.text == p_lang:
                    i.tap()
                    return True
        
        return False
        
