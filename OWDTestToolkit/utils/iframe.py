import os
import time
import sys


class iframe(object):

    def __init__(self, parent):
        self.parent = parent
        self.marionette = parent.marionette
        self.frames_visited = []

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
                # get the first part of the path, including the app:// part
                orig_frame = y.split('.')[0]
                return orig_frame

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

    def switch_to_frame(self, attr, value, exact=False, is_displayed=True, test=True):
        self.marionette.switch_to_frame()
        if value is None:
            return

        frames = self.marionette.find_elements("tag name", "iframe")
        frame = None
        for f in frames:
            attr_value = f.get_attribute(attr)
            if value in attr_value and (value == attr_value) == exact:
                if is_displayed:
                    if f.is_displayed():
                        frame = f
                else:
                    frame = f
                break

        result = self.marionette.switch_to_frame(frame)
        if test:
            if exact:
                msg = '<i>(Sucessfully switched to iframe whose src attribute <b>is</b>: "{}".)</i>'.format(value)
            else:
                msg = '<i>(Sucessfully switched to iframe whose src attribute <b>contains</b>: "{}".)</i>'.format(value)

            self.parent.test.test(result, msg, True)

    def switch_to_active_frame(self):
        self.marionette.switch_to_frame()
        the_frame = self.marionette.find_element(*('css selector', 'iframe.active'))
        self.marionette.switch_to_frame(the_frame)
        
    def switchToFrame(self, attrib, value, quit_on_error=True, via_root_frame=True, test=True):
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

        if test:
            self.parent.test.test(is_ok, "<i>(Sucessfully switched to iframe where '{}' contains '{}'.)</i>".format(attrib, value),
                                  quit_on_error)

    def view_all_iframes(self, frame_src=None):
        #
        # Base case
        #
        has_switched = self._do_the_switch(frame_src)

        if has_switched == "skip":
            return

        if has_switched:
            dump = self.parent.debug.screenShotOnErr()
            self.parent.reporting.logResult(
                "info",  "Iframe details for frame with path: {}".format(frame_src if frame_src else "root"), dump)

            frames = self.marionette.find_elements('tag name', 'iframe')

            if len(frames) > 0:
                src_list = []
                #
                # This needs to be done because references to HTML elements change between recursive calls to
                # view_all_iframes
                #
                for f in frames:
                    src = f.get_attribute('src')
                    if not src in self.frames_visited:
                        self.frames_visited.append(src)
                        src_list.append(src)

                for src in src_list:
                    #
                    # Before recursive call, restore the frame to the parent one
                    #
                    if src_list.index(src) > 0:
                        self._do_the_switch(frame_src)
                    self.view_all_iframes(src)

    def _do_the_switch(self, frame_src):
        #
        # ignore_list: costcontrol -> unnecessary, keyboard -> breaks marioette
        #
        ignore_list = ("costcontrol", "keyboard")
        if frame_src:

            startpos = frame_src.index('/') + 2
            stoppos = frame_src.index('.')
            appname = frame_src[startpos:stoppos]

            if appname in ignore_list:
                return "skip"

            _frameDef = ("xpath", "//iframe[contains(@{},'{}')]".format('src', appname))
            try:

                frame_elem = self.marionette.find_element(*_frameDef)
                self.marionette.switch_to_frame(frame_elem)
            except:
                self.parent.reporting.logResult(
                    'info', '<i>exception launched while doing the switch!!. Frame_src: {}</i>'.format(frame_src))
                return False
        else:
            self.marionette.switch_to_frame()

        return True
