from marionette import Wait
from OWDTestToolkit import DOM
from OWDTestToolkit.apps.video import Video
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.apps.music import Music
from OWDTestToolkit.apps.camera import Camera
import time

from OWDTestToolkit.utils.i18nsetup import I18nSetup
import re
_ = I18nSetup(I18nSetup).setup()


class Email(object):

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS

    def launch(self):
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(
            DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        return self.app

    def refresh(self):
        self.parent.wait_for_element_displayed(*DOM.Email.folder_refresh_button)
        self.marionette.find_element(*DOM.Email.folder_refresh_button).tap()

    def mails(self):
        self.refresh()
        self.wait_for_sync_completed()
        self.wait_for_message_list()
        return self.marionette.find_elements(*DOM.Email.email_entry)

    def _email_exists(self, subject):
        if subject in [mail.find_element(*DOM.Email.folder_subject_list).text for mail in self.mails()]:
            return True
        else:
            self.refresh()
            self.wait_for_sync_completed()
            self.UTILS.element.scroll_into_view(self.mails()[0])
            return False

    def get_email(self, subject):
        return filter(lambda msg: msg.find_element(*DOM.Email.folder_subject_list).text == subject, self.mails())[0]

    def wait_for_sync_completed(self):
        element = self.marionette.find_element(*DOM.Email.folder_refresh_button)
        self.parent.wait_for_condition(lambda m: element.get_attribute('data-state') == 'synchronized')

    def wait_for_folder(self, folder_name):
        self.parent.wait_for_condition(lambda m: m.find_element(*DOM.Email.folder_name).text == folder_name)

    def wait_for_email_loaded(self, subject):
        Wait(self.marionette, timeout=20, interval=5).until(
            lambda m: m.find_element(*DOM.Email.open_email_subject).text == subject)

    def wait_for_message_list(self):
        element = self.marionette.find_element(*DOM.Email.message_list_locator)
        self.parent.wait_for_condition(lambda m: element.is_displayed() and element.location['x'] == 0)

    def _create_attachment(self, locator, msg, frame_to_change):
        attach = self.UTILS.element.getElement(DOM.Email.compose_attach_btn, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()
        attacth_type = self.UTILS.element.getElement(locator, msg)
        attacth_type.tap()
        self.UTILS.iframe.switchToFrame(*frame_to_change)

    def create_email_image(self):
        self._create_attachment(DOM.Email.attach_gallery_btn, "From Gallery", DOM.Gallery.frame_locator)

    def create_email_camera_image(self):
        self._create_attachment(DOM.Email.attach_camera_btn, "From Camera", DOM.Camera.frame_locator)
        # Take a picture.
        self.camera = Camera(self.parent)
        self.camera.take_and_select_picture()
        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)

    def create_email_music(self):
        self._create_attachment(DOM.Email.attach_music_btn, "From Music", DOM.Music.frame_locator)

    def create_email_video(self):
        self._create_attachment(DOM.Email.attach_video_btn, "From video", DOM.Video.frame_locator)

    def attach_file(self, attached_type):
        """
        This method is reponsible of attaching a certain file to an email.
        NOTE: It does not fill neither the message destinatary nor the message body
        """

        self.gallery = Gallery(self.parent)
        self.video = Video(self.parent)
        self.music = Music(self.parent)

        if attached_type == "image":
            self.UTILS.general.add_file_to_device('./tests/_resources/80x60.jpg')
            self.create_email_image()
            self.gallery.click_on_thumbnail_at_position_email(0)
        elif attached_type == "cameraImage":
            self.create_email_camera_image()
        elif attached_type == "video":
            self.UTILS.general.add_file_to_device('./tests/_resources/mpeg4.mp4')
            self.create_email_video()
            self.video.click_on_video_at_position_email(0)
        elif attached_type == "audio":
            self.UTILS.general.add_file_to_device('./tests/_resources/AMR.amr')
            self.create_email_music()
            self.music.click_on_song_email()
        else:
            msg = "FAILED: Incorrect parameter received in create_and_send_mms()"\
                ". attached_type must being image, video or audio."
            self.UTILS.test.test(False, msg)

    def delete_email(self, subject):
        """
        Deletes the first message in this folder with this subject line.
        """
        self.open_msg(subject)

        # Press the delete button and confirm deletion.
        delete_btn = self.UTILS.element.getElementByXpath(DOM.Email.delete_this_email_btn[1])
        delete_btn.tap()
        delete_confirm = self.UTILS.element.getElement(DOM.Email.confirmation_delete_ok, "Confirmation button")
        delete_confirm.tap()

        # Refresh and check that the message is no longer in the inbox.
        self.refresh()
        self.wait_for_sync_completed()

        self.UTILS.test.test(not self._email_exists(
            subject), "Email with subject [{}] is no longer in the folder".format(subject))

    def email_is_in_folder(self, subject, timeout=60):
        self.parent.wait_for_condition(lambda m: self._email_exists(subject), timeout=timeout)
        return True

    def goto_folder_from_list(self, name):
        """
        Goto a specific folder in the folder list screen.
        """
        name = _(name)
        elem = ('xpath', DOM.Email.folder_name_xpath.format(name))
        folder_link = self.UTILS.element.getElement(elem, "Link to folder '" + name + "'")
        self.UTILS.element.scroll_into_view(folder_link)
        folder_link.tap()
        self.wait_for_folder(name)

    def open_folder(self, folder_name):
        # Check whether we're already there
        try:
            self.wait_for_folder(folder_name)
        except:
            # Open a specific mail folder (must be called from "Inbox").
            settings_menu = self.UTILS.element.getElement(DOM.Email.settings_menu_btn, "Settings menu button")
            settings_menu.tap()

            # When we're looking at the folders screen ...
            self.UTILS.element.waitForElements(
                DOM.Email.folder_list_container, "Folder list container", True, 20, False)
            self.goto_folder_from_list(folder_name)

            # Wait a while for everything to finish populating.
            self.UTILS.element.waitForNotElements(DOM.Email.folder_sync_spinner,
                                                  "Loading messages spinner", True, 60, False)

    def open_msg(self, subject):
        """
        Opens a specific email in the current folder
        (assumes we're already in the folder we want).
        """

        if self.email_is_in_folder(subject):
            mail = self.get_email(subject)
            self.UTILS.element.scroll_into_view(mail)
            mail.tap()
            self.wait_for_email_loaded(subject)
            return True
        else:
            screenshot = self.UTILS.debug.screenShotOnErr()
            self.UTILS.reporting.logResult('info', "Mail not found", screenshot)
            return False

    def _send_and_wait(self):
        send_btn = self.UTILS.element.getElement(DOM.Email.compose_send_btn, "Send button")
        send_btn.tap()

        self.UTILS.element.waitForElements(DOM.Email.toaster_sending_mail, "Sending email toaster", True, 60)
        self.UTILS.element.waitForNotElements(DOM.Email.toaster_sending_mail, "Sending email toaster", True, 60, False)
        self.UTILS.element.waitForElements(DOM.Email.toaster_sent_mail, "Email sent toaster", True, 120, False)

    def send_new_email(self, p_target, p_subject, p_message, attach=False, attached_type=None):
        """
        Compose and send a new email.
        """
        self.UTILS.reporting.logResult("info", "Getting 'compose message button'")

        compose_new_msg_btn = self.UTILS.element.getElement(DOM.Email.compose_msg_btn, "Compose button")
        time.sleep(1)
        compose_new_msg_btn.tap()

        # Put items in the corresponsing fields.
        self.parent.wait_for_element_displayed(*DOM.Email.compose_to)
        to_field = self.marionette.find_element(*DOM.Email.compose_to)
        if type(p_target) is list:
            for addr in p_target:
                to_field.send_keys(addr)
                to_field.send_keys(" ")
        else:
            to_field.send_keys(p_target)

        time.sleep(1)
        self.marionette.find_element(*DOM.Email.compose_subject).send_keys(p_subject)
        time.sleep(1)
        self.marionette.find_element(*DOM.Email.compose_msg).send_keys(p_message)
        if attach:
            self.attach_file(attached_type)

        self.send_the_email()

    def reply_msg(self, reply_message):
        """
        This method replies to a previously received message
        It assumes we already are viewing that message
        """

        # Get who sent us the email
        from_field = self.UTILS.element.getElement(DOM.Email.open_email_from, "'From' field").text

        reply_btn = self.UTILS.element.getElement(DOM.Email.reply_btn, "Reply message button")
        reply_btn.tap()

        reply_opt = self.UTILS.element.getElement(DOM.Email.reply_menu_reply, "'Reply' option button")
        reply_opt.tap()

        # Get the guy we're replying to
        to_field = self.UTILS.element.getElement(DOM.Email.compose_to_from_contacts, "[Reply] 'To' field")
        to_field = to_field.text

        # Check we're actually replying to the guy who sent us the email
        self.UTILS.test.test(to_field in from_field, "Checking we are replying correctly")

        # Write some reply content
        self.marionette.find_element(*DOM.Email.compose_msg).send_keys(reply_message)
        self.reply_the_email(from_field.split("@")[0])

    def reply_all(self, sender, reply_message):
        """
        This method replies to all recipients of a previously received message
        It assumes we already are viewing that message
        """

        # Get who sent us the email
        from_field = self.UTILS.element.getElement(DOM.Email.open_email_from, "'From' field").text

        reply_btn = self.UTILS.element.getElement(DOM.Email.reply_btn, "Reply message button")
        reply_btn.tap()

        # Now choose the "Reply all" option
        reply_opt = self.UTILS.element.getElement(DOM.Email.reply_menu_reply_all, "'Reply all' option button")
        reply_opt.tap()

        # Wait for 'compose message' header.
        self.parent.wait_for_element_displayed(*DOM.Email.compose_header, timeout=30)

        # Check the sender is not included in the 'To' field
        bubbles = self.UTILS.element.getElements(('css selector', '.cmp-to-container.cmp-addr-container .cmp-bubble-container .cmp-peep-name'),
                                                 '"To" field bubbles')
        bubbles_text = [bubble.text for bubble in bubbles]

        if sender['username'] in bubbles_text:
            self.UTILS.test.test(
                False, "Sender ({}) must not appear in the 'To field' when replying".format(sender['username']), True)

        # Write some reply content
        self.marionette.find_element(*DOM.Email.compose_msg).send_keys(reply_message)
        self.reply_the_email(from_field.split("@")[0])

    def forward_msg(self, p_target, fwd_message, attach=False, attached_type=None):
        """
        This method forward a previously received message to somebody else
        It assumes we already are viewing that message
        """

        # Get who sent us the email
        from_field = self.UTILS.element.getElement(DOM.Email.open_email_from, "'From' field").text

        reply_btn = self.UTILS.element.getElement(DOM.Email.reply_btn, "Reply message button")
        reply_btn.tap()

        # Now choose the "Forward" option
        fw_opt = self.UTILS.element.getElement(DOM.Email.reply_menu_forward, "'Forward' option button")
        fw_opt.tap()

        # Wait for 'compose message' header.
        self.parent.wait_for_element_displayed(*DOM.Email.compose_header, timeout=30)

        # Put items in the corresponding fields.
        self.parent.wait_for_element_displayed(*DOM.Email.compose_to)
        to_field = self.marionette.find_element(*DOM.Email.compose_to)
        if type(p_target) is list:
            for addr in p_target:
                to_field.send_keys(addr)
                to_field.send_keys(" ")
        else:
            to_field.send_keys(p_target)

        # Write some reply content
        self.marionette.find_element(*DOM.Email.compose_msg).send_keys(fwd_message)
        if attach:
            self.attach_file(attached_type)
        self.reply_the_email(from_field.split("@")[0])

    def reply_the_email(self, sender_name):
        """
        Hits the 'Send' button to reply to the message (handles
        waiting for the correct elements etc...).
        """
        self._send_and_wait()
        sender_header = ('xpath', DOM.GLOBAL.app_head_specific.format(sender_name))
        self.UTILS.element.waitForElements(sender_header, "Previous received message", True, 120)

    def send_the_email(self):
        """
        Hits the 'Send' button to send the message (handles
        waiting for the correct elements etc...).
        """
        self._send_and_wait()
        self.wait_for_folder(_("Inbox"))

    def send_the_email_and_switch_frame(self, header, frame_locator):
        send_btn = self.UTILS.element.getElement(DOM.Email.compose_send_btn, "Send button")
        send_btn.tap()
        app_header = ('xpath', DOM.GLOBAL.app_head_specific.format(header))
        self.UTILS.iframe.switchToFrame(*frame_locator)
        self.UTILS.element.waitForElements(app_header, header, True, 120)

    def setup_account_active_sync(self, user, email, passwd, hostname):
        """
        Set up a new ActiveSync account manually
        """
        if not self.no_existing_account(email):
            return

        # (At this point we are now in the 'New account' screen by one path or another.)
        self.marionette.find_element(*DOM.Email.username).send_keys(user)
        self.marionette.find_element(*DOM.Email.email_addr).send_keys(email)

        # Now tap on Manual setUp
        manual_setup = self.UTILS.element.getElement(DOM.Email.manual_setup, "Manual setup button")
        manual_setup.tap()

        # Check that we are indeed setting up an account manually
        self.UTILS.element.waitForElements(DOM.Email.manual_setup_sup_header, "Manual setup header", True, 5)

        # Change the account type to ActiveSync
        account_type = self.UTILS.element.getElement(DOM.Email.manual_setup_account_type, "Account type select")
        account_type.tap()

        # Change to top frame is needed in order to be able of choosing an option
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForElements(DOM.Email.manual_setup_account_options, "Account type options", True, 5)
        # Select active sync
        elem = (DOM.Email.manual_setup_account_option[0],
                DOM.Email.manual_setup_account_option[1].format("ActiveSync"))
        active_sync = self.UTILS.element.getElement(elem, "ActiveSync option")
        active_sync.tap()

        # Confirm
        ok_btn = self.UTILS.element.getElement(DOM.Email.manual_setup_account_type_ok, "Ok button")
        ok_btn.tap()

        # Going back to Email frame
        self.apps.switch_to_displayed_app()

        # Finish setting things up
        self.marionette.find_element(*DOM.Email.password).send_keys(passwd)
        time.sleep(1)
        self.marionette.find_element(*DOM.Email.manual_setup_activesync_host).send_keys(hostname)
        time.sleep(1)
        self.marionette.find_element(*DOM.Email.manual_setup_activesync_user).send_keys(user)
        time.sleep(1)

        manual_next_btn = self.UTILS.element.getElement(
            DOM.Email.manual_setup_next, "Manual Setup 'Next' button", True, 60)
        manual_next_btn.tap()

        manual_prefs_btn = self.UTILS.element.getElement(
            DOM.Email.login_account_prefs_next_btn, "Next button", True, 60)
        manual_prefs_btn.tap()

        # Click the 'continue to mail' button.
        manual_continue_btn = self.UTILS.element.getElement(
            DOM.Email.login_cont_to_email_btn, "'Continue to mail' button", True, 60)
        manual_continue_btn.tap()

        self.UTILS.element.waitForNotElements(DOM.Email.login_cont_to_email_btn, "'Continue to mail' button")
        self.wait_for_folder(_("Inbox"))

    def setup_account(self, user, email, passwd):
        """
        Set up a new email account in the email app and login.
        """
        if not self.no_existing_account(email):
            return

        # At this point we are now in the 'New account' screen by one path or another
        username_field = self._get_field(DOM.Email.username)
        username_field.send_keys(user)

        email_field = self._get_field(DOM.Email.email_addr)
        email_field.send_keys(email)

        self.tap_next_account_info()

        domain = re.search('[a-zA-Z0-9+_\-\.]+@([0-9a-zA-Z][.-0-9a-zA-Z]*).[a-zA-Z]+', email).group(1)
        if 'gmail' in domain:
            self.switch_to_gmail_frame(email)
            self.gmail_login(passwd)
            self.wait_for_gmail_approve_access()
            self.tap_gmail_approve_access()
        elif 'hotmail' or 'msn' or 'outlook' in domain:
            self.setup_hotmail_account(email, passwd)

        self.apps.switch_to_displayed_app()
        self.tap_next_account_preferences()
        self.tap_continue_to_mail()

        self.wait_for_folder(_("Inbox"))
        self.wait_for_sync_completed()
        self.wait_for_message_list()

    def setup_account_first_step(self, user, email, p_pass):
        """
        Set up a new email account in the email app and login.
        If we've just started out, email will open directly to "New Account").
        """
        if not self.no_existing_account(p_email):
            return

        # (At this point we are now in the 'New account' screen by one path or another.)
        self.marionette.find_element(*DOM.Email.username).send_keys(user)
        self.marionette.find_element(*DOM.Email.email_addr).send_keys(email)

    def no_existing_account(self, email):
        """
        Check if the new account header is present
        """
        try:
            self.parent.wait_for_element_displayed(*DOM.Email.setup_account_header)
            self.marionette.find_element(*DOM.Email.setup_account_header)
            return True
        except:

            #  If exception raised --> other account has been alread set up
            self.UTILS.reporting.logResult("info", "It is necessary to switch to another email account.")

            if self.switch_account(email):
                return False

            # It's not setup already, so prepare to set it up!
            set_settings = self.UTILS.element.getElement(DOM.Email.settings_set_btn, "Settings set button")
            set_settings.tap()

            add_account_btn = self.UTILS.element.getElement(DOM.Email.settings_add_account_btn, "Add account button")
            time.sleep(2)
            add_account_btn.tap()
            return True

    def switch_account(self, address):
        settings_menu = self.UTILS.element.getElement(DOM.Email.settings_menu_btn, "Settings menu button")
        settings_menu.tap()

        try:
            self.UTILS.reporting.logResult("info", "First, check whether we have one account configured or MORE")
            self.parent.wait_for_element_displayed(*DOM.Email.switch_account_panel_one_account)
            self.UTILS.reporting.logResult("info", "There's only a single account configured. Time to check if\
                                                        it's necessary to do the change")
            try:
                self.parent.wait_for_element_present(*DOM.Email.switch_account_current_account)
                current_account = self.marionette.find_element(*DOM.Email.switch_account_current_account)
                """
                Since the element is not displayed, sometimes we cannot access to the text using .text
                This way is more secure
                """
                current_account_text = self.marionette.execute_script(
                    "return arguments[0].innerHTML", script_args=[current_account])

                self.UTILS.reporting.logResult('info', "Current account: {}".format(current_account_text))
                self.UTILS.reporting.logResult('info', "Account to switch: {}".format(address))

                screenshot = self.UTILS.debug.screenShotOnErr()
                self.UTILS.reporting.logResult('info', "Screenshot", screenshot)

                if current_account_text == address:
                    self.UTILS.reporting.logResult("info", "Already in the account we want - switch back to inbox.")
                    self.goto_folder_from_list(_("Inbox"))
                    return True
                else:
                    self.UTILS.reporting.logResult(
                        "info", "It looks like the account we want to switch is not set up yet, so we cannot switch to it")
                    return False
            except:
                self.UTILS.reporting.logResult("info", "ONE ACCOUNT - something went wrong")

        except:
            self.UTILS.reporting.logResult("info", "Well, we have at least 2 accounts configured")

            self.UTILS.reporting.logResult("info", "Checking whether exists a scroll containing different accounts")
            self.parent.wait_for_element_displayed(*DOM.Email.switch_account_scroll_outer)

            self.UTILS.reporting.logResult("info", "Check if the current account is the one we we want to change")
            self.parent.wait_for_element_displayed(*DOM.Email.switch_account_current_account)
            current_account = self.marionette.find_element(*DOM.Email.switch_account_current_account)

            if current_account.text == address:
                self.UTILS.reporting.logResult("info", "Already in the account we want - switch back to inbox.")
                self.goto_folder_from_list(_("Inbox"))
                return True

            self.UTILS.reporting.logResult(
                "info", "We're not in the account we want to be, so open the scroll to see what's there")

            self.parent.wait_for_element_displayed(*DOM.Email.switch_account_scroll)
            scroll = self.marionette.find_element(*DOM.Email.switch_account_scroll)
            scroll.tap()

            self.UTILS.reporting.logResult(
                "info", "Now we have to iterate over all accounts displayed (but not already selected)")
            self.parent.wait_for_element_displayed(*DOM.Email.switch_account_accounts_to_change)
            accounts = self.marionette.find_elements(*DOM.Email.switch_account_accounts_to_change)

            for account in accounts:
                if account.text == address:
                    self.UTILS.reporting.logResult(
                        "info", "We got a winner. Switching to already configured account...")
                    account.tap()
                    self.wait_for_folder(_("Inbox"))
                    return True

            self.UTILS.reporting.logResult(
                "info", "It looks like the account we want to switch is not set up yet, so we cannot switch to it")
            return False

    def switch_to_gmail_frame(self, expected_email):
        """
        Switches to gmail login frame when trying to set up a gmail account
        """
        gmail_frame = self.parent.wait_for_element_present(*DOM.Email.gmail_iframe_locator)
        self.marionette.switch_to_frame(gmail_frame)

        # Make sure the page is loaded
        email = self.parent.wait_for_element_present(*DOM.Email.gmail_email_locator)
        self.parent.wait_for_condition(lambda m: email.get_attribute('value') == expected_email)

    def _get_field(self, locator):
        self.parent.wait_for_element_displayed(*locator)
        return self.marionette.find_element(*locator)

    def gmail_login(self, passwd):
        self.marionette.find_element(*DOM.Email.gmail_password_locator).send_keys(passwd)
        self.marionette.find_element(*DOM.Email.gmail_sign_in_locator).tap()

    def wait_for_gmail_approve_access(self):
        self.parent.wait_for_element_displayed(*DOM.Email.gmail_approve_access_locator)

    def tap_gmail_approve_access(self):
        self.parent.wait_for_condition(
            lambda m: self.marionette.find_element(*DOM.Email.gmail_approve_access_locator).is_enabled())
        self.marionette.find_element(*DOM.Email.gmail_approve_access_locator).tap()

    def tap_next_account_info(self):
        self.marionette.find_element(*DOM.Email.login_account_info_next_btn).tap()

    def tap_next_account_preferences(self):
        self.parent.wait_for_element_displayed(*DOM.Email.login_account_prefs_next_btn, timeout=120)
        self.marionette.find_element(*DOM.Email.login_account_prefs_next_btn).tap()

    def tap_continue_to_mail(self):
        self.parent.wait_for_element_displayed(*DOM.Email.login_cont_to_email_btn, timeout=20)
        continue_btn = self.marionette.find_element(*DOM.Email.login_cont_to_email_btn)
        time.sleep(1)
        continue_btn.tap()

    def setup_hotmail_account(self, expected_email, passwd):
        """
        Switches to gmail login frame when trying to set up a gmail account
        """
        self.parent.wait_for_element_displayed(*DOM.Email.email_label_for_passwd)
        label = self.marionette.find_element(*DOM.Email.email_label_for_passwd)
        self.UTILS.test.test(label.text == expected_email, "The account remains the same: {}".format(expected_email))

        self.parent.wait_for_element_displayed(*DOM.Email.password)
        self.marionette.find_element(*DOM.Email.password).send_keys(passwd)

        self.parent.wait_for_condition(lambda m: m.find_element(*DOM.Email.login_account_passwd_next_btn).is_enabled())
        self.marionette.find_element(*DOM.Email.login_account_passwd_next_btn).tap()
