import time
from OWDTestToolkit import DOM
from marionette import Actions
import functools
from OWDTestToolkit.utils.decorators import retry


class Loop(object):

    """Object representing the Loop application.
    """

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS
        self.actions = Actions(self.marionette)
        self.app_name = "Firefox Hello"

    def launch(self):
        """
        Launch the app.
        """
        self.app = self.apps.launch(self.app_name)
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay,
                                              self.__class__.__name__ + " app - loading overlay")
        return self.app

    def wizard_or_login(self):
        """ Checks if we have to skip the Wizard, log in, or if we're already at the main screen of Loop

            For the first two scenarios, it returns True.
            If we are alredy inside Loop, it returns False.
        """
        # TODO: switch try-except code -> first check login instead of wizard
        #      see if it works, when the wizard is first
        try:
            self.parent.wait_for_element_displayed(*DOM.Loop.wizard_header)
            self.UTILS.reporting.logResult('info', '[wizard_or_login] Wizard')
            self.skip_wizard()
            return True
        except:
            self.UTILS.reporting.logResult('info', '[wizard_or_login] Login')
            try:
                self.parent.wait_for_element_displayed(*DOM.Loop.wizard_login)
                return True
            except:
                header = ('xpath', DOM.GLOBAL.app_head_specific.format("Firefox Hello"))
                try:
                    self.parent.wait_for_element_displayed(*header)
                    return False
                except:
                    self.UTILS.test.TEST(False, "Ooops. Something went wrong")

    def get_wizard_steps(self):
        """ Returns the number of steps of the wizard
        """
        return len(self.marionette.find_elements(*DOM.Loop.wizard_slideshow_step))

    def skip_wizard(self):
        """ Skips first time use wizard by flicking the screen
        """
        time.sleep(1)
        wizard_steps = self.get_wizard_steps()

        current_frame = self.apps.displayed_app.frame
        x_start = current_frame.size['width']
        x_end = x_start // 3
        y_start = current_frame.size['height'] // 2

        for i in range(wizard_steps):
            self.actions.flick(
                current_frame, x_start, y_start, x_end, y_start, duration=500).perform()
            time.sleep(1)

        self.marionette.switch_to_frame(self.apps.displayed_app.frame_id)
        self.parent.wait_for_element_displayed(DOM.Loop.wizard_login[0], DOM.Loop.wizard_login[1], timeout=10)

    def _fill_fxa_field(self, field_locator, text):
        """ Auxiliary method to fill "Firefox account login" fields
        """
        self.UTILS.reporting.logResult('info', '[firefox_login] Filling fxa field with text: {}'.format(text))
        self.parent.wait_for_element_displayed(*field_locator)
        fxa_input = self.marionette.find_element(*field_locator)
        fxa_input.send_keys(text)
        time.sleep(2)

        self.parent.wait_for_condition(
            lambda m: m.find_element(*DOM.Loop.ffox_account_login_next).get_attribute("disabled") != "disabled")
        next_btn = self.marionette.find_element(*DOM.Loop.ffox_account_login_next)
        next_btn.tap()
        self.parent.wait_for_element_not_displayed(*DOM.Loop.ffox_account_login_overlay)

    def _tap_on_firefox_login_button(self):
        ffox_btn = self.marionette.find_element(*DOM.Loop.wizard_login_ffox_account)
        self.UTILS.element.simulateClick(ffox_btn)

    def firefox_login(self, email, password):
        """ Logs in using Firefox account
        """
        self._tap_on_firefox_login_button()

        self.UTILS.iframe.switchToFrame(*DOM.Loop.ffox_account_frame_locator)
        self.parent.wait_for_element_displayed(
            DOM.Loop.ffox_account_login_title[0], DOM.Loop.ffox_account_login_title[1], timeout=20)

        self._fill_fxa_field(DOM.Loop.ffox_account_login_mail, email)
        self._fill_fxa_field(DOM.Loop.ffox_account_login_pass, password)

        done_btn = self.marionette.find_element(*DOM.Loop.ffox_account_login_done)
        done_btn.tap()

    def phone_login(self):
        self.UTILS.reporting.logResult('info', '[TODO] Starting phone login...')

    @retry(5, aux_func="loop.retry_loop_connection")
    def allow_permission(self):
        """ Allows Loop to read our contacts

        This method checks whether is necessary to allow extra permissions for loop or not
        Also, since this is is the last step before connecting to the Loop server, it checks
        that no error has been raised. If that happens, it retries the connection up to 5 times.
        """
        self.marionette.switch_to_frame()
        try:
            self.parent.wait_for_element_displayed(
                DOM.GLOBAL.app_permission_dialog[0], DOM.GLOBAL.app_permission_dialog[1], timeout=10)
        except:
            try:
                self.apps.switch_to_displayed_app()
                header = ('xpath', DOM.GLOBAL.app_head_specific.format("Firefox Hello"))
                self.parent.wait_for_element_displayed(*header)
                return
            except:
                self.marionette.switch_to_frame()
                self.parent.wait_for_element_displayed(*DOM.GLOBAL.modal_dialog_alert_title)
                self.UTILS.reporting.logResult('info', "Error connecting...")
                # Make @retry do its work
                raise

        msg_text = self.marionette.find_element(*DOM.GLOBAL.app_permission_msg).text
        self.UTILS.test.TEST(self.app_name in msg_text, "Permissions for loop")

        allow_btn = self.marionette.find_element(*DOM.GLOBAL.app_permission_btn_yes)
        self.UTILS.element.simulateClick(allow_btn)

        self.apps.switch_to_displayed_app()

    def retry_loop_connection(self):
        """ Retry login if it has failed.

        This method is called as the aux_func for our brand new retry decorator
        """
        self.parent.wait_for_element_displayed(*DOM.GLOBAL.modal_dialog_alert_ok)
        ok_btn = self.marionette.find_element(*DOM.GLOBAL.modal_dialog_alert_ok)
        self.UTILS.element.simulateClick(ok_btn)

        self.apps.switch_to_displayed_app()
        time.sleep(2)
        self._tap_on_firefox_login_button()

    def open_settings(self):
        """ Open settings panel from call log 
        """
        self.parent.wait_for_element_displayed(*DOM.Loop.open_settings_btn)
        self.marionette.find_element(*DOM.Loop.open_settings_btn).tap()
        self.parent.wait_for_element_displayed(*DOM.Loop.settings_panel_header)

    def logout(self):
        """ This methods logs us out from Loop.

        It assumes we already are in the Loop Settings panel
        """
        self.parent.wait_for_element_displayed(*DOM.Loop.settings_logout)
        self.marionette.find_element(*DOM.Loop.settings_logout).tap()
        self.parent.wait_for_element_not_displayed(*DOM.Loop.loading_overlay)
        self.parent.wait_for_element_displayed(*DOM.Loop.wizard_login)
