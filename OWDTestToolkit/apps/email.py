from marionette import Wait
from OWDTestToolkit import DOM
from OWDTestToolkit.apps.video import Video
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.apps.music import Music
from OWDTestToolkit.apps.camera import Camera
import time

from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()


class Email(object):

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS

    def launch(self):
        #
        # Launch the app.
        #
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
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

    def createEmailImage(self):

        attach = self.UTILS.element.getElement(DOM.Email.compose_attach_btn, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        gallery = self.UTILS.element.getElement(DOM.Email.attach_gallery_btn, "From gallery")
        gallery.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Gallery.frame_locator)

    def createEmailCameraImage(self):
        self.camera = Camera(self.parent)

        attach = self.UTILS.element.getElement(DOM.Email.compose_attach_btn, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        camera = self.UTILS.element.getElement(DOM.Email.attach_camera_btn, "From Camera")
        camera.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Camera.frame_locator)

        #
        # Take a picture.
        #
        self.camera.take_and_select_picture()

        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)

    def createEmailMusic(self):

        attach = self.UTILS.element.getElement(DOM.Email.compose_attach_btn, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        music = self.UTILS.element.getElement(DOM.Email.attach_music_btn, "From music")
        music.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Music.frame_locator)

    def createEmailVideo(self):

        attach = self.UTILS.element.getElement(DOM.Email.compose_attach_btn, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        video = self.UTILS.element.getElement(DOM.Email.attach_video_btn, "From video")
        video.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Video.frame_locator)

    def attach_file(self, attached_type):
        #
        # This method is reponsible of attaching a certain file to an email.
        # NOTE: It does not fill neither the message destinatary nor the message body
        #

        self.gallery = Gallery(self.parent)
        self.video = Video(self.parent)
        self.music = Music(self.parent)

        if attached_type == "image":
            #
            # Add an image file
            #
            self.UTILS.general.add_file_to_device('./tests/_resources/80x60.jpg', destination='DCIM/100MZLLA')

            self.createEmailImage()
            self.gallery.click_on_thumbnail_at_position_email(0)

        elif attached_type == "cameraImage":
            #
            # Add an image file from camera
            #
            self.createEmailCameraImage()

        elif attached_type == "video":
            #
            # Load an video file into the device.
            #
            self.UTILS.general.add_file_to_device('./tests/_resources/mpeg4.mp4', destination='/SD/mus')

            self.createEmailVideo()
            self.video.click_on_video_at_position_email(0)

        elif attached_type == "audio":
            #
            # Load an video file into the device.
            #
            self.UTILS.general.add_file_to_device('./tests/_resources/AMR.amr', destination='/SD/mus')

            self.createEmailMusic()
            self.music.click_on_song_email()

        else:
            msg = "FAILED: Incorrect parameter received in create_and_send_mms()"\
                ". attached_type must being image, video or audio."
            self.UTILS.test.test(False, msg)

    def deleteEmail(self, subject):
        #
        # Deletes the first message in this folder with this subject line.
        #

        #
        # Open the message.
        #
        self.openMsg(subject)

        #
        # Press the delete button and confirm deletion.
        #
        delete_btn = self.UTILS.element.getElementByXpath(DOM.Email.delete_this_email_btn[1])
        delete_btn.tap()
        delete_confirm = self.UTILS.element.getElement(DOM.Email.confirmation_delete_ok, "Confirmation button")
        delete_confirm.tap()

        self.UTILS.element.waitForElements(DOM.Email.deleted_email_notif, "Email deletion notifier")

        #
        # Refresh and check that the message is no longer in the inbox.
        #
        refresh_btn = self.marionette.find_element(*DOM.Email.folder_refresh_button)
        refresh_btn.tap()
        time.sleep(2)

        x = self.UTILS.element.getElements(DOM.Email.folder_subject_list, "Email messages in this folder")
        self.UTILS.test.test(x[0].text != subject, "Email '" + subject + "' no longer found in this folder.", False)

    def emailIsInFolder(self, subject, timeout=60):
        self.parent.wait_for_condition(lambda m: self._email_exists(subject), timeout=timeout)
        return True

    def goto_folder_from_list(self, name):
        #
        # Goto a specific folder in the folder list screen.
        #
        name = _(name)
        elem = ('xpath', DOM.Email.folderList_name_xpath.format(name))

        folder_link = self.UTILS.element.getElement(elem, "Link to folder '" + name + "'")
        self.UTILS.element.scroll_into_view(folder_link)
        folder_link.tap()

        self.UTILS.element.waitForElements(("xpath", DOM.GLOBAL.app_head_specific.format(name)),
                                   "Header for '" + name + "' folder")

    def openMailFolder(self, folder_name):
        #
        # Check whether we're already there
        #
        try:
            self.UTILS.reporting.logResult("info", "Checking if it's necessary to open it")
            self.parent.wait_for_element_displayed(*("xpath", DOM.GLOBAL.app_head_specific.format(folder_name)))
        except:
            self.UTILS.reporting.logResult("info", "Yes, we have to open the folder: {}".format(folder_name))
            #
            # Open a specific mail folder (must be called from "Inbox").
            #
            x = self.UTILS.element.getElement(DOM.Email.settings_menu_btn, "Settings menu button")
            x.tap()

            #
            # When we're looking at the folders screen ...
            #
            self.UTILS.element.waitForElements(DOM.Email.folder_list_container, "Folder list container", True, 20, False)

            #
            # ... click on the folder were after.
            #
            self.goto_folder_from_list(folder_name)

            #
            # Wait a while for everything to finish populating.
            #
            self.UTILS.element.waitForNotElements(DOM.Email.folder_sync_spinner,
                                          "Loading messages spinner", True, 60, False)

    def openMsg(self, subject):
        """
        Opens a specific email in the current folder
        (assumes we're already in the folder we want).
        """

        if self.emailIsInFolder(subject):
            mail = self.get_email(subject)
            self.UTILS.element.scroll_into_view(mail)
            time.sleep(2)
            self.UTILS.element.simulateClick(mail)
            self.wait_for_email_loaded(subject)
            return True
        else:
            screenshot = self.UTILS.debug.screenShotOnErr()
            self.UTILS.reporting.logResult('info', "Mail not found", screenshot)
            return False

    def remove_accounts_and_restart(self):
        """Remove current email accounts via the UI and restart the application."""

        self.launch()

        try:
            self.UTILS.element.waitForElements(("xpath", "//h1[text()='{}']".format(_("Inbox"))),
                                                        "Inbox header", 10)
        except:
            # We have no accounts set up (or the app would default to
            # the inbox of one of them).
            self.UTILS.reporting.logResult("info", "(No email accounts set up yet.)")
            return

        settings_btn = self.UTILS.element.getElement(DOM.Email.settings_menu_btn, "Settings button")
        settings_btn.tap()

        set_btn = self.UTILS.element.getElement(DOM.Email.settings_set_btn, "Set settings button")
        set_btn.tap()

        self.UTILS.element.waitForElements(DOM.Email.settings_header, "Mail settings", True, 20, False)

        # Remove each email address listed ...
        accounts_list = self.UTILS.element.getElements(DOM.Email.email_accounts_list,
                                   "Email accounts list", False, 20, False)
        for i in accounts_list:
            if i.text != "":
                # This isn't a placeholder, so delete it.
                self.UTILS.reporting.logComment("i: " + i.text)
                i.tap()

                header = ('xpath', DOM.GLOBAL.app_head_specific.format(i.text))
                self.UTILS.element.waitForElements(header, i.text + " header", True, 20, False)

                # Delete.
                delacc = self.UTILS.element.getElement(DOM.Email.settings_del_acc_btn, "Delete account button")
                delacc.tap()
                time.sleep(2)

                # Confirm.  <<<< PROBLEM (on forums)!
                delconf = self.UTILS.element.getElement(DOM.Email.settings_del_conf_btn, "Confirm delete button")
                delconf.tap()

                # Wait for this dialog to go away, then sleep for 1s.

        # Now relaunch the app.
        self.launch()

    def send_new_email(self, p_target, p_subject, p_message, attach=False, attached_type=None):
        #
        # Compose and send a new email.
        #
        self.UTILS.reporting.logResult("info", "Getting 'compose message button'")

        self.parent.wait_for_element_displayed(*DOM.Email.compose_msg_btn)
        compose_new_msg_btn = self.marionette.find_element(*DOM.Email.compose_msg_btn)
        compose_new_msg_btn.tap()

        # Sometimes, the tap on the "Compose message button" does not work, resulting in a failed test
        # Let's try to do something about it
        self.parent.wait_for_condition(lambda m: self._is_composed_btn_tapped(),
                                        timeout=30, message="'Compose message' button tapped")
        # Put items in the corresponsing fields.
        if type(p_target) is list:
            for addr in p_target:
                self.UTILS.general.typeThis(DOM.Email.compose_to, "'To' field", addr, True, False, True, False)
                self.UTILS.general.typeThis(DOM.Email.compose_to, "'To' field", " ", True, False, True, False)
        else:
            self.UTILS.general.typeThis(DOM.Email.compose_to, "'To' field", p_target, True, False)
        self.UTILS.general.typeThis(DOM.Email.compose_subject, "'Subject' field", p_subject, True, False)
        self.UTILS.general.typeThis(DOM.Email.compose_msg, "Message field", p_message, True, False, False)

        if attach:
            self.attach_file(attached_type)

        self.sendTheMessage()

    def _is_composed_btn_tapped(self):

        try:
            self.parent.wait_for_element_displayed(*DOM.Email.compose_header)
            return True
        except:
            self.parent.wait_for_element_displayed(*DOM.Email.compose_msg_btn)
            compose_new_msg_btn = self.marionette.find_element(*DOM.Email.compose_msg_btn)
            compose_new_msg_btn.tap()
            return False

    def reply_msg(self, reply_message):
        #
        # This method replies to a previously received message
        # It assumes we already are viewing that message
        #

        # Get who sent us the email
        from_field = self.UTILS.element.getElement(DOM.Email.open_email_from, "'From' field").text

        reply_btn = self.UTILS.element.getElement(DOM.Email.reply_btn, "Reply message button")
        reply_btn.tap()

        reply_opt = self.UTILS.element.getElement(DOM.Email.reply_menu_reply, "'Reply' option button")
        reply_opt.tap()

        # Wait for 'compose message' header.
        self.parent.wait_for_element_displayed(*DOM.Email.compose_header)
        time.sleep(5)

        #
        #  TODO - Finnish the following assertion
        #

        # #
        # # Get the guy we're replying to
        # #
        # to_field = self.UTILS.element.getElement(DOM.Email.compose_to_from_contacts_address, "[Reply] 'To' field", False).text

        # #
        # # Check we're actually replying to the guy who sent us the email
        # #
        # self.UTILS.reporting.logResult("info", "'From' field: {}".format(from_field))
        # self.UTILS.reporting.logResult("info", "'To' field: {}".format(to_field))
        # self.UTILS.test.test(from_field == to_field, "Checking we are replying correctly")

        # Write some reply content
        self.UTILS.general.typeThis(DOM.Email.compose_msg, "Message field", reply_message, True, True, False, False)

        self.replyTheMessage(from_field.split("@")[0])

    def reply_all(self, sender, reply_message):
        #
        # This method replies to all recipients of a previously received message
        # It assumes we already are viewing that message
        #

        # Get who sent us the email
        from_field = self.UTILS.element.getElement(DOM.Email.open_email_from, "'From' field").text

        reply_btn = self.UTILS.element.getElement(DOM.Email.reply_btn, "Reply message button")
        reply_btn.tap()

        # Now choose the "Reply all" option
        reply_opt = self.UTILS.element.getElement(DOM.Email.reply_menu_reply_all, "'Reply all' option button")
        reply_opt.tap()

        # Wait for 'compose message' header.
        self.parent.wait_for_element_displayed(*DOM.Email.compose_header)
        time.sleep(5)

        # Check the sender is not included in the 'To' field
        bubbles = self.UTILS.element.getElements(('css selector', '.cmp-to-container.cmp-addr-container .cmp-bubble-container .cmp-peep-name'),
                                            '"To" field bubbles')
        bubbles_text = [bubble.text for bubble in bubbles]

        if sender['username'] in bubbles_text:
            self.UTILS.test.test(False, "Sender ({}) must not appear in the 'To field' when replying".format(sender['username']), True)

        # Write some reply content
        self.UTILS.general.typeThis(DOM.Email.compose_msg, "Message field", reply_message, True, True, False, False)

        self.replyTheMessage(from_field.split("@")[0])

    def forward_msg(self, p_target, fwd_message, attach=False, attached_type=None):
        #
        # This method forward a previously received message to somebody else
        # It assumes we already are viewing that message
        #

        # Get who sent us the email
        from_field = self.UTILS.element.getElement(DOM.Email.open_email_from, "'From' field").text

        reply_btn = self.UTILS.element.getElement(DOM.Email.reply_btn, "Reply message button")
        reply_btn.tap()

        # Now choose the "Forward" option
        fw_opt = self.UTILS.element.getElement(DOM.Email.reply_menu_forward, "'Forward' option button")
        fw_opt.tap()

        # Wait for 'compose message' header.
        self.parent.wait_for_element_displayed(*DOM.Email.compose_header)
        time.sleep(5)

        # Put items in the corresponding fields.
        if type(p_target) is list:
            for addr in p_target:
                self.UTILS.general.typeThis(DOM.Email.compose_to, "'To' field", addr, True, False, True, False)
                self.UTILS.general.typeThis(DOM.Email.compose_to, "'To' field", " ", True, False, True, False)
        else:
            self.UTILS.general.typeThis(DOM.Email.compose_to, "'To' field", p_target, True, False)

        # Write some reply content
        self.UTILS.general.typeThis(DOM.Email.compose_msg, "Message field", fwd_message, True, True, False, False)

        if attach:
            self.attach_file(attached_type)

        self.replyTheMessage(from_field.split("@")[0])

    def replyTheMessage(self, sender_name):
        #
        # Hits the 'Send' button to reply to the message (handles
        # waiting for the correct elements etc...).
        #

        x = self.UTILS.element.getElement(DOM.Email.compose_send_btn, "Send button")
        x.tap()

        self.UTILS.element.waitForElements(DOM.Email.compose_sending_spinner, "Sending email spinner")

        # Wait for inbox to re-appear (give it a BIG wait time because sometimes
        # it just needs it).
        self.UTILS.element.waitForNotElements(DOM.Email.compose_sending_spinner, "Sending email spinner", True, 60,
                                              False)

        # Version 2.1
        #
        # self.UTILS.element.waitForElements(DOM.Email.toaster_sending_mail, "Sending email toaster", True, 60)
        # self.UTILS.element.waitForNotElements(DOM.Email.toaster_sending_mail, "Sending email toaster", True, 60,
        #                                        False)
        # self.UTILS.element.waitForElements(DOM.Email.toaster_sent_mail, "Email sent toaster", True, 120,
        #                                       False)
        #
        x = ('xpath', DOM.GLOBAL.app_head_specific.format(sender_name))
        self.UTILS.element.waitForElements(x, "Previous received message", True, 120)

    def sendTheMessage(self):
        #
        # Hits the 'Send' button to send the message (handles
        # waiting for the correct elements etc...).
        #
        x = self.UTILS.element.getElement(DOM.Email.compose_send_btn, "Send button")
        x.tap()
        self.UTILS.element.waitForElements(DOM.Email.compose_sending_spinner, "Sending email spinner")

        # Wait for inbox to re-appear (give it a BIG wait time because sometimes
        # it just needs it).
        self.UTILS.element.waitForNotElements(DOM.Email.compose_sending_spinner, "Sending email spinner", True, 60,
                                              False)

        # Version 2.1
        #
        # self.UTILS.element.waitForElements(DOM.Email.toaster_sending_mail, "Sending email toaster", True, 60)
        # self.UTILS.element.waitForNotElements(DOM.Email.toaster_sending_mail, "Sending email toaster", True, 60,
        #                                        False)
        # self.UTILS.element.waitForElements(DOM.Email.toaster_sent_mail, "Email sent toaster", True, 120,
        #                                       False)
        x = ('xpath', DOM.GLOBAL.app_head_specific.format(_("Inbox")))
        self.UTILS.element.waitForElements(x, "Inbox", True, 120)

        return True

    def sendTheMessageAndSwitchFrame(self, header, frame_locator):
        #
        # Hits the 'Send' button to send the message (handles
        # waiting for the correct elements etc...) and switches to a specific frame
        #
        # This method comes handy when the email app is called from another app
        # (i.e Contacts, SMS...)
        #
        x = self.UTILS.element.getElement(DOM.Email.compose_send_btn, "Send button")
        x.tap()
        self.UTILS.element.waitForElements(DOM.Email.compose_sending_spinner, "Sending email spinner")

        #
        # Wait for inbox to re-appear (give it a BIG wait time because sometimes
        # it just needs it).
        #
        self.UTILS.element.waitForNotElements(DOM.Email.compose_sending_spinner, "Sending email spinner", True, 60,
                                              False)

        # Version 2.1
        #
        # self.UTILS.element.waitForElements(DOM.Email.toaster_sending_mail, "Sending email toaster", True, 60)
        # self.UTILS.element.waitForNotElements(DOM.Email.toaster_sending_mail, "Sending email toaster", True, 60,
        #                                        False)
        # self.UTILS.element.waitForElements(DOM.Email.toaster_sent_mail, "Email sent toaster", True, 120,
        #                                       False)
        #

        x = ('xpath', DOM.GLOBAL.app_head_specific.format(header))

        self.UTILS.iframe.switchToFrame(*frame_locator)
        self.UTILS.element.waitForElements(x, header, True, 120)

        return True

    def setupAccountActiveSync(self, user, email, passwd, hostname):
        #
        # Set up a new ActiveSync account manually
        #

        if not self.no_existing_account(email):
            return

        # (At this point we are now in the 'New account' screen by one path or
        # another.)
        self.UTILS.general.typeThis(DOM.Email.username, "Username field", user, True, True, False)
        self.UTILS.general.typeThis(DOM.Email.email_addr, "Address field", email, True, True, False)
        self.UTILS.general.typeThis(DOM.Email.password, "Password field", passwd, True, True, False)

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
        elem = (DOM.Email.manual_setup_account_option[0], DOM.Email.manual_setup_account_option[1].format("ActiveSync"))
        active_sync = self.UTILS.element.getElement(elem, "ActiveSync option")
        active_sync.tap()

        # Confirm
        ok_btn = self.UTILS.element.getElement(DOM.Email.manual_setup_account_type_ok, "Ok button")
        ok_btn.tap()

        # Going back to Email frame
        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)

        #  Finish setting things up
        self.UTILS.general.typeThis(DOM.Email.manual_setup_activesync_host, "Active Sync Hostname field", hostname,
                                    True, True, False)
        self.UTILS.general.typeThis(DOM.Email.manual_setup_activesync_user, "Active Sync Username field", user, True,
                                    True, False)

        time.sleep(2)
        x = self.UTILS.element.getElement(DOM.Email.manual_setup_next, "Manual Setup 'Next' button", True, 60)
        x.tap()

        time.sleep(2)
        x = self.UTILS.element.getElement(DOM.Email.login_account_prefs_next_btn, "Next button", True, 60)
        x.tap()

        # Click the 'continue to mail' button.
        time.sleep(1)
        x = self.UTILS.element.getElement(DOM.Email.login_cont_to_email_btn, "'Continue to mail' button", True, 60)
        x.tap()

        self.UTILS.element.waitForNotElements(DOM.Email.login_cont_to_email_btn, "'Continue to mail' button")

        self.UTILS.element.waitForElements(('xpath', DOM.GLOBAL.app_head_specific.format(_("Inbox"))), "Inbox")
        time.sleep(2)

    def setupAccount(self, user, email, passwd):
        #
        # Set up a new email account in the email app and login.
        #
        if not self.no_existing_account(email):
            return

        #
        # (At this point we are now in the 'New account' screen by one path or
        # another.)
        #
        self.UTILS.general.typeThis(DOM.Email.username, "Username field", user, True, True, False)
        self.UTILS.general.typeThis(DOM.Email.email_addr, "Address field", email, True, True, False)
        self.UTILS.general.typeThis(DOM.Email.password, "Password field", passwd, True, True, False)

        #
        # TODO : surround this by a try-except block, calling to quit_test. This has to be done
        # once we fix the great delay caused by viewAllIframes()
        #
        self.parent.wait_for_element_displayed(*DOM.Email.login_account_info_next_btn, timeout=60)
        nxt = self.marionette.find_element(*DOM.Email.login_account_info_next_btn)
        self.UTILS.element.simulateClick(nxt)
        self.UTILS.reporting.logResult("info", "'Next button'")

        self.parent.wait_for_element_displayed(*DOM.Email.login_account_prefs_next_btn, timeout=120)
        next2 = self.marionette.find_element(*DOM.Email.login_account_prefs_next_btn)
        # screenshot = self.UTILS.debug.screenShotOnErr()
        # self.UTILS.reporting.logResult('info', "Screenshot", screenshot)
        time.sleep(1)
        self.UTILS.element.simulateClick(next2)
        self.UTILS.reporting.logResult("info", "'Next button'")

        #
        # Click the 'continue to mail' button.
        #
        time.sleep(1)
        self.parent.wait_for_element_present(*DOM.Email.login_cont_to_email_btn, timeout=120)
        continue_btn = self.marionette.find_element(*DOM.Email.login_cont_to_email_btn)
        continue_btn.tap()
        self.UTILS.reporting.logResult("info", "'Continue to email' button")

        self.UTILS.element.waitForNotElements(DOM.Email.login_cont_to_email_btn, "'Continue to mail' button")

        self.UTILS.element.waitForElements(('xpath', DOM.GLOBAL.app_head_specific.format(_("Inbox"))), "Inbox")
        time.sleep(2)

    def setupAccountFirstStep(self, p_user, p_email, p_pass):
        #
        # Set up a new email account in the email app and login.
        # If we've just started out, email will open directly to "New Account").
        #
        if not self.no_existing_account(p_email):
            return

        #
        # (At this point we are now in the 'New account' screen by one path or
        # another.)
        #
        self.UTILS.general.typeThis(DOM.Email.username, "Username field", p_user, True, True)
        self.UTILS.general.typeThis(DOM.Email.email_addr, "Address field", p_email, True, True)
        self.UTILS.general.typeThis(DOM.Email.password, "Password field", p_pass, True, True)

    def no_existing_account(self, email):
        """Check if the new account header is present
        """

        try:
            self.parent.wait_for_element_displayed(*DOM.Email.setup_account_header)
            self.marionette.find_element(*DOM.Email.setup_account_header)
            return True
        except:
            #
            #  If exception raised --> other account has been alread set up
            #
            self.UTILS.reporting.logResult("info", "It is necessary to switch to another email account.")
            #
            # We have at least one email account setup, so
            # check to see if we can just switch to ours.
            #
            if self.switchAccount(email):
                return False

            #
            # It's not setup already, so prepare to set it up!
            #
            set_settings = self.UTILS.element.getElement(DOM.Email.settings_set_btn, "Settings set button")
            set_settings.tap()

            add_account_btn = self.UTILS.element.getElement(DOM.Email.settings_add_account_btn, "Add account button")
            time.sleep(2)
            add_account_btn.tap()
            return True

    def switchAccount(self, address):
        #
        # Add a new account.
        #
        x = self.UTILS.element.getElement(DOM.Email.settings_menu_btn, "Settings menu button")
        x.tap()

        try:
            self.UTILS.reporting.logResult("info", "First, check whether we have one account configured or MORE")
            self.parent.wait_for_element_displayed(*DOM.Email.switch_account_panel_one_account)
            self.UTILS.reporting.logResult("info", "There's only a single account configured. Time to check if\
                                                        it's necessary to do the change")
            try:
                self.parent.wait_for_element_present(*DOM.Email.switch_account_current_account)
                current_account = self.marionette.find_element(*DOM.Email.switch_account_current_account)

                #
                # Since the element is not displayed, sometimes we cannot access to the text using .text
                # This way is more secure
                #
                current_account_text = self.marionette.execute_script("return arguments[0].innerHTML", script_args=[current_account])

                self.UTILS.reporting.logResult('info', "Current account: {}".format(current_account_text))
                self.UTILS.reporting.logResult('info', "Account to switch: {}".format(address))

                screenshot = self.UTILS.debug.screenShotOnErr()
                self.UTILS.reporting.logResult('info', "Screenshot", screenshot)

                if current_account_text == address:
                    self.UTILS.reporting.logResult("info", "Already in the account we want - switch back to inbox.")
                    self.goto_folder_from_list(_("Inbox"))
                    return True
                else:
                    self.UTILS.reporting.logResult("info", "It looks like the account we want to switch is not set up yet, so we cannot switch to it")
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

            self.UTILS.reporting.logResult("info", "We're not in the account we want to be, so open the scroll to see what's there")

            self.parent.wait_for_element_displayed(*DOM.Email.switch_account_scroll)
            scroll = self.marionette.find_element(*DOM.Email.switch_account_scroll)
            scroll.tap()

            self.UTILS.reporting.logResult("info", "Now we have to iterate over all accounts displayed (but not already selected)")
            self.parent.wait_for_element_displayed(*DOM.Email.switch_account_accounts_to_change)
            accounts = self.marionette.find_elements(*DOM.Email.switch_account_accounts_to_change)

            for account in accounts:
                if account.text == address:
                    self.UTILS.reporting.logResult("info", "We got a winner. Switching to already configured account...")
                    account.tap()
                    self.UTILS.element.waitForElements(("xpath", DOM.GLOBAL.app_head_specific.format(_("Inbox"))),
                                   "Header for 'Inbox' folder")
                    return True

            self.UTILS.reporting.logResult("info", "It looks like the account we want to switch is not set up yet, so we cannot switch to it")
            return False

    def waitForDone(self):
        #
        # Wait until any progress icon goes away.
        #
        self.UTILS.element.waitForNotElements(('tag name', 'progress'), "Progress icon", True, 60);
        time.sleep(2)  # (just to be sure!)
