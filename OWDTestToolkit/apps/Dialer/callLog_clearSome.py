from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def callLog_clearSome(self, p_entryNumbers):
        #
        # Wipes entries from the call log, using p_entryNumbers as an array of
        # numbers. For example: callLog_clearSome([1,2,3]) will remove the first 3.
        # <br><b>NOTE:</b> the first item is 1, <i>not</i> 0.
        #
        try:
            self.wait_for_element_displayed(*DOM.Dialer.call_log_filter, timeout=1)
        except:
            self.openCallLog()

        boolLIST = True
        try:
            self.wait_for_element_displayed(*DOM.Dialer.call_log_no_calls_msg, timeout=1)
            boolLIST = False
        except:
            pass

        if boolLIST:
            #
            # At the moment, the 'edit' div looks like it's not displayed, so Marionette can't tap it.
            # For this reason I'm using JS to click() instead.
            #
            self.UTILS.logResult("info", "Some numbers are in the call log here - removing them ...")
            x = self.UTILS.getElement(DOM.Dialer.call_log_edit_btn, "Edit button")
            x.tap()

            #
            # The edit mode doens't seem to be 'displayed', so we have to work around
            # that at the moment.
            #
            time.sleep(2)
            self.wait_for_element_present(*DOM.Dialer.call_log_edit_header, timeout=2)
            _els = ("xpath", "//ol[@class='log-group']//li")
            x = self.UTILS.getElements(_els, "Call log items", False)


            _precount = len(x)
            self.UTILS.logResult("info", "%s items found." % _precount)
            for i in p_entryNumbers:
                if i != 0:
                    _precount = _precount - 1
                    x[i-1].tap()

            #prueba
            #time.sleep(0.5)
            self.wait_for_element_present(*DOM.Dialer.call_log_edit_delete, timeout=2)
            self.marionette.execute_script("document.getElementById('%s').click();" % DOM.Dialer.call_log_edit_delete[1])
            #time.sleep(0.5)
            self.marionette.execute_script("""
            var getElementByXpath = function (path) {
                return document.evaluate(path, document, null, 9, null).singleNodeValue;
            };
            getElementByXpath("/html/body/form[3]/menu/button[2]").click();
            """)

            try:
                _postcount = self.UTILS.getElements(_els, "Call log items", False)
                _postcount = len(_postcount)
            except:
                _postcount = 0


            self.UTILS.TEST(_postcount == _precount,
                        "%s numbers are left after deletion (there are %s)." % \
                        (_precount,_postcount))



