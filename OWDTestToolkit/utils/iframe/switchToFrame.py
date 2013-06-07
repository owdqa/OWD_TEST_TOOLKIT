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
    
