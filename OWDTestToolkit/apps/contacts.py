import time
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.decorators import retry
from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()


class Contacts(object):

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

    def add_gallery_image_to_contact(self, num):
        """
        Adds an image for this contact from the gallery
        (assumes we're already in the 'new contact' or
        'edit conact' screen, and also that we have already
        added an image to the gallery).
        """

        # Click the 'add picture' link.
        x = self.UTILS.element.getElement(DOM.Contacts.add_photo, "'Add picture' link")
        x.tap()

        # Switch to the 'make a choice' iframe.
        self.marionette.switch_to_frame()

        # Choose to get a picture from the Gallery.
        elem = (DOM.GLOBAL.action_menu_option[0], DOM.GLOBAL.action_menu_option[1].format("Gallery"))
        gallery_option = self.UTILS.element.getElement(elem, "Gallery link")
        gallery_option.tap()

        # Switch to Gallery iframe.
        self.UTILS.iframe.switchToFrame(*DOM.Gallery.frame_locator)
        self.UTILS.element.waitForNotElements(DOM.Gallery.loading_bar, "Loading bar", True, 10)

        # Select the thumbnail (assume it's the only one).
        thumbnails = self.UTILS.element.getElements(DOM.Contacts.picture_thumbnails, "Thumbnails for pictures")
        if thumbnails:
            thumbnails[num].tap()
            time.sleep(1)
            # Tap 'crop done' button.
            boolOK = True
            try:
                crop_done_btn = self.UTILS.element.getElement(DOM.Contacts.picture_crop_done_btn, "Crop 'done' button")
                crop_done_btn.tap()
            except:
                boolOK = False

            self.UTILS.test.test(boolOK, "Can finish cropping the picture and return to Contacts app.")

        # Back to contacts app iframe.
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

    def add_another_email_address(self, email_address):
        """
        Add a new email address to the contact currnetly being viewed in Edit mode.
        """
        add_email_button = self.UTILS.element.getElement(DOM.Contacts.add_email_button, "Add email button")
        add_email_button.tap()

        # (Marionette currently messes up the screen, so correct this.)
        self.marionette.execute_script("document.getElementsByTagName('h1')[0].scrollIntoView();")

        # Add the email.
        fields = self.UTILS.element.getElements(DOM.Contacts.email_fields, "Email fields", False, 2)
        for field in fields:
            if field.get_attribute("value") == "":
                field.send_keys(email_address)

                # (if there's a "_" in the email address, the screen will lock.)
                if "_" in email_address:
                    orig_frame = self.UTILS.iframe.currentIframe()
                    self.lockscreen.unlock()
                    self.marionette.switch_to_frame()
                    self.UTILS.iframe.switchToFrame("src", orig_frame)
                break

    def change_contact(self, contact_name, field, value):
        """
        Change a value for a contact (assumes we're looking at the 'all contacts' screen
        currently).
        """
        # View our contact.
        self.view_contact(contact_name)

        # Press the edit button.
        self.press_edit_contact_button()

        # Change the name to "aaaaabbbbbccccaaaa"
        contFields = self.get_contact_fields()
        self.replace_str(contFields[field], value)

        # Save the changes
        update_btn = self.UTILS.element.getElement(DOM.Contacts.edit_update_button, "Edit 'update' button")
        update_btn.tap()

        # Return to the contact list screen.
        back_btn = self.UTILS.element.getElement(DOM.Contacts.details_back_button, "Details 'back' button")
        time.sleep(1)
        back_btn.tap()

        self.UTILS.element.waitForElements(DOM.Contacts.view_all_header, "'View all contacts' screen header")

    def check_edit_contact_details(self, contact):
        """
        Validate the details of a contact in the 'view contact' screen.

        @contact must be an object in the same format as the
        one in ./example/tests/mock_data/contacts.py.
        """
        self.press_edit_contact_button()

        # Correct details are in the contact fields.
        self.verify_field_contents(contact)

    def check_match(self, element, value, name):
        """
        Test for a match between an element and a string
        (found I was doing this rather a lot so it's better in a function).
        """
        test_str = str(element.get_attribute("value"))
        self.UTILS.test.test((test_str == value), name + " = \"" + value + "\" (it was \"" + test_str + "\").")

    def check_search_results(self, contact_name, present=True):
        """
        Checks the results of a search() to see
        if the contact is present or not (depending
        on the 'present' setting).
        """

        # Verify our contact is all that's displayed in the result list.
        results = self.marionette.find_elements(*DOM.Contacts.search_results_list)
        boolContact = False
        for result in results:
            if contact_name in result.text:
                boolContact = True

        msg = (" is " if present else " is not ") + "displayed in the result list."

        self.UTILS.test.test(present == boolContact, "Contact '" + contact_name + "'" + msg)

    def check_view_contact_details(self, contact, check_image=False):
        """
        Validate the details of a contact in the 'view contact' screen.
        <br><br>
        <b>contact</b> must be an object in the same format as the
        one in ./example/tests/mock_data/contacts.py.
        """

        # Go to the view details screen for this contact.
        self.view_contact(contact['name'])
        if check_image:

            # Verify that an image is displayed.
            boolOK = False
            try:
                self.parent.wait_for_element_displayed(*DOM.Contacts.view_contact_image, timeout=1)
                image = self.marionette.find_element(*DOM.Contacts.view_contact_image)
                attrs = ["style", "data-img-hash", "data-photo-ready"]
                boolOK = all(image.get_attribute(attr) is not None for attr in attrs)
            except:
                pass

            self.UTILS.test.test(boolOK, "Contact's image contains a picture in contact details screen.")

        # Correct details are in the contact fields.
        self.verify_field_contents(contact, True)

    def count_email_addresses_while_editing(self):
        """
        Count the emails and return the number - assumes you
        are currently EDITING the contact (not viewing).
        """

        # (for some reason these are flagged as not displayed, so
        # you have to get them as 'present').
        fields = self.UTILS.element.getElements(DOM.Contacts.email_fields, "Email fields", False, 2)
        self.UTILS.reporting.logResult("info", "NOTE: Contact's email addresses:")
        counter = 0
        for field in fields:
            if field.get_attribute("value") != "#value#":
                counter = counter + 1
                self.UTILS.reporting.logResult("info", "    - " + str(counter) + ": " + field.get_attribute("value"))
        return counter

    def create_contact(self, contact, img_src=False):
        """
        Create a new contact with a image (if specified).
        img_src is either "gallery" or "camera" (or left undefined).
        <br><br>
        <b>contact</b> must be an object in the same format as the
        one in ./example/tests/mock_data/contacts.py.
        """
        self.start_create_new_contact()

        if img_src == "gallery":
            self.add_gallery_image_to_contact(0)

        self.populate_contact_fields(contact)

    def delete_contact(self, fullname, header_check=True):
        """
        Deletes a contact.<br>
        fullname must match the name displayed
        in the 'view all contacts' screen (including spaces).
        """

        # Make sure we are in the contacts app.
        try:
            self.parent.wait_for_element_displayed("xpath", "//h1[text() = '{}']".format(_("Contacts")), timeout=1)
        except:
            self.launch()

        self.view_contact(fullname, header_check)
        self.press_edit_contact_button()
        self.press_delete_contact_button()

        # Confirm deletion.
        confirm_btn = self.UTILS.element.getElement(DOM.Contacts.confirm_delete_btn, "Confirm deletion button")
        confirm_btn.tap()

        # Now verify that this contact is no longer present (or no search field if
        # this was the only contact).
        contact_el = ("xpath", DOM.Contacts.view_all_contact_xpath.format(fullname.replace(" ", "")))
        self.UTILS.element.waitForNotElements(contact_el, "Contact name in 'all contacts' screen")

    def edit_contact(self, name, contact):
        """
        Replace the details of one contact with another via the edit screen.

        <b>p_contact_curr_json_obj</b> and <b>contact</b> must
        be objects in the same format as the one in
        ./example/tests/mock_data/contacts.py (however, only needs the
        'name' component is used from the p_contact_curr_json_obj).
        """

        # Go to the view details screen for this contact.
        self.view_contact(name)

        edit_btn = self.UTILS.element.getElement(DOM.Contacts.edit_details_button, "Edit details button")
        edit_btn.tap()
        self.UTILS.element.waitForElements(DOM.Contacts.edit_contact_header, "'Edit contacts' screen header")

        # Enter the new contact details and save the changes
        self.populate_fields(contact)

        # Save the changes
        update_btn = self.UTILS.element.getElement(DOM.Contacts.edit_update_button, "Edit 'update' button")
        update_btn.tap()

        # Return to the contact list screen.
        back_btn = self.UTILS.element.getElement(DOM.Contacts.details_view_header, "Details 'back' button")
        back_btn.tap(25, 25)

        self.UTILS.element.waitForElements(DOM.Contacts.view_all_header, "'View all contacts' screen header")

    def enable_FB_import(self):
        """
        Enable fb import.
        """

        enable_switch = self.UTILS.element.getElement(DOM.Contacts.settings_fb_enable, "Enable facebook button")
        enable_switch.tap()
        time.sleep(1)

        # Were we already connected to facebook?
        boolFound = False
        try:
            self.parent.wait_for_element_displayed('xpath', "//button[text()='{}']".format(_("Remove")), timeout=5)
            boolFound = True
        except:
            pass

        if boolFound:
            self.UTILS.reporting.logResult("info", "Logging out of facebook so I can re-enable the FB import ...")
            remove_btn = self.UTILS.element.getElement(
                ('xpath', "//button[text()='{}']".format(_("Remove"))), "Remove button")
            remove_btn.tap()

            self.UTILS.element.waitForElements(DOM.Contacts.settings_fb_logout_wait, "FB logout message", True, 5)
            self.UTILS.element.waitForNotElements(DOM.Contacts.settings_fb_logout_wait, "FB logout message", True, 60)

            self.marionette.switch_to_frame()
            self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

            enable_switch = self.UTILS.element.getElement(DOM.Contacts.settings_fb_enable, "Enable facebook button")
            enable_switch.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

    def _export(self, locator, msg):
        settings_btn = self.UTILS.element.getElement(DOM.Contacts.settings_button, "Settings button")
        settings_btn.tap()

        export_btn = self.UTILS.element.getElement(DOM.Contacts.export_contacts, "Export button")
        export_btn.tap()

        # Press the option
        export_option_btn = self.UTILS.element.getElement(locator, "Export {}".format(msg))
        self.UTILS.test.test(export_option_btn.get_attribute(
            "disabled") == "false", "{} button is enabled.".format(msg))
        time.sleep(1)
        export_option_btn.tap()

    def export_bluetooth(self):
        """
        Press the Settings button, then Bluetooth
        """
        self._export(DOM.Contacts.export_bluetooth, "Bluetooth")

    def export_sd_card(self):
        """
        Press the Settings button, then memory card
        """
        self._export(DOM.Contacts.export_sd_card, "SD card")

    def export_sim_card(self):
        """
        Presses the Settings button, then SIM card
        """
        self._export(DOM.Contacts.export_sim_card, "SIM card")

    def export_contacts_to_sim_card_by_position(self, positions):
        self.select_contacts_by_position(positions)
        export_button = self.UTILS.element.getElement(DOM.Contacts.export, "Export action button")
        export_button.tap()

    def select_contacts_by_position(self, positions):
        """
            Selects some contacts in "Edition Mode"
        """
        contact_list = self.UTILS.element.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        for pos in positions:
            contact_list[pos].tap()

    def get_contact_fields(self, view=False):
        """
        Return 3-d array of contact details.
        if view is set, it will use the DOM specs for the view screen. Otherwise
        it will assume you are in the edit screen.
        """
        if view:
            return {
                'name': self.UTILS.element.getElement(DOM.Contacts.view_details_title, "Name in title field", True, 5, False),
                'tel': self.UTILS.element.getElement(DOM.Contacts.view_contact_tel_field, "Phone number field", True, 5, False),
                'email': self.UTILS.element.getElement(DOM.Contacts.view_contact_email_field, "Email field", True, 5, False),
                'address': self.UTILS.element.getElement(DOM.Contacts.view_contact_address, "Address field", True, 5, False),
            }
        else:
            # Locate and press the 'Add Address' button
            add_btn = self.UTILS.element.getElement(DOM.Contacts.add_address_button, "Add Address button")
            self.UTILS.element.scroll_into_view(add_btn)
            add_btn.tap()
            return {
                'givenName': self.UTILS.element.getElement(DOM.Contacts.given_name_field, "Given name field", True, 5, False),
                'familyName': self.UTILS.element.getElement(DOM.Contacts.family_name_field, "Family name field", True, 5, False),
                'tel': self.UTILS.element.getElement(DOM.Contacts.phone_field, "Phone number field", True, 5, False),
                'email': self.UTILS.element.getElement(DOM.Contacts.email_field, "Email field", True, 5, False),
                'street': self.UTILS.element.getElement(DOM.Contacts.street_field, "Street field", True, 5, False),
                'zip': self.UTILS.element.getElement(DOM.Contacts.zip_code_field, "Zip code field", True, 5, False),
                'city': self.UTILS.element.getElement(DOM.Contacts.city_field, "City field", True, 5, False),
                'country': self.UTILS.element.getElement(DOM.Contacts.country_field, "Country field", True, 5, False),
            }

    @retry(5, 5)
    def switch_to_gmail_login_frame(self):
        self.marionette.switch_to_frame()
        gmail_frame = self.marionette.find_element(*DOM.Contacts.gmail_frame)
        result = self.marionette.switch_to_frame(gmail_frame)
        self.UTILS.reporting.debug("**** Switched to gmail frame: {}".format(result))

    def import_gmail_login(self, name, passwd, click_signin=True):
        """
        Presses the Settings button, then Gmail, then logs in using
        name and passwd (to begin the process of importing contacts).
        <br>
        If click_signin is set to True then this method will also click
        the Sign in button (defaults to true).
        <br>
        Returns False if the login failed, else True.
        """

        self.UTILS.reporting.logResult("info", "Logging in with '{}'/'{}'.".format(name, passwd))

        settings_btn = self.UTILS.element.getElement(DOM.Contacts.settings_button, "Settings button")
        settings_btn.tap()

        import_btn = self.UTILS.element.getElement(DOM.Contacts.import_contacts, "Import button")
        # import_btn.tap()
        self.UTILS.element.simulateClick(import_btn)

        # Press the Gmail button.
        import_gmail_btn = self.UTILS.element.getElement(DOM.Contacts.gmail_button, "Gmail button")
        time.sleep(1)
        import_gmail_btn.tap()

        """
        Sometimes the device remembers your login from before (even if the device is
        reset and all data cleared), so check for that.
        self.switch_to_gmail_login_frame()
        """
        self.UTILS.iframe.switch_to_frame("data-url", "google")
        try:
            time.sleep(2)
            self.UTILS.element.waitForNotElements(DOM.Contacts.import_throbber, "Animated 'loading' indicator")

            # Send the login information (the email field isn't always displayed).
            self.parent.wait_for_element_displayed(*DOM.Contacts.gmail_password, timeout=30)
            try:
                self.parent.wait_for_element_displayed(*DOM.Contacts.gmail_username, timeout=5)

                username_field = self.UTILS.element.getElement(DOM.Contacts.gmail_username, "Username field")
                username_field.send_keys(name)
            except:
                pass

            passwd_field = self.UTILS.element.getElement(DOM.Contacts.gmail_password, "Password field")
            passwd_field.send_keys(passwd)

            if click_signin:
                signin_btn = self.UTILS.element.getElement(DOM.Contacts.gmail_signIn_button, "Sign In button")
                time.sleep(1)
                self.UTILS.element.simulateClick(signin_btn)

                # Check to see if sigin failed. If it did then stay here.
                try:
                    self.parent.wait_for_element_displayed(*DOM.Contacts.gmail_login_error_msg, timeout=2)

                    screenshot = self.UTILS.debug.screenShotOnErr()
                    self.UTILS.reporting.logResult("info", "<b>Login failed!</b> Screenshot and details:", screenshot)
                    return False
                except:
                    pass

                self.check_gmail_permissions()
            else:
                return True
        except:
            self.UTILS.reporting.logResult("info", "<b>Already logged in</b>")
            self.check_gmail_permissions()
            pass

        time.sleep(5)

        # Journey back to the import iframe.
        txt = "<b>(NOTE: we've had some problems here - if this iframe switch fails " + \
              "then check at the 'root-level' iframe screenshot for an error message.)</b>"
        self.UTILS.reporting.logResult("info", txt)
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.gmail_import_frame, via_root_frame=False)

        self.UTILS.element.waitForElements(DOM.Contacts.import_conts_list, "Contacts list", False, 2)
        return True

    def check_gmail_permissions(self):
        """
        PERMISSIONS (sometimes appears).
        Seems to happen a few times, so loop through 5 just in case ...
        """
        for i in range(5):
            try:
                self.parent.wait_for_element_displayed(*DOM.Contacts.gmail_permission_accept, timeout=2)

                permission_accept = self.marionette.find_element(*DOM.Contacts.gmail_permission_accept)
                permission_accept.tap()

                self.UTILS.reporting.logResult('info', "Gmail permissions accepted")
                time.sleep(5)
                break
            except:
                self.UTILS.reporting.logResult('info', "Checking permissions once again")

    def import_hotmail_login(self, name, passwd, click_signin=True, just_signin=False):
        """
        Presses the Settings button in the contacts app, then Hotmail, then logs in using
        name and passwd (to begin the process of importing contacts).
        <br>
        If click_signin is set to True then this method will also click
        the Sign in button (defaults to true).
        <br>
        Returns False if the login failed, True otherwise.
        """

        settings_btn = self.UTILS.element.getElement(DOM.Contacts.settings_button, "Settings button")
        settings_btn.tap()

        self.parent.wait_for_element_displayed(*DOM.Contacts.import_contacts, timeout=30)
        import_btn = self.UTILS.element.getElement(DOM.Contacts.import_contacts, "Import button")
        time.sleep(1)
        import_btn.tap()

        # Press the Hotmail button.
        x = self.UTILS.element.getElement(DOM.Contacts.hotmail_button, "Hotmail button")
        time.sleep(1)
        x.tap()

        # Login.
        login_success = self.hotmail_login(name, passwd, click_signin)
        if not login_success:
            return False

        if not click_signin or just_signin:
            # If we're just entering the login details but not clicking sign in,
            # then here's where we finish.
            return True

        # Go to the hotmail import iframe.
        self.UTILS.reporting.logResult('info', "Doing the switch to contacts......")
        time.sleep(2)

        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult('info', "Screenshot before switching", screenshot)
        return True

    @retry(5, 5)
    def switch_to_hotmail_login_frame(self):
        self.marionette.switch_to_frame()
        hotmail_sign_in = self.marionette.find_element(*DOM.Contacts.hotmail_signin_frame)
        result = self.marionette.switch_to_frame(hotmail_sign_in)
        self.UTILS.reporting.debug("**** Switched to hotmail frame: {}".format(result))

    def hotmail_login(self, name, passwd, click_signin):
        """
        Sometimes the device remembers your login from before (even if the device is
        reset and all data cleared), so check for that.
        """

        self.UTILS.reporting.logResult("info", "Entering hotmail_login ...")
        try:
            self.UTILS.iframe.switch_to_frame("data-url", "live")
            try:
                self.UTILS.element.waitForNotElements(DOM.Contacts.import_throbber, "Animated 'loading' indicator")

                """
                Send the login information (sometimes the username isn't required, just the password).
                I 'know' that the password field will appear though, so use that element to get the
                timing right.
                """
                self.parent.wait_for_element_displayed(*DOM.Contacts.hotmail_password, timeout=30)
                try:
                    self.parent.wait_for_element_displayed(*DOM.Contacts.hotmail_username, timeout=2)

                    user_input = self.marionette.find_element(*DOM.Contacts.hotmail_username)
                    user_input.send_keys(name)
                except Exception as e:
                    self.UTILS.reporting.logResult('info', "[hotmail_username]: {}".format(e))

                passwd_input = self.UTILS.element.getElement(DOM.Contacts.hotmail_password, "Password field")
                passwd_input.send_keys(passwd)

                if click_signin:
                    signin_btn = self.UTILS.element.getElement(DOM.Contacts.hotmail_signIn_button, "Sign In button")
                    self.UTILS.element.simulateClick(signin_btn)

                    # Check to see if sign in failed. If it did then return False.
                    try:
                        self.marionette.switch_to_frame()
                        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
                        self.parent.wait_for_element_displayed("id", "fb-curtain", timeout=10)
                        self.UTILS.reporting.debug("*** Login succeeded!")
                    except:
                        self.UTILS.reporting.debug("*** Login failed! Returning False")
                        return False
            except Exception as e:
                self.UTILS.reporting.logResult('info', "[Throbber]: {}".format(e))
        except Exception as e:
            self.UTILS.reporting.logResult('info', "[Switch to hotmail frame]: {}".format(e))
        return True

    def is_contact_a_favorite(self, element=None):
        """
        Checks is a certain contact has been added as favorite
        It assumes it is already the contact_view
        """

        fav_button = element or self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Favourite toggle button")
        classes = fav_button.get_attribute("class").split()
        try:
            classes.index("on")
            return True
        except ValueError:
            return False

    def hotmail_check_permissions(self, passwd):
        """
        @deprecated
        Sometimes hotmail asks for permission - just accept it if it's there.
        """

        try:
            self.UTILS.reporting.debug("*** Entering hotmail_check_permissions")
            self.marionette.start_session()
            self.parent.wait_for_element_displayed(*DOM.Contacts.hotmail_permission_accept, timeout=2)
            self.UTILS.reporting.debug(">>> Finding element hotmail_permission_accept")
            x = self.marionette.find_element(*DOM.Contacts.hotmail_permission_accept)
            x.tap()
            self.UTILS.reporting.debug(">>> Get element hotmail password")
            x = self.UTILS.element.getElement(DOM.Contacts.hotmail_password, "Password field")
            x.send_keys(passwd)
            self.UTILS.reporting.debug(">>> Get element hotmail sign in button")
            x = self.UTILS.element.getElement(DOM.Contacts.hotmail_signIn_button, "Sign In button")
            x.tap()
            self.UTILS.reporting.debug(">>> Wait for not elements import throbber")
            self.UTILS.element.waitForNotElements(DOM.Contacts.import_throbber, "Animated 'loading' indicator")
            self.UTILS.reporting.debug(">>> Ending checking hotmail permissions")
        except Exception as e:
            self.UTILS.reporting.debug("*** Error checking hotmail permissions: {}".format(e))

    def check_all_friends_imported(self):
        """
        Check to see if the message "All your friends are imported" is being displayed.
        """

        all_imported = False
        try:
            # For some reason this is needed before the message can be seen!
            screenshot = self.UTILS.debug.screenShotOnErr()
            self.parent.wait_for_element_displayed(*DOM.Contacts.import_all_imported_msg, timeout=2)
            all_imported = True
        except:
            pass

        if all_imported:
            self.UTILS.reporting.logResult("info",
                                           "<b>NOTE:</b> Apparently all your friends are already imported - " +
                                           "see the following screenshots for details", screenshot)

            self.marionette.execute_script("document.getElementById('{}').click()".
                                           format(DOM.Contacts.import_close_icon[1]))
            time.sleep(1)

            # Switch back to the contacts app frame and wait for the hotmail frame to go away.
            self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
            time.sleep(1)

            # Close the settings screen.
            settings_done_button = self.UTILS.element.getElement(
                DOM.Contacts.settings_done_button, "Contacts app settings 'done' button")
            settings_done_button.tap()

            # Record the contacts we currently have imported (in case this test fails and this is why).
            self.UTILS.element.waitForElements(DOM.Contacts.view_all_header, "All contacts main screen", True, 2)

            screenshot = self.UTILS.debug.screenShotOnErr()
            self.UTILS.reporting.logResult("info",
                                           "<b>NOTE:</b> Apparently all your friends are imported from hotmail. " +
                                           "These are the contacts you have in the Contacts app:", screenshot)
            return True
        else:
            return False

    def import_all(self):
        """
        Assumes you're already in the gmail import screen (after logging in etc...).
        """

        self.UTILS.reporting.logResult("info", "Tapping the 'Select All' button ...")
        self.marionette.execute_script("document.getElementById('{}').click()".
                                       format(DOM.Contacts.import_select_all[1]))
        time.sleep(1)

        self.marionette.execute_script("document.getElementById('{}').click()".
                                       format(DOM.Contacts.import_import_btn[1]))
        time.sleep(1)
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

    def import_toggle_select_contact(self, num):
        """
        Toggles select / de-select a gmail contact( marionette doesn't work here yet, so use JS).
        num is the actualt contact number (1 -> x).
        """
        el_num = num - 1

        x = self.UTILS.element.getElements(DOM.Contacts.import_conts_list, "Contact list")
        cont_name = x[el_num].get_attribute("data-search")

        self.UTILS.reporting.logResult("info", "Selecting contact {} ('{}') ...".format(num, cont_name))

        self.marionette.execute_script("document.getElementsByClassName('block-item')[{}].click()".format(el_num))

        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of current position", screenshot)

    def populate_contact_fields(self, contact):
        """
        Put the contact details into each of the fields.
        <br><br>
        <b>contact</b> must be an object in the same format as the
        one in ./example/tests/mock_data/contacts.py.
        """

        self.populate_fields(contact)

        # Press the 'done' button and wait for the 'all contacts' page to load.
        done_button = self.UTILS.element.getElement(DOM.Contacts.done_button, "'Done' button")
        done_button.tap()

        # Wait for the 'view all contacts' header to be displayed.
        self.UTILS.element.waitForElements(DOM.Contacts.view_all_header, "View all contacts header")

        # Now check the contact's name is displayed here too.
        contact_name = ("xpath", DOM.Contacts.view_all_contact_xpath.format(contact['name'].upper().\
                                                                            replace(" ", "")))

        self.UTILS.element.waitForElements(contact_name, "Contact '{}'".format(contact['name'].upper().\
                                                                               replace(" ", "")), timeout=30)

    def populate_fields(self, contact):
        """
        Put the contact details into the fields (assumes you are in the correct
        screen already since this could be create or edit).
        <br><br>
        <b>contact</b> must be an object in the same format as the
        one in ./example/tests/mock_data/contacts.py.
        """

        contFields = self.get_contact_fields()
        """
        Put the contact details into each of the fields (this method
        clears each field first).
        """
        self.replace_str(contFields['givenName'], contact["givenName"])
        self.replace_str(contFields['familyName'], contact["familyName"])
        self.replace_str(contFields['tel'], contact["tel"]["value"])
        self.replace_str(contFields['email'], contact["email"]["value"])
        self.replace_str(contFields['street'], contact["addr"]["streetAddress"])
        self.replace_str(contFields['zip'], contact["addr"]["postalCode"])
        self.replace_str(contFields['city'], contact["addr"]["locality"])
        self.replace_str(contFields['country'], contact["addr"]["countryName"])

    def press_cancel_edit_button(self):
        """
        Presses the Edit contact button when vieweing a contact.
        """
        edit_cancel_button = self.UTILS.element.getElement(DOM.Contacts.edit_cancel_button, "Cancel edit button")
        edit_cancel_button.tap()
        self.UTILS.element.waitForElements(DOM.Contacts.view_details_title, "'View contact details' title")

    def press_delete_contact_button(self):
        """
        In it's own function just to save time figuring out
        that you have to get the button into view before you
        can press it, then re-align the screen again.
        """
        self.marionette.execute_script("document.getElementById('" +
                                       DOM.Contacts.delete_contact_btn[1] +
                                       "').scrollIntoView();")
        self.marionette.execute_script("document.getElementById('settings-button').scrollIntoView();")
        delete_contact_btn = self.UTILS.element.getElement(
            DOM.Contacts.delete_contact_btn, "Delete contacts button", False)
        delete_contact_btn.tap()

    def press_edit_contact_button(self):
        """
        Presses the Edit contact button when vieweing a contact.
        """
        edit_btn = self.UTILS.element.getElement(DOM.Contacts.edit_details_button, "Edit details button")
        edit_btn.tap()
        self.UTILS.element.waitForElements(DOM.Contacts.edit_contact_header, "'Edit contact' screen header")

    def replace_str(self, field, value):
        """
        Replace text in a field (as opposed to just appending to it).
        """
        field.clear()
        field.send_keys(value)

        # Tap outside the field, so that we exit its edition
        header = self.marionette.find_element("xpath", '//h1[@id="contact-form-title"]')
        header.tap()

        self.check_match(field, value, "After replacing the string, this field now")

    def search(self, value):
        """
        Searches the 'all contacts' screen for value
        (assumes we're currently in the 'all contacts' screen).
        """

        # Tap the search area.
        search_field = self.UTILS.element.getElement(DOM.Contacts.search_field, "Search field")
        search_field.tap()

        self.UTILS.general.typeThis(DOM.Contacts.search_contact_input, "Search input", value,
                                    p_no_keyboard=True, p_validate=False, p_clear=False, p_enter=False)

    def select_search_result(self, contact_name):
        """
        Select the result of a search
        """
        results = self.UTILS.element.getElements(DOM.Contacts.search_results_list, "Search results list")
        for result in results:
            if contact_name in result.text:
                result.tap()
                break

    def call_current_contact(self):
        """Call the contact being shown after selecting from contact list or search results.
        """
        call_btn = self.UTILS.element.getElement(DOM.Contacts.view_contact_tel_field, "Contact number button")
        call_btn.tap()

    def select_search_result_several_phones(self, contact_name, number, cancel=False):
        """
        Select the result of a search.

        Select the contact with the given name from the search results, and then,
        select the given number.
        If cancel is True, the number is not selected, and the Cancel button is pressed instead.
        """
        results = self.UTILS.element.getElements(DOM.Contacts.search_results_list, "Search results list", True, 10)
        for result in results:
            if contact_name in result.text:
                result.tap()
                break

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        btn = None
        if cancel:
            btn = self.UTILS.element.getElement((DOM.Contacts.select_recipient_btn[0],
                                             DOM.Contacts.select_recipient_btn[1].format("Cancel")),
                                             "Cancel Select number button")
        else:
            btn = self.UTILS.element.getElement((DOM.Contacts.select_recipient_btn[0],
                                             DOM.Contacts.select_recipient_btn[1].format(number + " ")),
                                             "Select number button")
        btn.tap()

    def start_create_new_contact(self):
        """
        Open the screen to add a contact.
        """

        # First make sure we're in the right place.
        viewAllHeader = self.UTILS.element.getElement(
            DOM.Contacts.view_all_header, "'View all contacts' header", False)
        if not viewAllHeader.is_displayed():
            # Header isn't present, so we're not running yet.
            self.launch()

        # Click Create new contact from the view all screen.
        self.UTILS.element.waitForElements(DOM.Contacts.view_all_header, "View all contacts header")
        add_new_contact = self.UTILS.element.getElement(DOM.Contacts.add_contact_button, "'Add new contact' button")

        add_new_contact.tap()

        # Enter details for new contact.
        self.UTILS.element.waitForElements(DOM.Contacts.add_contact_header, "Add contact header")

    def switch_to_facebook(self):
        """
        <i>Private</i> function to handle the iframe hop-scotch involved in
        finding the facebook app launched via contacts app.
        """
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        # self.UTILS.iframe.switchToFrame(*DOM.Contacts.settings_fb_frame, via_root_frame=False)
        frame = self.marionette.find_element(*DOM.Contacts.settings_fb_frame)
        self.marionette.switch_to_frame(frame)

        # Wait for the fb page to start.
        self.UTILS.element.waitForElements(DOM.Facebook.friends_header, "Facebook friends header")

    def tapLinkContact(self):
        """
        Press the 'Link contact' button in the view contact details screen.
        NOTE: there is more than one button with this ID, so make sure we use the right one!
        (One of them isn't visible, so we need to check for visibility this way or the
        'invisible' one will cause 'getElements()' to fail the test).
        """
        self.UTILS.element.getElement(DOM.Contacts.link_button, "Link contact button").tap()
        self.switch_to_facebook()
        time.sleep(5)

    def tapSettingsButton(self):
        settings_btn = self.UTILS.element.getElement(DOM.Contacts.settings_button, "Settings button")
        self.UTILS.element.simulateClick(settings_btn)

        self.UTILS.element.waitForElements(DOM.Contacts.settings_header, "Settings header")

    def view_test(self, desc, str1, str2):
        self.UTILS.test.test(str1 in str2, "{} field contains '{}' (it was '{}').".format(desc, str1, str2))

    def verify_field_contents(self, contact, view=False):
        """
        Verify the contents of the contact fields in this screen (assumes
        you are in the correct screen since this could be view or edit).
        <br><br>
        <b>contact</b> must be an object in the same format as the
        one in ./example/tests/mock_data/contacts.py.<br>
        <b>view</b> selects whether this is the 'view contact' screen or not (defaults to False -> edit screen).
        """
        contFields = self.get_contact_fields(view)

        if view:
            self.view_test("Name", contact['name'], contFields['name'].text)
            self.view_test("Telephone", contact['tel']['value'], contFields['tel'].text)
            self.view_test("Email", contact['email']['value'], contFields['email'].text)
            self.view_test("Street", contact['addr']['streetAddress'], contFields['address'].text)
            self.view_test("Post code", contact['addr']['postalCode'], contFields['address'].text)
            self.view_test("Locality", contact['addr']['locality'], contFields['address'].text)
            self.view_test("Country", contact['addr']['countryName'], contFields['address'].text)

        else:
            self.check_match(contFields['givenName'], contact['givenName'], "Given name")
            self.check_match(contFields['familyName'], contact['familyName'], "Family name")
            self.check_match(contFields['tel'], contact['tel']['value'], "Telephone")
            self.check_match(contFields['email'], contact['email']['value'], "Email")
            self.check_match(contFields['street'], contact['addr']['streetAddress'], "Street")
            self.check_match(contFields['zip'], contact['addr']['postalCode'], "Zip")
            self.check_match(contFields['city'], contact['addr']['locality'], "City")
            self.check_match(contFields['country'], contact['addr']['countryName'], "Country")

    def verify_image_in_all_contacts(self, contact_name):
        """
        Verify that the contact's image is displayed.
        """
        contact_list = self.UTILS.element.getElements(DOM.Contacts.view_all_contact_list, "Contact list", False)
        for contact in contact_list:
            if contact_name.replace(" ", "") == contact.get_attribute("data-order"):
                isImage = True
                try:
                    img = contact.find_element("xpath", "//span[@data-type='img']")
                    self.UTILS.test.test("blob" in img.get_attribute(
                        "data-src"), "Contact image present in 'all contacts' screen.")
                except:
                    self.UTILS.reporting.logResult(
                        "Cannot find img tag in contact. Contact data: {}".format(contact.text))
                    isImage = False

                self.UTILS.test.test(isImage, "An image is present for this contact in all contacts screen.")

    def verify_linked(self, contact_name, fb_email):
        """
        Verifies that this contact is linked with a facebook account
        """
        button = self.UTILS.element.getElement(DOM.Contacts.link_button, "Link contact button")
        linked = button.get_attribute("data-fb_is_linked")
        self.UTILS.test.test(linked == "true", "Contact is linked: {}".format(linked))

    def view_contact(self, contact_name, header_check=True):
        """
        Navigate to the 'view details' screen for a contact (assumes we are in the
        'view all contacts' screen, either from Contacts app, or Dialer app).
        <br>
        In some cases you don't want this to check the header (if the contact has no name,
        or you're just using the given name etc..). In that case, set header_check=False.

        Because this can be called from several applications (contacts, dialer, sms ...), finding
        the right iframe can be tricky, which is why "self.find_frame()" is here.
        """
        self._orig = self.UTILS.iframe.currentIframe()

        self.find_frame()

        all_contacts = self.UTILS.element.getElements(
            DOM.Contacts.view_all_contact_list, "All contacts list", False, 10)

        self.UTILS.reporting.logResult("info", u"{} contacts listed.".format(len(all_contacts)))
        found = False
        for i in range(len(all_contacts)):
            self.UTILS.reporting.logResult("info", u"'{}'".format(all_contacts[i].text))
            if contact_name.lower() in all_contacts[i].text.lower():
                found = True
                self.UTILS.reporting.logResult(
                    "info", u"Contact '{}' found in all contacts - selecting this contact ...".format(contact_name))
                self.marionette.execute_script("document.getElementsByClassName('contact-item')[{}].click()".format(i))
                break

            self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator, quit_on_error=False)
            all_contacts = self.UTILS.element.getElements(
                DOM.Contacts.view_all_contact_list, "All contacts list", False)

        if not found:
            self.UTILS.reporting.logResult("info", u"FYI: Contact '{}' was <b>not</b> found in the contacts list.".
                                           format(contact_name))
            return

        # test: Correct contact name is in the page header.

        if header_check:
            self.UTILS.element.headerCheck(contact_name)

        frame = self.find_frame()

        if frame == "Dialer":
            details_title = self.UTILS.element.getElement(DOM.Contacts.view_details_title, "View details title")
            self.UTILS.test.test(contact_name in details_title.text, "Name is in the title")

    def find_frame(self):
        """
        Private method to cater for the fact that *SOMETIMES* the
        frame is different if coming from Dialer.
        """
        self.marionette.switch_to_frame()
        x = self.try_frame(DOM.Dialer.frame_locator)
        if x:
            x = self.try_frame(DOM.Dialer.call_log_contact_name_iframe)
            if x:
                self.UTILS.reporting.logResult("info", "<i>Switched to dialer -> contacts iframe.)</i>")
                return "Dialer"

        self.marionette.switch_to_frame()
        x = self.try_frame(DOM.Contacts.frame_locator)
        if x:
            return "Contacts"

        self.marionette.switch_to_frame()
        x = self.try_frame(DOM.Messages.frame_locator)
        if x:
            return "Messages"

        self.marionette.switch_to_frame()
        x = self.try_frame(["src", self._orig])
        return "Unknown"

    def try_frame(self, dom):
        """
        Private function to return an object for the many types of 'return iframes'.
        """
        try:
            iframe = ("xpath", "//iframe[contains(@{},'{}')]".format(dom[0], dom[1]))
            self.parent.wait_for_element_present(*iframe, timeout=2)
            x = self.marionette.find_element(*iframe)
            self.marionette.switch_to_frame(x)
            return True
        except:
            return False

    def go_back(self):
        """Press back button in the contacts list scren
        """
        # TODO: remove tap with coordinates after Bug 1061698 is fixed
        self.UTILS.element.getElement(DOM.Contacts.search_contact_header, "Back button").tap(25, 25)
