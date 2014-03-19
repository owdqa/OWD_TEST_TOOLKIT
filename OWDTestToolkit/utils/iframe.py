import os
import time


class iframe(object):

    def __init__(self, parent):
        self.parent = parent
        self.marionette = parent.marionette

    def currentIframe(self, attribute="src"):
        #
        # Returns the "src" attribute of the current iframe
        # (very useful if you need to return to this iframe).<br>
        # The 'attribute' is the attribute that would contain
        # this url.
        #
        x = self.marionette.execute_script('return document.URL')
        # (remove anything after a '#' char.)
        x = x.split("#")[0]

        #
        # Need to switch to top layer ...
        #
        self.marionette.switch_to_frame()
        for i in self.marionette.find_elements("tag name", "iframe"):
            y = i.get_attribute(attribute)
            if x in y:
                #
                # Switch back to the original iframe and return the result.
                #
                z = self.marionette.find_element("xpath", "//iframe[@" + attribute + "='" + y + "']")
                self.marionette.switch_to_frame(z)
                return y

        # In case there's a problem.
        return ""

    def framePresent(self, attrib, value, via_root_frame=True):
        #
        # Checks for the presence of an iframe containing the attribute value <b>value</b>.<br>
        # For example: ("src", "contacts") or ("src", "sms") etc...<br><br>
        # NOTE: You *usually* need to do this via the 'root' frame (almost all iframes
        # are contained in the root-level frame).<br><br>
        # Performs this 'silently' and just returns True or False.
        #
        if via_root_frame:
            self.parent.general.checkMarionetteOK()
            self.marionette.switch_to_frame()

        if value == "":
            #
            # Use "=" because we want this field to be an empty string.
            #
            _frameDef = ("xpath", "//iframe[@{}='{}']".format(attrib, value))
        else:
            _frameDef = ("xpath", "//iframe[contains(@{},'{}')]".format(attrib, value))

        try:
            self.parent.parent.wait_for_element_present(*_frameDef, timeout=2)
            return True
        except:
            return False

    def switchToFrame(self, attrib, value, quit_on_error=True, via_root_frame=True):
        #
        # Switch to the iframe containing the attribute value <b>value</b>.<br>
        # For example: ("src", "contacts") or ("src", "sms") etc...<br><br>
        # NOTE: You *usually* need to do this via the 'root' frame (almost all iframes
        # are contained in the root-level frame).
        #
        if via_root_frame:
            self.parent.reporting.logResult("debug", "(Switching to root-level iframe.)")
            self.parent.general.checkMarionetteOK()
            self.marionette.switch_to_frame()

        #
        # We need to get all of them because some apps (browser) have more than one
        # matching iframe.
        #
        if value == "":
            #
            # Use "=" because we want this field to be an empty string.
            #
            _frameDef = ("xpath", "//iframe[@{}='{}']".format(attrib, value))
        else:
            _frameDef = ("xpath", "//iframe[contains(@{},'{}')]".format(attrib, value))

        x = ""
        try:
            self.parent.parent.wait_for_element_displayed(*_frameDef, timeout=20)
            x = self.marionette.find_elements(*_frameDef)
        except:
            pass

        is_ok = False
        for i in range(len(x)):
            #
            # Some iframes have > 1 'version' (such as the web page frame in browser app).
            # The only way to reliably tell them apart is to switch to the displayed one.
            #
            if x[i].is_displayed():
                try:
                    self.marionette.switch_to_frame(x[i])
                    is_ok = True
                    break
                except:
                    pass
            x = self.marionette.find_elements(*_frameDef)

        #
        # If we didn't manage to switch, then try frames that are not
        # displayed (sometime this is the case).
        #
        if not is_ok:
            x = self.marionette.find_elements(*_frameDef)
            for i in range(len(x)):
                try:
                    self.marionette.switch_to_frame(x[i])
                    is_ok = True
                    break
                except:
                    pass

            x = self.marionette.find_elements(*_frameDef)

        self.parent.test.TEST(is_ok, "<i>(Sucessfully switched to iframe where '{}' contains '{}'.)</i>".format(attrib, value),
                  quit_on_error)

    _framepath = []
    _MAXLOOPS = 20
    _old_src = ""

    def viewAllIframes(self):
        #
        # Dumps details of all iframes (recursively) into the run log.
        #

        # Just in case we end up in an endless loop ...
        self._MAXLOOPS = self._MAXLOOPS - 1
        if self._MAXLOOPS < 0:
            return

        #
        # Climb up from 'root level' iframe to the starting position ...
        #
        srcSTR = ""
        self.marionette.switch_to_frame()
        time.sleep(0.5)
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
                        self.parent.reporting.logResult("info", "<i>(Avoiding 'endless loop' where src=\"{}\"...)</i>"\
                                                        .format(new_src))
                        return

                    self._old_src = new_src
                    new_src = new_src if len(new_src) > 0 else "<i>(nothing)</i>"
                    srcSTR = "value of 'src'      = \"{}\"".format(new_src)

                self.marionette.switch_to_frame(int(i))

        x = self.parent.debug.screenShotOnErr()
        self.parent.reporting.logResult("info",  "Iframe details for frame with path: {}|{}".\
                                        format(self._framePathStr(), srcSTR), x)

        #
        # Do the same for all iframes in this iframe
        #
        self.parent.general.checkMarionetteOK()
        x = self.marionette.find_elements("tag name", "iframe")
        if len(x) > 0:
            for i2 in range(len(x)):
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
            pathStr = "{} -> {}".format(pathStr, i)

        return pathStr + "</b>"

    def _getFrameDetails(self):
        #
        # Private method to record the iframe details (LOCKS UP FOR SOME REASON, SO DON'T USE IT YET!!).
        #
        framepath_str = ""
        for i in self._framepath:
            if len(framepath_str) > 0:
                framepath_str = framepath_str + "-"
            framepath_str = framepath_str + i

        fnam = "{}/{}_frame_{}_details.txt".format(os.environ['RESULT_DIR'], self.parent.test.TESTNum, framepath_str)

        f = open(fnam, 'w')
        f.write("Attributes for this iframe ...\n")

        js_str = "return document.getElementsByTagName('iframe')[{}]".format(self._framepath[-1])
        num_attribs = self.marionette.execute_script(js_str + ".attributes.length;")
        for i in range(num_attribs):
            attrib_name = self.marionette.execute_script(js_str + ".attributes[{}].nodeName;".format(i))
            attrib_value = self.marionette.execute_script(js_str + ".attributes[{}].nodeValue;".format(i))
            f.write("    |_ " + attrib_name.ljust(20) + ": \"" + attrib_value + "\"\n")
        f.close()
        return fnam
