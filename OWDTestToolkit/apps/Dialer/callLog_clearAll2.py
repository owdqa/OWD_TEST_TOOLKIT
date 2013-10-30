from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def callLog_clearAll2(self):
    #
    # Wipes all entries from the csll log.
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

            self.UTILS.logResult("info", "Some numbers are in the call log here - removing them ...")
            x = self.UTILS.getElement(DOM.Dialer.call_log_edit_btn, "Edit button")
            x.tap()
            time.sleep(2)
            self.wait_for_element_present(*DOM.Dialer.call_log_edit_selAll, timeout=2)
            self.marionette.execute_script("document.getElementById('%s').click();" % DOM.Dialer.call_log_edit_selAll[1])
            time.sleep(1)
            self.wait_for_element_present(*DOM.Dialer.call_log_edit_delete, timeout=2)
            self.marionette.execute_script("document.getElementById('%s').click();" % DOM.Dialer.call_log_edit_delete[1])
            time.sleep(1)
            self.wait_for_element_present(*DOM.Dialer.call_log_dialog_delete, timeout=2)
            x = self.UTILS.getElement(DOM.Dialer.call_log_dialog_delete, "Confirm button")
            x.tap()

        self.UTILS.waitForElements(DOM.Dialer.call_log_no_calls_msg, "'No calls ...' message")
