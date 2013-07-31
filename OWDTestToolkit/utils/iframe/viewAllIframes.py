from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):
    
    msg = ""
    
    def viewAllIframes(self):
        #
        # DEV TOOL: this will loop through every iframe, 
        # report all attributes ("src","id" etc...), take a screenshot and capture the html.
        #
        # Because this is only meant as a dev aid (and shouldn't be in any released test
        # scripts), it reports to ERROR instead of COMMENT.
        #
        self.logResult("info", "** Collecting details of all iframes (* = current iframe) ...")
        
        LOGDIR              = os.environ['RESULT_DIR'] + "/"
        current_iframe_src  = self.currentIframe()
        
        if current_iframe_src == "":
            extra_bit = "(*) "
        else:
            extra_bit = ""
            
        self.msg = extra_bit + "Iframe for 'top level' () ..."
        filename_screenshot = LOGDIR + "top_level" + ".png"
        filename_htmldump   = LOGDIR + "top_level" + ".html"
        self.marionette.switch_to_frame()
        self._recordDetails(filename_screenshot, filename_htmldump)
        self.logResult("info", self.msg)

        frames = self.marionette.find_elements("tag name", "iframe")
        ucount=0
        for fnum in range (0, len(frames)):
            
            #
            # The app name is usually in the 'src' attribute,
            # so it's worth a shot.
            #
            frame_src = frames[fnum].get_attribute("src")
              
            if frame_src != "":
                startpos = frame_src.index('/') + 2
                stoppos  = frame_src.index('.')
                
                appname  = frame_src[startpos:stoppos]
                filename = appname                
            else:
                ucount = ucount + 1
                appname  = "(unknown)"
                filename = "unknown_" + str(ucount)
                
            filename = self.testNum + "_" + filename
                  
            #
            # Mark the current iframe.
            #
            if frame_src == current_iframe_src:
                extra_bit = "(*) "
            else:
                extra_bit = ""
            
            filename = filename + "-" + self.testNum + "_err_" + str(self.errNum)
                  
            filename_details    = LOGDIR + filename + "_iframe_details.txt"
            filename_screenshot = LOGDIR + filename + ".png"
            filename_htmldump   = LOGDIR + filename + ".html"

            #
            # I have random problems with 'costcontrol', so
            # since I'm not testing it I'll ignore it.
            #
            if appname == "costcontrol":
                continue
              
            self.msg = extra_bit + "Iframe for app \"" + appname + "\" ..."
             
            #
            # Record the iframe details.
            #
            self.msg = self.msg + "|iframe details saved to : " + filename_details
            f = open(filename_details, 'w')
            f.write("Attributes for this iframe ...\n")
            num_attribs = self.marionette.execute_script("return document.getElementsByTagName('iframe')[" + str(fnum) + "].attributes.length;")
            for i in range(0,num_attribs):
                attrib_name  = self.marionette.execute_script("return document.getElementsByTagName('iframe')[" + str(fnum) + "].attributes[" + str(i) + "].nodeName;")
                attrib_value = self.marionette.execute_script("return document.getElementsByTagName('iframe')[" + str(fnum) + "].attributes[" + str(i) + "].nodeValue;")
        
                f.write("    |_ " + attrib_name.ljust(20) + ": \"" + attrib_value + "\"\n")   
            f.close()
    
             
            #
            # Switch to this frame.
            #
            self.marionette.switch_to_frame(fnum)
              
            self._recordDetails(filename_screenshot, filename_htmldump)
             
            self.marionette.switch_to_frame()

            self.logResult("info", self.msg)

    def _recordDetails(self, filename_screenshot, filename_htmldump):
        #
        # PRIVATE function to record the details of this frame.
        #
        
        #
        # Take the screenshot and save it to the file.
        #
        self.msg = self.msg + "|screenshot saved to     : " + filename_screenshot
        screenshot = self.marionette.screenshot()[22:]
        with open(filename_screenshot, 'w') as f:
            f.write(base64.decodestring(screenshot))
        f.close()
              
        #
        # Take the html dump and save it to the file.
        #
        self.msg = self.msg + "|html dump saved to      : " + filename_htmldump
        f = open(filename_htmldump, 'w')
        f.write(self.marionette.page_source.encode('ascii', 'ignore') )
        f.close()

#     def viewAllIframes(self):
#         #
#         # DEV TOOL: this will loop through every iframe, report the "src", 
#         # take a screenshot and capture the html.
#         #
#         # Because this is only meant as a dev aid (and shouldn't be in any released test
#         # scripts), it reports to ERROR instead of COMMENT.
#         #
#         self.logResult("info", "(FOR DEBUGGING:) All current iframes (screenshots + html source) ...")
# 
#         time.sleep(1)
# 
#         try:
#             current_iframe_src = self.currentIframe()
#             fnam = self.screenShotOnErr()
#             self.logResult("info", "Current iframe - src=\"" + str(current_iframe_src) + "\" ...", fnam)
#         except:
#            self.logResult("info", "(Cannot determine current iframe!)")
#             
# 
#         self.marionette.switch_to_frame()
#         fnam = self.screenShotOnErr()
#         self.logResult("info", "Top level iframe: ()", fnam)
# 
#         iframes = self.marionette.find_elements("tag name", "iframe")
#         for iframe in iframes:
#             iframe_src = iframe.get_attribute("src")
#             iframe_x   = str(iframe.get_attribute("data-frame-origin"))
#             
#             try:
#                 self.marionette.switch_to_frame(iframe)
#                 time.sleep(1)
#     
#                 fnam = self.screenShotOnErr()
#                 log_msg = "iframe src=\"" + iframe_src + \
#                           "\" data-frame-origin=\"" + iframe_x + "\""
#                 self.logResult("info", log_msg, fnam)
#             except:
#                 self.logResult("info", 
#                                "** Could not switch to iframe with src='" + iframe_src + "' and data-frame-origin='" + iframe_src + "'! **")
#             
#             self.marionette.switch_to_frame()
#         
