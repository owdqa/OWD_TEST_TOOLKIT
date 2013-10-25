from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def enterNumber(self, p_num):
        #
        # Enters a number into the dialler using the keypad.
        #

        try:
            self.wait_for_element_displayed(*DOM.Dialer.phone_number, timeout=1)
        except:
            x = self.UTILS.getElement(DOM.Dialer.option_bar_keypad, "Keypad option selector")
            x.tap()
            self.UTILS.waitForElements(DOM.Dialer.phone_number, "Phone number area")

        for i in str(p_num):

            if i=="+":
                x = self.UTILS.getElement( ("xpath", DOM.Dialer.dialler_button_xpath % 0),
                                           "keypad symbol '+'")
                self.actions=Actions(self.marionette)
                self.actions.long_press(x,2).perform()
            elif i=="1":
                self.marionette.execute_script("""
                var getElementByXpath = function (path) {
                    return document.evaluate(path, document, null, 9, null).singleNodeValue;
                };
                getElementByXpath("/html/body/section/article[3]/div/article/section/div/div").click();
                """)
            else:
                x = self.UTILS.getElement( ("xpath", DOM.Dialer.dialler_button_xpath % i),
                                           "keypad number %s" % i)
                x.tap()

        #
        # Verify that the number field contains the expected number.
        #
        x = self.UTILS.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = x.get_attribute("value")
        self.UTILS.TEST(str(p_num) in dialer_num, "After entering '%s', phone number field contains '%s'." % \
                                                  (dialer_num, str(p_num)))

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot:", x)