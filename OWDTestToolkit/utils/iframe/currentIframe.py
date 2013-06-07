from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def currentIframe(self, p_attribute="src"):
        #
        # Returns the "src" attribute of the current iframe
        # (very useful if you need to return to this iframe).<br>
        # The 'p_attribute' is the attribute that would contain
        # this url. 
        #
        x = self.marionette.execute_script('return document.URL')
        x = x.split("#")[0] #(remove anything after a '#' char.)
        
        #
        # Need to switch to top layer ...
        #
        self.marionette.switch_to_frame()
        for i in self.marionette.find_elements("tag name", "iframe"):
            y = i.get_attribute(p_attribute)
            if x in y:
                #
                # Switch back to the original iframe and return the result.
                #
                z = self.marionette.find_element("xpath", "//iframe[@" + p_attribute + "='" + y + "']")
                self.marionette.switch_to_frame(z)
                return y
        
        # In case there's a problem.
        return ""
    
