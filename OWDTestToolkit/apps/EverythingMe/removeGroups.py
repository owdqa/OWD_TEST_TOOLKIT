from OWDTestToolkit.global_imports import *


class main(GaiaTestCase):
         
    def removeGroups(self, p_groupArray):
        #
        # Removes groups from the EME group page.<br>
        # <b>p_groupArray</p> is an array of group names (default = all groups).<br>
        # <br>
        # For example: <i> removeGroups(["Games","Local"])
        #
         
        #
        # Put the groups into edit mode.
        # Sometimes this takes a while to happen, so increase the length
        # of time you press the icon until it works!
        #
        _boolOK = False
        x = self.marionette.find_element('css selector', DOM.Home.app_icon_css % p_groupArray[0])
        from marionette import Actions
        actions = Actions(self.marionette)
        actions.press(x).wait(3).release()
        try:
            actions.perform()
        except:
            pass
            
        try:
            x = self.UTILS.getElement( ("xpath", DOM.Home.app_delete_icon_xpath % p_groupArray[0]), "Delete button", False, 5, True)
            if x.is_displayed():
                _boolOK = True
        except:
            pass
               
            time.sleep(2)
 
        self.UTILS.TEST(_boolOK, "Enabled EDIT mode.")
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of app in EDIT mode:", x)
 
        #
        # Remove all groups in the array.
        #
        _removed   = 0
        _groupCNT  = len(p_groupArray)

        self.UTILS.logResult("info", "Removing %s groups" % str(_groupCNT))

        self.UTILS.logResult("info", "Removing groups: %s" % str(p_groupArray))

        for _groupSpecified in p_groupArray:
            #
            # Remove it.
            #
            self.marionette.find_element('css selector', DOM.Home.app_icon_css % _groupSpecified)
            y = self.UTILS.getElement(("xpath", DOM.Home.app_delete_icon_xpath % _groupSpecified),
                                      "Delete button", False, 5, True)
            y.tap()

            delete = self.UTILS.getElement(DOM.Home.app_confirm_delete, "Confirm app delete button")
            delete.tap()
            _removed = _removed + 1
            self.UTILS.logResult("info", "Removed group '%s' ..." % _groupSpecified)
            self.UTILS.logResult("info", "Removed %s groups" % str(_removed))
            if _removed == _groupCNT:
                break

        #
        # Turn off edit mode.
        #
        self.UTILS.logResult("info", "Disabling edit mode ...")
        self.UTILS.touchHomeButton()