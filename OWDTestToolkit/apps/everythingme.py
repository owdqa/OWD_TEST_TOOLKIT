from OWDTestToolkit import DOM
from marionette import Actions
import time


class EverythingMe(object):

    def __init__(self, p_parent):
        self.apps = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.parent = p_parent
        self.marionette = p_parent.marionette
        self.UTILS = p_parent.UTILS
        self.actions = Actions(self.marionette)

    def launch(self):
        #
        # Launch the app.
        #
        self.UTILS.home.goHome()

        #
        # If EME has already been launched, then the DOM has changed.
        #
        self.UTILS.reporting.logResult("info", "Launching Everything ME.")
        boolOK = False
        try:
            self.parent.wait_for_element_displayed(*DOM.EME.start_eme_icon, timeout=1)
            x = self.marionette.find_element(*DOM.EME.start_eme_icon)
            x.tap()
            boolOK = True
        except:
            self.UTILS.reporting.logResult("info", "Everything ME is already 'running', so just waking it up ...")
            self._relaunch()
            try:
                self.parent.wait_for_element_displayed(*DOM.EME.groups, timeout=3)
            except:
                self._relaunch()
            boolOK = True

        self.UTILS.test.TEST(boolOK, "EME Starting up ...")

    def _relaunch(self):
        #
        # Private function to re-launch.
        # This gets complicated:
        # 1. el.tap() and el.click() only work *sometimes*, so use the keyboard to relaunch.
        # 2. Sometimes the messges app randomly launches instead of evme!
        #
        x = self.marionette.find_element(*DOM.EME.search_field)
        x.send_keys("waking up evme")

        x = self.marionette.find_element(*DOM.EME.search_clear)
        x.tap()

    def add_app_to_homescreen(self, name):
        #
        # Pick an app from the apps listed in this group.
        #
        x = self.UTILS.element.getElements(DOM.EME.app_to_install, "The first game that is not installed already")[0]
        APP_NAME = x.get_attribute("data-name")
        self.UTILS.reporting.logResult("debug", "icon displayed: {}".format(x.is_displayed()))

        self.UTILS.test.TEST(APP_NAME == name, "" + APP_NAME + "'is the correct app", True)

        actions = Actions(self.marionette)
        actions.press(x).wait(2).release()
        try:
            actions.perform()
        except:
            pass

        x = self.UTILS.element.getElement(DOM.EME.add_app_to_homescreen, "Add app to homescreen button")
        x.tap()

        return True

    def add_group(self, group):
        #
        # Adds a group to EME (assumes you're already in the EME group screen).
        #
        self.UTILS.reporting.logResult("info", "(Adding group '" + group + "'.)")

        #
        # Click the 'More' icon.
        #
        x = self.UTILS.element.getElement(DOM.EME.add_group_button, "'More' icon")
        x.tap()

        #
        # Wait for the 'loading' spinner to go away (can take a while!).
        #
        self.UTILS.element.waitForNotElements(DOM.EME.loading_groups_message, "'Loading' message", True, 120)

        #
        # Chose an item from the groups list...
        #
        self.UTILS.general.selectFromSystemDialog(group)

        #
        # Verify the new group is in the groups list.
        #
        x = self.UTILS.element.getElements(DOM.EME.groups, "Groups")
        boolOK = False
        for i in x:
            if i.get_attribute("data-query") == group:
                boolOK = True
                break

        self.UTILS.test.TEST(boolOK, "New group '" + group + "' is now present in the EME groups.")
        return boolOK

    def add_multiple_groups(self, group_array=False):
        #
        # Adds multiple groups based on an array of numbers (defaults to all available groups).
        # <br><br>
        # For example: add_multiple_groups([0,1,2,3,8,11]) ... or just: add_multiple_groups()
        #
        x = self.UTILS.element.getElement(DOM.EME.add_group_button, "'More' icon")
        x.tap()
        self.UTILS.element.waitForNotElements(DOM.EME.loading_groups_message, "'Loading' message", True, 120)

        #
        # Switch to group selector (in top level iframe).
        #
        self.marionette.switch_to_frame()

        # for checking later
        list_names = []
        elements = self.UTILS.element.getElements(DOM.GLOBAL.modal_valueSel_list, "Groups list", False)

        for i in range(len(elements)):
            if i > 0:
                # Keep shuffling the groups into view so they can be tapped.
                self.actions.press(elements[i]).move(elements[i - 1]).wait(0.5).release().perform()
                elements = self.marionette.find_elements(*DOM.GLOBAL.modal_valueSel_list)

            #
            # Only select it if it's the list, or there is no list.
            #
            select_elements = False
            if group_array:
                if len(group_array) == len(list_names):
                    #
                    # We've done all of them - stop looping!
                    break
                if i in group_array:
                    select_elements = True
            else:
                select_elements = True

            if select_elements:
                tmp_name = elements[i].find_element("tag name", "span").text
                self.UTILS.reporting.logResult("info", "Selecting '{}' ...".format(tmp_name))
                list_names.append(tmp_name)
                elements[i].tap()

                #
                # Sometimes the first tap does nothing for some reason.
                #
                if not elements[i].get_attribute("aria-checked"):
                    elements[i].tap()

        #
        # Click the OK button.
        #
        x = self.UTILS.element.getElement(DOM.GLOBAL.modal_valueSel_ok, "OK button")
        try:
            # Sometimes it's one, sometimes the other ...
            x.tap()
            x.click()
        except:
            pass

        time.sleep(1)

        #
        # Checkk all the items we expect are now loaded in evme.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)
        time.sleep(5)
        for name in list_names:
            ok = False

            # Reload the groups (silently or we'll have loads of these messages!).
            try:
                x = self.marionette.find_elements(*DOM.EME.groups)
            except:
                break

            for i in x:
                group_name = i.get_attribute("data-query")
                if group_name == name:
                    ok = True
                    break

            self.UTILS.test.TEST(ok, "'{}' is now among the groups.".format(name))

    def bookmark_app(self, app_name):
        #
        # 'Bookmarks' (installs) an app from EME (assumes everything.me is already running).
        #
        x = self.search_for_app(app_name)
        if not x:
            #
            # No point going beyond this point.
            #
            return False

        x.tap()

        self.marionette.switch_to_frame()
        self.UTILS.element.waitForElements(DOM.EME.launched_button_bar, "Button bar", False)

        #
        # Wait for the bookmark option to be enabled (can take a few seconds).
        #
        boolOK = False
        for i in range(10):
            x = self.marionette.find_element(*DOM.EME.launched_button_bookmark)
            if not x.get_attribute("data-disabled"):
                boolOK = True
                break

            time.sleep(6)

        x = self.UTILS.element.getElement(DOM.EME.launched_display_button_bar, "Button bar 'displayer' element")
        x.tap()

        self.UTILS.test.TEST(boolOK, "Bookmark button is enabled in the button bar.", True)

        time.sleep(1)

        x = self.UTILS.element.getElement(DOM.EME.launched_button_bookmark, "Button bar - bookmark button")
        self.UTILS.test.TEST(not x.get_attribute("data-disabled"), "Bookmark button is enabled.", True)
        x.tap()

        self.marionette.switch_to_frame()
        _boolOK = False
        x = self.UTILS.element.getElements(DOM.EME.launched_add_to_homescreen, "Apps to be added to homescreen")
        for i in x:
            if i.text == app_name:
                i.tap()
                _boolOK = True
                break

        self.UTILS.test.TEST(_boolOK, "Adding '{}' to homescreen (app selected).".format(app_name))

        self.UTILS.iframe.switchToFrame(*DOM.EME.add_to_home_screen_frame)
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point:", x)

        x = self.UTILS.element.getElement(DOM.EME.add_to_home_screen_btn, "Add to homescreen (button)")
        x.tap()

        self.marionette.switch_to_frame()
        x = self.UTILS.element.getElement(DOM.EME.launched_display_button_bar, "Button bar 'displayer' element")
        x.tap()

        x = self.UTILS.element.getElement(DOM.EME.launched_button_bookmark, "Button bar - bookmark button")
        self.UTILS.test.TEST(x.get_attribute("data-disabled") == "true", "Bookmark button is now disabled.")

        self.UTILS.test.TEST(self.UTILS.findAppIcon(app_name), "'{}' is now installed.".format(app_name))

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of the button bar:", x)
        return True

    def launch_from_group(self, app_name):
        #
        # Function to launch an app directly from an EME group.
        #
        x = self.UTILS.element.getElement(("xpath", "//li[@data-name='{}']".format(app_name)),
                                  "Icon for app '{}'".format(app_name), False)
        try:
            x.tap()
        except:
            #
            # App is not visible, so I need to move it into view first.
            #
            _id = x.get_attribute("_id")
            self.marionette.execute_script("document.getElementById('{}').scrollIntoView();".format(_id))
            x.tap()

        time.sleep(1)
        self.UTILS.element.waitForNotElements(DOM.EME.launched_activity_bar, "Activity notifier", True, 30)

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of app running:", x)

    def pick_group(self, name):
        #
        # Pick a group from the main icons.
        #
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "<b>Choosing group '{}' from here ...</b>".format(name), x)

        ok = False

        x = self.marionette.find_element('css selector', DOM.Home.app_icon_css.format(name))
        self.UTILS.reporting.logResult("debug", "icon displayed: {}".format(x.is_displayed()))
        x.tap()

        try:
            self.parent.wait_for_element_displayed(*DOM.EME.apps_not_installed, timeout=20)
            self.UTILS.reporting.logResult("info", "(Apps for group {} were displayed.)".format(name))
            ok = True
        except:
            x = self.UTILS.debug.screenShotOnErr()
            self.UTILS.reporting.logResult("info", "(<b>NOTE:</b>Apps for group {} were not displayed.)|{}|{}".\
                                 format(name, x[0], x[1]))

        return ok

    def remove_groups(self, group_array):
        #
        # Removes groups from the EME group page.<br>
        # <b>group_array</p> is an array of group names (default = all groups).<br>
        # <br>
        # For example: <i> remove_groups(["Games","Local"])
        #

        #
        # Put the groups into edit mode.
        # Sometimes this takes a while to happen, so increase the length
        # of time you press the icon until it works!
        #
        ok = False
        x = self.marionette.find_element('css selector', DOM.Home.app_icon_css.format(group_array[0]))
        actions = Actions(self.marionette)
        actions.press(x).wait(3).release()
        try:
            actions.perform()
        except:
            pass

        try:
            x = self.UTILS.element.getElement(("xpath", DOM.Home.app_delete_icon_xpath.format(group_array[0])),
                                      "Delete button", False, 5, True)
            if x.is_displayed():
                ok = True
        except:
            pass

            time.sleep(2)

        self.UTILS.test.TEST(ok, "Enabled EDIT mode.")
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of app in EDIT mode:", x)

        #
        # Remove all groups in the array.
        #
        removed = 0
        group_cnt = len(group_array)

        self.UTILS.reporting.logResult("info", "Removing {} groups".format(group_cnt))
        self.UTILS.reporting.logResult("info", "Removing groups: {}".format(group_array))

        for group_specified in group_array:
            #
            # Remove it.
            #
            self.marionette.find_element('css selector', DOM.Home.app_icon_css.format(group_specified))
            y = self.UTILS.element.getElement(("xpath", DOM.Home.app_delete_icon_xpath.format(group_specified)),
                                      "Delete button", False, 5, True)
            y.tap()

            delete = self.UTILS.element.getElement(DOM.Home.app_confirm_delete, "Confirm app delete button")
            delete.tap()
            removed = removed + 1
            self.UTILS.reporting.logResult("info", "Removed group '{}' ...".format(group_specified))
            self.UTILS.reporting.logResult("info", "Removed {} groups".format(removed))
            if removed == group_cnt:
                break

        #
        # Turn off edit mode.
        #
        self.UTILS.reporting.logResult("info", "Disabling edit mode ...")
        self.UTILS.home.touchHomeButton()

    def search_for_app(self, name):
        #
        # Uses the search field to find the app (waits for the
        # result to appear etc...).<br>
        # Returns the element for the icon (or False if it's not found).
        #
        x = self.UTILS.element.getElement(DOM.EME.search_field, "Search field")
        x.clear()
        x.send_keys(name)
        x.click()
        time.sleep(5)

        #
        # Can take a few seconds to appear, so try a few times (about 1 min).
        #
        for retry in range(10):
            x = self.UTILS.debug.screenShotOnErr()
            self.UTILS.reporting.logResult("debug", "Looking for '{}' - attempt {} ...".format(name, retry), x)

            x = self.UTILS.element.getElements(DOM.EME.search_suggestions, "Search suggestions")
            ok = False
            for i in x:
                i_name = i.get_attribute("data-suggestion")
                if i_name:
                    i_name = i_name.lower()
                    i_name = i_name.replace("[", "")
                    i_name = i_name.replace("]", "")
                    is_in = False
                    for i2 in name.lower().split():
                        self.UTILS.reporting.logResult("debug", "Is '{}' in '{}'?".format(i2, i_name))
                        if i2 not in i_name:
                            is_in = False
                            break
                        else:
                            is_in = True
                    if is_in:
                        i.tap()
                        ok = True
                        break
            if ok:
                break

            time.sleep(6)

        self.UTILS.test.TEST(ok, "Found '%s' in suggestions." % name)

        ok = True
        try:
            elem = ("xpath", DOM.EME.search_result_icon_xpath.format(name))
            self.parent.wait_for_element_displayed(*elem, timeout=60)
            x = self.marionette.find_element(*elem)
            return x
        except:
            ok = False

        return ok
