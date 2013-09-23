from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):
    
    _framepath  = []
    _MAXLOOPS   = 20
    _old_src    = ""
    
    def viewAllIframes(self):
        #
        # Dumps details of all iframes (recursively) into the run log.
        #
        
        # Just in case we end up in an endless loop ...
        self._MAXLOOPS = self._MAXLOOPS - 1
        if self._MAXLOOPS < 0: return
        
        #
        # Climb up from 'root level' iframe to the starting position ...
        #
        srcSTR=""
        self.marionette.switch_to_frame()
        time.sleep(0.5)
        frame_dets = "<i>(unknown)</i>"
        if len(self._framepath) > 0:
            for i in self._framepath:
                
                if i == self._framepath[-1]:
                    # We're at the target iframe - record its "src" value.
                    try:
                        new_src = self.marionette.find_elements("tag name", "iframe")[int(i)].get_attribute("src")
                    except:
                        return
                    
                    if new_src != "" and new_src == self._old_src:
                        # This is an endless loop (some iframes seem to do this) - ignore it and move on.
                        self.logResult("info", "<i>(Avoiding 'endless loop' where src=\"%s\"...)</i>" % new_src)
                        return

                    self._old_src   = new_src
                    new_src         = new_src if len(new_src) > 0 else "<i>(nothing)</i>"
                    srcSTR          = "value of 'src'      = \"%s\"" % new_src
                    
                self.marionette.switch_to_frame(int(i))
            
        x = self.screenShotOnErr()
        self.logResult("info",  "Iframe details for frame with path: %s|%s" % (self._framePathStr(), srcSTR), x)

        #
        # Do the same for all iframes in this iframe 
        #
        ignoreme = -1
        self.checkMarionetteOK()
        x = self.marionette.find_elements("tag name", "iframe")
        
        if len(x) > 0:
                
            for i2 in range(0, len(x)):                 
                # Add this iframe number to the array.
                self._framepath.extend(str(i2))
                 
                # Process this iframe.
                self.viewAllIframes()
                 
                # Remove this iframe number from the array.
                del self._framepath[-1]
                
    def _framePathStr(self):
        #
        # Private method to return the iframe path in a 'nice' format.
        #
        pathStr = "<i>(root level)</i><b>"
        for i in self._framepath:
            pathStr = "%s -> %s" % (pathStr, i)
            
        return pathStr + "</b>"
                

    def _getFrameDetails(self):
        #
        # Private method to record the iframe details (LOCKS UP FOR SOME REASON, SO DON'T USE IT YET!!).
        #
        framepath_str = ""
        for i in self._framepath:
            if len(framepath_str) > 0: framepath_str = framepath_str + "-"
            framepath_str = framepath_str + i
            
        fnam = "%s/%s_frame_%s_details.txt" % (os.environ['RESULT_DIR'], self.testNum, framepath_str) 
        
        f = open(fnam, 'w')
        f.write("Attributes for this iframe ...\n")
         
        js_str = "return document.getElementsByTagName('iframe')[%s]" % self._framepath[-1]
        num_attribs = self.marionette.execute_script(js_str + ".attributes.length;")
        for i in range(0,num_attribs):
            attrib_name  = self.marionette.execute_script(js_str + ".attributes[%s].nodeName;" % i)
            attrib_value = self.marionette.execute_script(js_str + ".attributes[%s].nodeValue;" % i)
     
            f.write("    |_ " + attrib_name.ljust(20) + ": \"" + attrib_value + "\"\n")   
        f.close()
        
        return fnam

