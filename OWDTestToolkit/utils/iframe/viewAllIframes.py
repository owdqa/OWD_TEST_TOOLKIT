from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):
    
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
        
        self.marionette.switch_to_frame()
        frames = self.marionette.find_elements("tag name", "iframe")
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
              
            msg = extra_bit + "Iframe for app \"" + appname + "\" ..."
            msg = msg + "|iframe details saved to : " + filename_details
            msg = msg + "|screenshot saved to     : " + filename_screenshot
            msg = msg + "|html dump saved to      : " + filename_htmldump
            self.logResult("info", msg)
             
            #
            # Record the iframe details.
            #
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
              
            #
            # Take the screenshot and save it to the file.
            #
            screenshot = self.marionette.screenshot()[22:]
            with open(filename_screenshot, 'w') as f:
                f.write(base64.decodestring(screenshot))
            f.close()
                  
            #
            # Take the html dump and save it to the file.
            #
            f = open(filename_htmldump, 'w')
            f.write(self.marionette.page_source.encode('ascii', 'ignore') )
            f.close()
             
            self.marionette.switch_to_frame()


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
