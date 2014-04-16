from OWDTestToolkit import DOM
import time


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
        x = self.UTILS.element.getElement(DOM.Email.delete_this_email_btn, "Delete button")
        x.tap()

        #
        # Horrific, but there's > 1 button with this id and > 1 button with this text.
        # For some reason, I can't wait_for_displayed() here either, so I have to wait for the buttons
        # to be 'present' (not 'displayed'), then look through them until I find the one I want.
        #
        x = self.UTILS.element.getElements(DOM.Email.delete_confirm_buttons, "Confirmation buttons", False, 2, False)
        for i in x:
            if i.is_displayed() and i.text == "Delete":
                self.UTILS.reporting.logResult("info", "Clicking confirmation button.")
                # (click, not tap!)
                i.click()
                break

        #
        # "1 message deleted" displayed.
        #
        x = self.UTILS.element.getElement(DOM.Email.deleted_email_notif, "Email deletion notifier")

        #
        # Refresh and check that the message is no longer in the inbox.
        #
        x = self.marionette.find_element(*DOM.Email.folder_refresh_button)
        x.tap()
        time.sleep(5)
        x = self.UTILS.element.getElements(DOM.Email.folder_subject_list, "Email messages in this folder")

        self.UTILS.test.TEST(x[0].text != subject, "Email '" + subject + "' no longer found in this folder.", False)

    def emailIsInFolder(self, subject):
        #
        # Verify an email is in this folder with the expected subject.
        #

        #
        # Because this can take a while, try to "wait_for_element..." several times (5 mins).
        #
        loops = 60
        while loops > 0:
            try:
                #
                # Look through any entries found in the folder ...
                #
                self.parent.wait_for_element_displayed(*DOM.Email.folder_subject_list, timeout=2)
                z = self.marionette.find_elements(*DOM.Email.folder_subject_list)
                pos = 0
                for i in z:
                    #
                    # Do any of the folder items match our subject?
                    #
                    if i.text == subject:
                        # Yes! But it might be off the screen, so scroll it into view.
                        # This is a bit of a hack since marionette.tap() doesn't do it
                        # (and I haven't figured out how to get the action chain to do it yet).
                        self.marionette.execute_script("document.getElementsByClassName('" + \
                                                       DOM.Email.folder_headers_list[1] + \
                                                       "')[" + str(pos) + "].scrollIntoView();")
                        self.marionette.execute_script("document.getElementsByTagName('h1')[0].scrollIntoView();")
                        time.sleep(1)

                        return i

                    pos = pos + 1

            except:
                #
                # Nothing is in the folder yet, just ignore and loop again.
                #
                pass

            #
            # Either the folder is still empty, or none of the items in it match our
            # subject yet.
            # Wait a couple for seconds and try again.
            #
            # (don't validate because this could go on for a while...)
            self.UTILS.reporting.logResult("info",
                                 "'" + subject + "' not found yet - refreshing the folder and looking again ...")
            x = self.marionette.find_element(*DOM.Email.folder_refresh_button)
            x.tap()

            time.sleep(5)

            loops = loops - 1

        return False

    def goto_folder_from_list(self, name):
        #
        # Goto a specific folder in the folder list screen.
        #
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screen shot:", x)
        x = self.UTILS.element.getElement(('xpath', DOM.Email.folderList_name_xpath.format(name)),
                                  "Link to folder '" + name + "'")
        x.tap()

        self.UTILS.element.waitForElements(("xpath", DOM.GLOBAL.app_head_specific.format(name)),
                                   "Header for '" + name + "' folder")

    def openMailFolder(self, folder_name):
        #
        # Open a specific mail folder (must be called from "Inbox").
        #
        x = self.UTILS.element.getElement(DOM.Email.settings_menu_btn, "Settings menu button")
        x.tap()

        #
        # When we're looking at the folders screen ...
        #
        self.UTILS.element.waitForElements(DOM.Email.folderList_header, "Folder list header", True, 20, False)

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
        #
        # Opens a specific email in the current folder
        # (assumes we're already in the folder we want).
        #

        myEmail = self.emailIsInFolder(subject)
        self.UTILS.test.TEST(myEmail != False, "Found email with subject '" + subject + "'.")
        if myEmail:
            #
            # We found it - open the email.
            #
            myEmail.tap()

            #
            # Check it opened.
            #
            ok = True
            try:
                self.parent.wait_for_element_displayed(*DOM.Email.open_email_from)
                ok = True
            except:
                ok = False

            return ok
        else:
            return False

    def remove_accounts_and_restart(self):
        #
        # Remove current email accounts via the UI and restart the application.
        # <br><br>
        # <b>NOTE:</b> Currently broken due to https://bugzilla.mozilla.org/show_bug.cgi?id=849183
        # so it's been set to do nothing!
        #
        return

        try:
            #
            # Make sure we're starting from the beginning ...
            # (it might not be running, so ignore any errors here).
            #
            self.marionette.kill("Email")
        except:
            pass

        self.launch()

        try:
            x = self.UTILS.element.waitForElements(("xpath", "//h1[text()='Inbox']"), "Inbox header", 10)
        except:
            #
            # We have no accounts set up (or the app would default to
            # the inbox of one of them).
            #
            self.UTILS.reporting.logResult("info", "(No email accounts set up yet.)")
            return

        x = self.UTILS.element.getElement(DOM.Email.settings_menu_btn, "Settings button")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Email.settings_set_btn, "Set settings button")
        x.tap()

        x = ('xpath', DOM.GLOBAL.app_head_specific.format("Mail Settings"))
        self.UTILS.element.waitForElements(x, "Mail settings", True, 20, False)

        #
        # Remove each email address listed ...
        #
        x = self.UTILS.element.getElements(DOM.Email.email_accounts_list,
                                   "Email accounts list", False, 20, False)
        for i in x:
            if i.text != "":
                # This isn't a placeholder, so delete it.
                self.UTILS.reporting.logComment("i: " + i.text)
                i.tap()

                x = ('xpath', DOM.GLOBAL.app_head_specific.format(i.text))
                self.UTILS.element.waitForElements(x, i.text + " header", True, 20, False)

                # Delete.
                delacc = self.UTILS.element.getElement(DOM.Email.settings_del_acc_btn, "Delete account button")
                delacc.tap()
                time.sleep(2)

                # Confirm.  <<<< PROBLEM (on forums)!
                delconf = self.UTILS.element.getElement(DOM.Email.settings_del_conf_btn, "Confirm delete button")
                delconf.tap()

                # Wait for this dialog to go away, then sleep for 1s.

        #
        # Now relaunch the app.
        #
        self.launch()

    def send_new_email(self, p_target, p_subject, p_message):
        #
        # Compose and send a new email.
        #
        x = self.UTILS.element.getElement(DOM.Email.compose_msg_btn, "Compose message button")
        x.tap()

        #
        # Wait for 'compose message' header.
        #
        x = self.UTILS.element.getElement(('xpath', DOM.GLOBAL.app_head_specific.format("Compose")),
                                  "Compose message header")

        #
        # Put items in the corresponsing fields.
        #
        self.UTILS.general.typeThis(DOM.Email.compose_to, "'To' field", p_target, True, False)
        self.UTILS.general.typeThis(DOM.Email.compose_subject, "'Subject' field", p_subject, True, False)
        self.UTILS.general.typeThis(DOM.Email.compose_msg, "Message field", p_message, True, False, False)

        self.sendTheMessage()

    def sendTheMessage(self):
    #
        # Hits the 'Send' button to send the message (handles
        # waiting for the correct elements etc...).
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

        x = ('xpath', DOM.GLOBAL.app_head_specific.format("Inbox"))
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

        x = ('xpath', DOM.GLOBAL.app_head_specific.format(header))

        self.UTILS.iframe.switchToFrame(*frame_locator)
        self.UTILS.element.waitForElements(x, header, True, 120)

        return True

    def setupAccount(self, user, email, passwd):
        #
        # Set up a new email account in the email app and login.
        #

        #
        # If we've just started out, email will open directly to "New Account").
        #
        x = self.UTILS.element.getElement(DOM.GLOBAL.app_head, "Application header")
        if x.text.lower() != "new account":
            #
            # We have at least one emali account setup,
            # check to see if we can just switch to ours.
            #
            if self.switchAccount(email):
                return

            #
            # It's not setup already, so prepare to set it up!
            #
            x = self.UTILS.element.getElement(DOM.Email.settings_set_btn, "Settings set button")
            x.tap()

            x = self.UTILS.element.getElement(DOM.Email.settings_add_account_btn, "Add account button")
            x.tap()

        #
        # (At this point we are now in the 'New account' screen by one path or
        # another.)
        #
        self.UTILS.general.typeThis(DOM.Email.username, "Username field", user, True, True)
        self.UTILS.general.typeThis(DOM.Email.email_addr, "Address field", email, True, True)
        self.UTILS.general.typeThis(DOM.Email.password, "Password field", passwd, True, True)

        self.parent.lockscreen.unlock()
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)

        #
        # (doesn't always appear when using hotmail)
        #
        try:
            self.parent.wait_for_element_displayed(*DOM.Email.login_next_btn, timeout=5)
            btn = self.marionette.find_element(*DOM.Email.login_next_btn)
            btn.tap()
        except:
            pass

        time.sleep(2)
        x = self.UTILS.element.getElement(DOM.Email.login_next_btn, "'Next' button", True, 60)
        x.tap()

        time.sleep(2)
        x = self.UTILS.element.getElement(DOM.Email.login_next_btn, "'Next' button", True, 60)
        x.tap()

        #
        # Click the 'continue to mail' button.
        #
        time.sleep(1)
        x = self.UTILS.element.getElement(DOM.Email.login_cont_to_email_btn, "'Continue to mail' button", True, 60)
        x.tap()

        self.UTILS.element.waitForNotElements(DOM.Email.login_cont_to_email_btn, "'Continue to mail' button")

        self.UTILS.element.waitForElements(('xpath', DOM.GLOBAL.app_head_specific.format('Inbox')), "Inbox")
        time.sleep(2)

    def setupAccountFirstStep(self, p_user, p_email, p_pass):
        #
        # Set up a new email account in the email app and login.
        #

        #
        # If we've just started out, email will open directly to "New Account").
        #
        x = self.UTILS.element.getElement(DOM.GLOBAL.app_head, "Application header")
        if x.text.lower() != "new account":
            #
            # We have at least one emali account setup,
            # check to see if we can just switch to ours.
            #
            if self.switchAccount(p_email):
                return

            #
            # It's not setup already, so prepare to set it up!
            #
            x = self.UTILS.element.getElement(DOM.Email.settings_set_btn, "Settings set button")
            x.tap()

            x = self.UTILS.element.getElement(DOM.Email.settings_add_account_btn, "Add account button")
            x.tap()

        #
        # (At this point we are now in the 'New account' screen by one path or
        # another.)
        #
        self.UTILS.general.typeThis(DOM.Email.username, "Username field", p_user, True, True)
        self.UTILS.general.typeThis(DOM.Email.email_addr, "Address field", p_email, True, True)
        self.UTILS.general.typeThis(DOM.Email.password, "Password field", p_pass, True, True)

        self.parent.lockscreen.unlock()
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)

        #
        # (doesn't always appear when using hotmail)
        #
        try:
            self.parent.wait_for_element_displayed(*DOM.Email.login_next_btn, timeout=5)
            btn = self.marionette.find_element(*DOM.Email.login_next_btn)
            btn.tap()
        except:
            pass

    def switchAccount(self, address):
        #
        # Add a new account.
        #
        x = self.UTILS.element.getElement(DOM.Email.settings_menu_btn, "Settings menu button")
        x.tap()

        #
        # Are we already in this account?
        #
        x = self.UTILS.element.getElement(DOM.GLOBAL.app_head, "Header")
        self.UTILS.reporting.logResult("info",
                            "Currently using email account '{}' (looking to be in account '{}').".\
                            format(x.text, address))
        if x.text == address:
            self.UTILS.reporting.logResult("info", "Already in the account we want - switch back to inbox.")
            self.goto_folder_from_list("Sent Mail")
            return True

        self.UTILS.reporting.logResult("info", "Need to switch from account '{}' to account '{}' ...".\
                             format(x.text, address))

        #
        # We're not in this account already, so let's look for it.
        #
        x = self.UTILS.element.getElement(DOM.Email.goto_accounts_btn, "Accounts button")
        x.tap()

        x = ('xpath', DOM.GLOBAL.app_head_specific.format("Accounts"))
        self.UTILS.element.waitForElements(x, "Accounts header", True, 20, False)

        #
        # Check if it's already set up (this may be empty, so don't test for this element).
        #
        try:
            self.parent.wait_for_element_present(*DOM.Email.accounts_list_names, timeout=2)
            time.sleep(1)
            x = self.marionette.find_elements(*DOM.Email.accounts_list_names)
            for i in x:
                if i.text != "":
                    if i.text == address:
                        i.tap()
                        self.goto_folder_from_list("Sent Mail")
                        return True
        except:
            pass

        #
        # It's not setup yet, so we couldn't switch.
        #
        return False

    def waitForDone(self):
        #
        # Wait until any progress icon goes away.
        #
        self.UTILS.element.waitForNotElements(('tag name', 'progress'), "Progress icon", True, 60);
        time.sleep(2)  # (just to be sure!)
