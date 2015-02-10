import time
import os
from OWDTestToolkit import DOM
from OWDTestToolkit.apps.browser import Browser
from marionette import Actions
from OWDTestToolkit.utils.decorators import retry
from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()


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
        self.browser = Browser(self.parent)
        self.app_name = "Firefox Hello"
        self.market_url = "https://owd.tid.es/B3lg1r89n/market/appList.html"
        self.loop_dir = self.UTILS.general.get_config_variable("install_dir", "loop")
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")[3:]

    def launch(self):
        """
        Launch the app.
        """
        self.app = self.apps.launch(self.app_name)
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay,
                                              self.__class__.__name__ + " app - loading overlay")
        return self.app

    def is_installed(self):
        return self.apps.is_app_installed(self.app_name)

    def install(self):
        via = self.UTILS.general.get_config_variable("install_via", "loop")
        if via == "Grunt":
            self.install_via_grunt()
        elif via == "Market":
            self.install_via_marketplace()
        else:
            self.UTILS.test.test(False, "Not valid way to install Loop")

    def install_via_grunt(self, version="1.1.1"):
        self.UTILS.reporting.logResult('info', 'Installing via grunt....')
        script = """ cd {0}
        git checkout {1}
        git fetch && git merge origin/{1}
        grunt build
        """.format(self.loop_dir, version)

        result = os.popen(script).read()
        self.UTILS.reporting.logResult('info', "Result of this test script: {}".format(result))

        self.marionette.switch_to_frame()
        msg = "{} installed".format(self.app_name)
        installed_app_msg = (DOM.GLOBAL.system_banner_msg[0], DOM.GLOBAL.system_banner_msg[1].format(msg))
        self.UTILS.element.waitForElements(installed_app_msg, "App installed", timeout=30)

        install_ok_msg = "Done, without errors."
        self.UTILS.test.test(install_ok_msg in result, "Install via grunt is OK")

    def install_via_marketplace(self):
        self.UTILS.reporting.logResult('info', 'Installing via marketplace....')
        # Make sure we install the latest version
        self.update_and_publish()

        self.browser.launch()
        time.sleep(1)
        self.browser.open_url(self.market_url)

        loop_link = self.UTILS.element.getElement(
            ('xpath', '//p[contains(text(), "{}")]'.format(self.app_name)), "App link")
        loop_link.tap()

        self.marionette.switch_to_frame()
        install_ok = self.UTILS.element.getElement(DOM.GLOBAL.app_install_ok, "Install button")
        install_ok.tap()

        msg = "{} installed".format(self.app_name)
        installed_app_msg = (DOM.GLOBAL.system_banner_msg[0], DOM.GLOBAL.system_banner_msg[1].format(msg))
        self.UTILS.element.waitForElements(installed_app_msg, "App installed", timeout=30)

    def reinstall(self):
        self.uninstall()
        time.sleep(2)
        self.install()

    def uninstall(self):
        self.UTILS.reporting.logResult('info', "uninstalling.........")
        self.apps.uninstall(self.app_name)
        self.parent.wait_for_condition(lambda m: not self.apps.is_app_installed(
            self.app_name), timeout=20, message="{} is not installed".format(self.app_name))

    def update_and_publish(self):
        self.publish_loop_dir = self.UTILS.general.get_config_variable("aux_files", "loop")

        result = os.popen("cd {} && ./publish_app.sh {}".format(self.publish_loop_dir, self.loop_dir)).read()
        chops = result.split("\n")
        self.UTILS.reporting.logResult('info', "result: {}".format(chops))
        self.UTILS.test.test("And all done, hopefully." in chops, "The script to publish an app is OK", True)

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

    def tap_on_firefox_login_button(self):
        ffox_btn = self.marionette.find_element(*DOM.Loop.wizard_login_ffox_account)
        self.UTILS.element.simulateClick(ffox_btn)

    def tap_on_phone_login_button(self):
        phone_btn = self.marionette.find_element(*DOM.Loop.wizard_login_phone_number)
        self.UTILS.element.simulateClick(phone_btn)

    def _get_mobile_id_options(self):
        return self.marionette.find_elements(*DOM.Loop.mobile_id_sim_list_item)

    def wizard_or_login(self):
        """ Checks if we have to skip the Wizard, log in, or if we're already at the main screen of Loop

            For the first two scenarios, it returns True.
            If we are already inside Loop, it returns False.
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
                self.UTILS.reporting.logResult('info', '[wizard_or_login] Loop')
                try:
                    self.parent.wait_for_element_displayed(*DOM.Loop.app_header)
                    return False
                except:
                    self.UTILS.test.test(False, "Ooops. Something went wrong", True)

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
        x_start = current_frame.size['width'] // 2
        x_end = x_start // 4
        y_start = current_frame.size['height'] // 2

        for i in range(wizard_steps):
            self.actions.flick(current_frame, x_start, y_start, x_end, y_start, duration=600).perform()
            time.sleep(1)

        self.marionette.switch_to_frame(self.apps.displayed_app.frame_id)
        self.parent.wait_for_element_displayed(*DOM.Loop.wizard_login, timeout=10)

    def firefox_login(self, email, password, is_wrong=False):
        """ Logs in using Firefox account
        """
        self.tap_on_firefox_login_button()

        self.UTILS.iframe.switchToFrame(*DOM.Loop.ffox_account_frame_locator)
        self.parent.wait_for_element_displayed(*DOM.Loop.ffox_account_login_title, timeout=20)

        self._fill_fxa_field(DOM.Loop.ffox_account_login_mail, email)
        self.marionette.find_element(*DOM.Loop.ffox_account_login_next).tap()

        # Sometimes we can get an age verification screen. In that case, select a proper value
        # and continue.
        try:
            self.parent.wait_for_element_displayed(*DOM.Loop.ffox_account_age_selector, timeout=6)
            self.marionette.find_element(*DOM.Loop.ffox_account_age_selector).tap()
            self.marionette.switch_to_frame()
            self.marionette.find_element(*DOM.Loop.ffox_account_age_option).tap()
            self.UTILS.reporting.debug("Age validation 1990 or earlier selected")
            self.marionette.find_element(*DOM.GLOBAL.conf_screen_ok_button).tap()
            self.UTILS.iframe.switchToFrame(*DOM.Loop.ffox_account_frame_locator)
            self.parent.wait_for_element_displayed(*DOM.Loop.ffox_account_login_next, timeout=6)
            self.marionette.find_element(*DOM.Loop.ffox_account_login_next).tap()
        except Exception as e:
            self.UTILS.reporting.debug("Age validation not found. Exception was: {}".format(e))

        self.UTILS.reporting.debug("Waiting for password input to be displayed...")
        self.parent.wait_for_element_displayed(*DOM.Loop.ffox_account_login_pass)
        self.UTILS.reporting.debug("Filling in password input...")
        self._fill_fxa_field(DOM.Loop.ffox_account_login_pass, password)

        time.sleep(2)
        if not is_wrong:
            done_btn = self.marionette.find_element(*DOM.Loop.ffox_account_login_done)
            done_btn.tap()

    # @retry(5, context=("OWDTestToolkit.apps.loop", "Loop"), aux_func_name="retry_phone_login")
    def phone_login_auto(self, option_number=1):
        """Wrapper to log in using phone number, either the already selected or entering it manually"""
        try:
            self.UTILS.reporting.info("Trying phone login using Mobile ID")
            self.phone_login(option_number)
        except:
            self.UTILS.reporting.info("Mobile ID login failed, falling back to manual")
            self.phone_login_manually(self.phone_number)

#    @retry(5, context=("OWDTestToolkit.apps.loop", "Loop"), aux_func_name="retry_phone_login")
    def phone_login(self, option_number=1):
        """ Logs in using mobile id
        """
        self.tap_on_phone_login_button()
        self.UTILS.iframe.switchToFrame(*DOM.Loop.mobile_id_frame_locator)
        self.parent.wait_for_element_not_displayed(*DOM.Loop.ffox_account_login_overlay)

        time.sleep(5)
        self.UTILS.reporting.info("Looking for Mobile ID header")
        mobile_id_header = ("xpath", DOM.GLOBAL.app_head_specific.format(_("Mobile ID")))
        self.parent.wait_for_element_displayed(*mobile_id_header)

        #=======================================================================
        # FJCS: I think this is not required now
        # options = self._get_mobile_id_options()
        # if len(options) > 1:
        #    # Option number refers to the SIM number (1 or 2), not to the position in the array
        #    options[option_number - 1].tap()
        #=======================================================================
        self.UTILS.reporting.info("Looking for Mobile ID INPUT")
        mobile_id_input = self.marionette.find_element(*DOM.Loop.mobile_id_add_phone_number_number)
        mobile_id_value = mobile_id_input.get_attribute("value")
        self.UTILS.reporting.info("Mobile ID Found: [{}]".format(mobile_id_value))
        if mobile_id_value == "":
            self.UTILS.reporting.info("No ID found, switching to manual...")
            self.marionette.find_element(*DOM.Loop.mobile_id_close_btn).tap()
            self.UTILS.iframe.switchToFrame(*DOM.Loop.frame_locator)
            time.sleep(5)
            self.marionette.find_element(*DOM.Loop.error_screen_ok).tap()
            time.sleep(5)
            raise Exception
        allow_button = self.marionette.find_element(*DOM.Loop.mobile_id_allow_button)
        allow_button.tap()

        try:
            self.UTILS.iframe.switchToFrame(*DOM.Loop.mobile_id_frame_locator)
            self.parent.wait_for_element_displayed(*DOM.Loop.mobile_id_verified_button, timeout=30)
            verified_button = self.marionette.find_element(*DOM.Loop.mobile_id_verified_button)
            time.sleep(5)
            verified_button.tap()
        except:
            self.parent.wait_for_condition(lambda m: "state-sending" in m.find_element(
                *DOM.Loop.mobile_id_allow_button).get_attribute("class"), timeout=5, message="Button is still sending")
            raise

        self.apps.switch_to_displayed_app()

    # @retry(5, context=("OWDTestToolkit.apps.loop", "Loop"), aux_func_name="retry_phone_login")
    def phone_login_manually(self, phone_number_without_prefix):
        """
        Logs in using mobile id, but instead of using the automatically provided by the app
        selecting the manual option
        @phone_number_without_prefix str Phone number to register into Loop
        NOTE: for the shake of simplicity, we assume the prefix is the spanish one (+34) by default
        """

        self.tap_on_phone_login_button()
        self.UTILS.iframe.switchToFrame(*DOM.Loop.mobile_id_frame_locator)
        self.parent.wait_for_element_not_displayed(*DOM.Loop.ffox_account_login_overlay)

        mobile_id_header = ("xpath", DOM.GLOBAL.app_head_specific.format(_("Mobile ID")))
        self.parent.wait_for_element_displayed(*mobile_id_header)

        self.parent.wait_for_element_displayed(*DOM.Loop.mobile_id_add_phone_number_number)
        phone_input = self.marionette.find_element(*DOM.Loop.mobile_id_add_phone_number_number)
        phone_input.send_keys(phone_number_without_prefix)

        # NOTE: before you virtually kill me, I cannot take this duplicated code into another
        # separated method due to the @reply decorator. Just letting you know :).
        self.parent.wait_for_element_displayed(*DOM.Loop.mobile_id_add_phone_number_number)
        allow_button = self.marionette.find_element(*DOM.Loop.mobile_id_allow_button)
        allow_button.tap()

        try:
            self.parent.wait_for_element_displayed(
                DOM.Loop.mobile_id_verified_button[0], DOM.Loop.mobile_id_verified_button[1], timeout=30)
            verified_button = self.marionette.find_element(*DOM.Loop.mobile_id_verified_button)
            self.UTILS.reporting.info("Before Tapping verify button")
            time.sleep(5)
            self.UTILS.reporting.info("Tapping verify button")
            verified_button.tap()
        except:
            self.parent.wait_for_condition(lambda m: "state-sending" in m.find_element(
                *DOM.Loop.mobile_id_allow_button).get_attribute("class"), timeout=5, message="Button is still sending")
            # Make @retry do its work
            raise

        self.apps.switch_to_displayed_app()

    @retry(5, context=("OWDTestToolkit.apps.loop", "Loop"), aux_func_name="retry_ffox_login")
    def allow_permission_ffox_login(self):
        """ Allows Loop to read our contacts

        This method checks whether is necessary to allow extra permissions for loop or not ater
        loggin in with Firefox accounts

        Also, since this is is the last step before connecting to the Loop server, it checks
        that no error has been raised. If that happens, it retries the connection up to 5 times.
        """
        self.marionette.switch_to_frame()
        try:
            self.UTILS.reporting.debug("Looking for permission panel....")
            self.parent.wait_for_element_displayed(
                DOM.GLOBAL.app_permission_dialog[0], DOM.GLOBAL.app_permission_dialog[1], timeout=10)
        except:
            try:
                self.UTILS.reporting.debug("Now looking for permission Loop main view....")
                self.apps.switch_to_displayed_app()
                self.parent.wait_for_element_displayed(*DOM.Loop.app_header)
                return
            except:
                self.UTILS.reporting.debug("And Now looking for error....")
                self.marionette.switch_to_frame()
                self.parent.wait_for_element_displayed(*DOM.GLOBAL.modal_dialog_alert_title)
                self.UTILS.reporting.logResult('info', "Error connecting...")
                # Make @retry do its work
                raise

        msg_text = self.marionette.find_element(*DOM.GLOBAL.app_permission_msg).text
        self.UTILS.test.test(self.app_name in msg_text, "Permissions for loop")

        allow_btn = self.marionette.find_element(*DOM.GLOBAL.app_permission_btn_yes)
        self.UTILS.element.simulateClick(allow_btn)

        self.apps.switch_to_displayed_app()

    def allow_permission_phone_login(self):
        """ Allows Loop to read our contacts

        This method checks whether is necessary to allow extra permissions for loop or not ater
        loggin in with Mobile ID

        Also, since this is is the last step before connecting to the Loop server, it checks
        that no error has been raised. If that happens, it retries the connection up to 5 times.
        """
        self.marionette.switch_to_frame()
        try:
            self.UTILS.reporting.debug("Looking for permission panel....")
            self.parent.wait_for_element_displayed(
                DOM.GLOBAL.app_permission_dialog[0], DOM.GLOBAL.app_permission_dialog[1], timeout=10)
        except:
            self.UTILS.reporting.debug("Now looking for permission Loop main view....")
            self.apps.switch_to_displayed_app()
            self.parent.wait_for_element_displayed(*DOM.Loop.app_header)
            return

        msg_text = self.marionette.find_element(*DOM.GLOBAL.app_permission_msg).text
        self.UTILS.test.test(self.app_name in msg_text, "Permissions for loop")

        allow_btn = self.marionette.find_element(*DOM.GLOBAL.app_permission_btn_yes)
        self.UTILS.element.simulateClick(allow_btn)

        self.apps.switch_to_displayed_app()

    def retry_ffox_login(self):
        """ Retry Ffox account login if it has failed.

        This method is called as the aux_func for our brand new retry decorator
        """

        self.UTILS.reporting.logResult('info', "Retrying FxA login...")
        self.apps.switch_to_displayed_app()
        time.sleep(2)

        self.parent.wait_for_element_displayed(*DOM.Loop.error_screen_ok)
        ok_btn = self.marionette.find_element(*DOM.Loop.error_screen_ok)
        self.UTILS.element.simulateClick(ok_btn)

        self.parent.wait_for_element_displayed(*DOM.Loop.wizard_login)
        self.tap_on_firefox_login_button()

    def retry_phone_login(self):
        """ Retry phone login if it has failed
        """
        self.UTILS.reporting.logResult('info', "Retrying phone login...")
        self.parent.wait_for_element_displayed(*DOM.Loop.mobile_id_back)
        back_btn = self.marionette.find_element(*DOM.Loop.mobile_id_back)
        self.UTILS.element.simulateClick(back_btn)

        self.apps.switch_to_displayed_app()
        time.sleep(2)
        self.tap_on_phone_login_button()

    def open_settings(self):
        """ Open settings panel from call log 
        """
        self.parent.wait_for_element_displayed(*DOM.Loop.open_settings_btn)
        settings_btn = self.marionette.find_element(*DOM.Loop.open_settings_btn)
        self.UTILS.element.simulateClick(settings_btn)
        self.parent.wait_for_element_displayed(*DOM.Loop.settings_panel_header)

    def logout(self, confirm=True):
        """ This methods logs us out from Loop.

        It assumes we already are in the Loop Settings panel
        """
        try:
            self.parent.wait_for_element_displayed(*DOM.Loop.settings_logout)
        except:
            self.UTILS.reporting.logResult('info', "Already logged out")
            return
        logout_btn = self.marionette.find_element(*DOM.Loop.settings_logout)
        self.UTILS.element.simulateClick(logout_btn)

        self.parent.wait_for_element_displayed(*DOM.Loop.form_confirm_logout)
        if confirm:
            confirm_btn = self.marionette.find_element(*DOM.Loop.form_confirm_logout)
            self.UTILS.element.simulateClick(confirm_btn)
            self.parent.wait_for_element_not_displayed(*DOM.Loop.loading_overlay)
            self.parent.wait_for_element_displayed(*DOM.Loop.wizard_login)
        else:
            cancel_btn = self.marionette.find_element(*DOM.Loop.form_confirm_cancel)
            self.parent.wait_for_element_displayed(*DOM.Loop.settings_panel_header)

    def switch_to_urls(self):
        self.parent.wait_for_element_displayed(*DOM.Loop.call_log_shared_links_tab)
        tab = self.marionette.find_element(*DOM.Loop.call_log_shared_links_tab)
        tab.tap()
        self.parent.wait_for_condition(lambda m: tab.get_attribute(
            "aria-selected") == "true", timeout=10, message="Checking that 'Shared links' is selected")

    def _get_number_of_urls(self, locator):
        try:
            entries = self.marionette.find_elements(*locator)
            return len(entries)
        except:
            return 0

    def get_number_of_all_urls(self):
        return self._get_number_of_urls(DOM.Loop.shared_links_entry)

    def get_number_of_available_urls(self):
        return self._get_number_of_urls(DOM.Loop.shared_links_entry_available)

    def get_number_of_revoked_urls(self):
        return self._get_number_of_urls(DOM.Loop.shared_links_entry_revoked)

    def _select_action(self, action):
        elem = (DOM.Loop.form_action_action[0], DOM.Loop.form_action_action[1].format(action))
        self.parent.wait_for_element_displayed(*elem)
        self.marionette.find_element(*elem).tap()

    def _confirm(self, decission):
        elem = DOM.Loop.form_confirm_delete if decission else DOM.Loop.form_confirm_cancel
        self.parent.wait_for_element_displayed(*elem)
        self.marionette.find_element(*elem).tap()

    def _is_entry_revoked(self, entry):
        try:
            entry.find_element(*DOM.Loop.shared_links_entry_revoked_nested)
            return True
        except Exception, e:
            self.UTILS.reporting.logResult('info', "What happened here? {}".format(e))
            return False

    def delete_single_entry_by_pos(self, position, confirm=True):
        try:
            entry = self.marionette.find_elements(*DOM.Loop.shared_links_entry)[position]
        except:
            self.UTILS.test.test(False, "No entry to delete by position", True)

        is_revoked = self._is_entry_revoked(entry)
        self.actions.long_press(entry, 2).perform()

        self._select_action("delete")

        if not is_revoked:
            self._confirm(confirm)

    def revoke_single_entry_by_pos(self, position, confirm=True):
        try:
            entry = self.marionette.find_elements(*DOM.Loop.shared_links_entry)[position]
        except:
            self.UTILS.test.test(False, "No entry to delete by position", True)

        self.actions.long_press(entry, 2).perform()
        self._select_action("revoke")

    def delete_all_urls(self, cancel=False, decission=True):
        self.parent.wait_for_element_displayed(*DOM.Loop.settings_clean_shared_links)
        self.marionette.find_element(*DOM.Loop.settings_clean_shared_links).tap()

        if cancel:
            self.parent.wait_for_element_displayed(*DOM.Loop.form_action_cancel)
            self.marionette.find_element(*DOM.Loop.form_action_cancel).tap()
        else:
            self._select_action("cleanAll")
            self._confirm(decission)

    def delete_just_revoked(self, cancel=False):
        self.parent.wait_for_element_displayed(*DOM.Loop.settings_clean_shared_links)
        self.marionette.find_element(*DOM.Loop.settings_clean_shared_links).tap()

        if cancel:
            self.parent.wait_for_element_displayed(*DOM.Loop.form_action_cancel)
            self.marionette.find_element(*DOM.Loop.form_action_cancel).tap()
        else:
            self._select_action("cleanJustRevoked")

    def settings_go_back(self):
        self.parent.wait_for_element_displayed(*DOM.Loop.settings_panel_back_btn)
        self.marionette.find_element(*DOM.Loop.settings_panel_back_btn).tap()

    def share_micro_and_camera(self):
        self.marionette.switch_to_frame()
        try:
            self.parent.wait_for_element_displayed(*DOM.GLOBAL.app_permission_btn_yes, timeout=10)
            allow_btn = self.marionette.find_element(*DOM.GLOBAL.app_permission_btn_yes)
            self.UTILS.reporting.debug("*** allow_btn: {}".format(allow_btn))
            self.UTILS.element.simulateClick(allow_btn)
        except Exception as e:
            self.UTILS.reporting.debug("Error waiting for button: {}".format(e))
        self.UTILS.iframe.switch_to_frame(*DOM.Loop.frame_locator)

    def initial_test_checks(self):
        # Make sure Loop is installed
        result = True
        if not self.is_installed():
            self.install()
        else:
            self.launch()
            # If already logged in, logout
            result = self.wizard_or_login()
            if not result:
                self.open_settings()
                self.logout()
        return result

    def open_address_book(self):
        self.parent.wait_for_element_displayed(*DOM.Loop.call_from_loop)
        open_link = self.marionette.find_element(*DOM.Loop.call_from_loop)
        time.sleep(1)
        open_link.tap()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

    def change_call_mode(self, mode):
        _values = {"Audio": "false", "Video": "true"}

        self.parent.wait_for_element_displayed(*DOM.Loop.settings_select_call_mode)
        self.marionette.find_element(*DOM.Loop.settings_select_call_mode).tap()

        self.marionette.switch_to_frame()

        option = (DOM.GLOBAL.modal_valueSel_option[0], DOM.GLOBAL.modal_valueSel_option[1].format(mode.capitalize()))
        self.parent.wait_for_element_displayed(*option)
        self.marionette.find_element(*option).tap()

        # Check the option has been selected before hitting OK button
        option_selected = (DOM.GLOBAL.modal_valueSel_option_selected[
                           0], DOM.GLOBAL.modal_valueSel_option_selected[1].format(mode.capitalize()))
        self.parent.wait_for_condition(
            lambda m: m.find_element(*option_selected).get_attribute("aria-selected") == "true")
        self.marionette.find_element(*DOM.GLOBAL.conf_screen_ok_button).tap()

        self.apps.switch_to_displayed_app()

        # Make sure the option is indeed selected, for that we have to check against the _values var
        self.parent.wait_for_condition(
            lambda m: m.find_element(*DOM.Loop.settings_select_call_mode).get_attribute("value") == _values[mode.capitalize()])

    def toggle_new_communication(self, is_room=True):
        """
        Taps on new communication button displayed_app at the footer of the Rooms Log or Calls log
        and selects one of the options.
        Does not deal with what may come after (Call: contact selection panel; Room: New room form)
        """
        self.parent.wait_for_element_displayed(*DOM.Loop.toggle_new_communication_button)
        self.marionette.find_element(*DOM.Loop.toggle_new_communication_button).tap()

        communication_button = DOM.Loop.create_new_room if is_room else DOM.Loop.create_new_call
        self.parent.wait_for_element_displayed(*communication_button)
        self.marionette.find_element(*communication_button).tap()

    def create_room(self, name):
        """Create a new room.

        Tap on the new communication button, enter the room name and click Save.
        """
        self.toggle_new_communication()
        time.sleep(2)
        self.parent.wait_for_element_displayed(*DOM.Loop.new_room_input)

        # Enter room name
        name_input = self.marionette.find_element(*DOM.Loop.new_room_input)
        name_input.send_keys(name)

        # Save room
        save_btn = self.marionette.find_element(*DOM.Loop.save_room_btn)
        save_btn.tap()

    def open_room_details(self, name):
        """Open room details page."""

        self.UTILS.reporting.info("Looking for Room entry: [{}]".format(name))
        room = self.marionette.find_element(DOM.Loop.room_entry[0], DOM.Loop.room_entry[1].format(name))
        self.UTILS.reporting.info("Tapping Edit button")
        self.marionette.find_element(*DOM.Loop.room_entry, id=room.id).tap()

    def edit_room(self, new_name):
        """Edit the room being shown in the detail view and change its name"""

        self.marionette.find_element(*DOM.Loop.room_detail_edit_btn).tap()

        self.parent.wait_for_element_displayed(*DOM.Loop.room_edit_name_reset)
        self.UTILS.reporting.info("Resetting Room name")
        reset_btn = self.marionette.find_element(*DOM.Loop.room_edit_name_reset)
        reset_btn.tap()

        self.UTILS.reporting.info("Setting new room name")
        name_input = self.marionette.find_element(*DOM.Loop.room_edit_name_input)
        name_input.send_keys(new_name)

        self.UTILS.reporting.info("Save room")
        self.marionette.find_element(*DOM.Loop.save_room_btn).tap()

    def share_room(self, contact, by_sms=True):
        """Share the current room with the given contact.

        If the by_sms parameter is True and the user has both phone number and email,
        the room link will be sent by SMS. Otherwise, it will be sent by email.
        """

        self.parent.wait_for_element_displayed(*DOM.Loop.room_share_button)
        self.marionette.find_element(*DOM.Loop.room_share_button).tap()

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.parent.contacts.search(contact['name'])
        self.parent.contacts.select_search_result(contact['name'])

        # If the contact does not have either phone number or email, an error screen
        # will appear
        try:
            self.marionette.switch_to_frame()
            self.UTILS.reporting.debug("Waiting for Invalid contact message...")
            self.parent.wait_for_element_displayed(*DOM.Loop.room_share_invalid_contact_ok, timeout=6)
            self.marionette.find_element(*DOM.Loop.room_share_invalid_contact_ok).tap()
            return False
        except:
            self.UTILS.iframe.switchToFrame(*DOM.Loop.frame_locator)
            self.UTILS.reporting.debug("Message not found, continue sharing.")
            pass

        # If the contact has both phone number and email, a menu will appear, asking which of the
        # two contact methods should be used. The by_sms parameter is used to select.
        try:
            self.UTILS.reporting.debug("Using email: {}".format(contact['email']['value']))
            button = (DOM.Loop.room_share_button_with_text[0],
                      DOM.Loop.room_share_button_with_text[1].format(contact['email']['value']))
            self.UTILS.reporting.debug("Waiting for button with text: {}".format(contact['email']['value']))
            self.parent.wait_for_element_displayed(*button, timeout=6)
            self.UTILS.reporting.debug("Button found, selecting method {}".format("SMS" if by_sms else "Email"))
            if by_sms:
                button = (DOM.Loop.room_share_button_with_text[0],
                      DOM.Loop.room_share_button_with_text[1].format(contact['tel']['value']))
                self.UTILS.reporting.debug("Looking for SMS button with text: {}".format(contact['tel']['value']))
            share_button = self.marionette.find_element(*button)
            self.UTILS.reporting.debug("Tapping method button: {}".format(share_button))
            self.UTILS.element.simulateClick(share_button)
            time.sleep(2)
        except Exception as e:
            self.UTILS.reporting.debug("Error selecting sharing method: {}".format(e))
            pass

        time.sleep(3)
        if by_sms:
            self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
            self.marionette.find_element(*DOM.Messages.send_message_button).tap()
        else:
            self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)
            self.marionette.find_element(*DOM.Email.compose_send_btn).tap()
        time.sleep(2)
        self.UTILS.iframe.switchToFrame(*DOM.Loop.frame_locator)

    def clean_all_rooms(self):
        """Remove all the rooms for the current user."""

        self.marionette.find_element(*DOM.Loop.open_settings_btn).tap()
        self.parent.wait_for_element_displayed(*DOM.Loop.settings_clean_rooms, timeout=6)
        self.marionette.find_element(*DOM.Loop.settings_clean_rooms).tap()
        self.parent.wait_for_element_displayed(*DOM.GLOBAL.confirm_form_delete_btn, timeout=6)
        self.marionette.find_element(*DOM.GLOBAL.confirm_form_delete_btn).tap()

    def select_camera_and_join_room(self, back=True):
        """Select the camera for a given call or room.

        If the back parameter is True indicates the back camera will be used. The front camera will
        be used otherwise.
        """
        btn_dom = DOM.Loop.room_select_camera_back if back else DOM.Loop.room_select_camera_front
        self.UTILS.reporting.debug("Selecting [{}] camera with DOM [{}]".format("Back" if back else "Front", btn_dom))
        self.parent.wait_for_element_displayed(*btn_dom)
        btn = self.marionette.find_element(*btn_dom)
        self.UTILS.element.simulateClick(btn)
        camera_container = self.marionette.find_element(*DOM.Loop.room_camera_container)
        selected_camera = camera_container.get_attribute("data-camera")
        expected_camera = "camera-{}".format("back" if back else "front")
        self.UTILS.test.test(selected_camera == expected_camera, "Expected camera: {}   Got: {}".
                             format(expected_camera, selected_camera))
        self.marionette.find_element(*DOM.Loop.room_button_join).tap()

    def hangup_room(self):
        """Hang up a room conversation and go back to the call log"""

        self.parent.wait_for_element_displayed(*DOM.Loop.room_leave_btn)
        leave_btn = self.marionette.find_element(*DOM.Loop.room_leave_btn)
        self.UTILS.element.simulateClick(leave_btn)
        time.sleep(2)
