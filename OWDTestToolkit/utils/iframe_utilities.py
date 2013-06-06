from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):
    def switchToFrame(self, p_tag, p_str, p_quitOnError=True):
        #
        # Switch to a different iframe based on tag and value.<br>
        # NOTE: You *usually* need to use self.marionette.switch_to_frame() first.
        #        
        x = self.getElement( ("xpath", "//iframe[@" + p_tag + "='" + p_str + "']"),
                             "iFrame with " + p_tag + " = '" + p_str + "'", False, 5)
        
        self.logResult("info", "(Switching to this frame.)")
        self.marionette.switch_to_frame(x)
        
# # This method was better is you wanted a 'null' element, i.e. src="".
#         self.wait_for_element_present("tag name", "iframe")
#         x = self.marionette.find_elements("tag name", "iframe")
#         for i in x:
#             if i.get_attribute(p_tag) == p_str:
#                 self.marionette.switch_to_frame(i)
#                 return True
#          
#         if p_quitOnError:
#             self.logResult(False, "Switch to frame " + p_tag + "=\"" + p_str + "\".")
#             self.quitTest()
#         else:
#             return False
    
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
    
    def viewAllIframes(self):
        #
        # DEV TOOL: this will loop through every iframe, report the "src", 
        # take a screenshot and capture the html.
        #
        # Because this is only meant as a dev aid (and shouldn't be in any released test
        # scripts), it reports to ERROR instead of COMMENT.
        #
        self.logResult("info", "(FOR DEBUGGING:) All current iframes (screenshots + html source) ...")

        time.sleep(1)

        try:
            current_iframe_src = self.currentIframe()
            fnam = self.screenShotOnErr()
            self.logResult("info", "Current iframe - src=\"" + str(current_iframe_src) + "\" ...", fnam)
        except:
           self.logResult("info", "(Cannot determine current iframe!)")
            

        self.marionette.switch_to_frame()
        fnam = self.screenShotOnErr()
        self.logResult("info", "Top level iframe: ()", fnam)

        iframes = self.marionette.find_elements("tag name", "iframe")
        for iframe in iframes:
            iframe_src = iframe.get_attribute("src")
            iframe_x   = str(iframe.get_attribute("data-frame-origin"))
            
            try:
                self.marionette.switch_to_frame(iframe)
                time.sleep(1)
    
                fnam = self.screenShotOnErr()
                log_msg = "iframe src=\"" + iframe_src + \
                          "\" data-frame-origin=\"" + iframe_x + "\""
                self.logResult("info", log_msg, fnam)
            except:
                self.logResult("info", 
                               "** Could not switch to iframe with src='" + iframe_src + "' and data-frame-origin='" + iframe_src + "'! **")
            
            self.marionette.switch_to_frame()
        
