from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

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
        
