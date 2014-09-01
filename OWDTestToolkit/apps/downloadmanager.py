import re
import time
from OWDTestToolkit import DOM
from marionette import Actions
from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()


class DownloadManager(object):

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS

    def _check_button_status(self, locator, button_type, attribute, desired_value, return_button=False):
        """
        Checks a certain button status
        """
        button = self.UTILS.element.getElement(locator, "Getting '{button_type}' button")
        self.UTILS.test.TEST(button.get_attribute(attribute) == desired_value,
                             'Checking "{}" button is "{}"'.format(button_type, desired_value))
        if return_button:
            return button

    def _enter_edit_mode(self):
        """
        Enter into Edit Mode
        """
        edit_mode = self.UTILS.element.getElement(DOM.DownloadManager.download_edit_button,
                                                  "Getting download edit button", True, 10)
        edit_mode.tap()
        self.UTILS.element.waitForElements(DOM.DownloadManager.downloads_edit_header_title,
                                           "Getting edit downloads header")

    def get_download_entry(self, data_url):
        elem = (DOM.DownloadManager.download_element[0],
                DOM.DownloadManager.download_element[1].format(data_url))
        return self.UTILS.element.getElement(elem, "Obtain the download entry")

    def get_download_state(self, data_url):
        download_entry = self.get_download_entry(data_url)
        return download_entry.get_attribute("data-state")

    def verify_download_status(self, data_url, status):
        self.UTILS.test.TEST(self.get_download_state(data_url) == status,
                             "The download entry {} has the state: {}".format(data_url, status))

    def clean_downloads_list(self):
        """
        Wipes the download list (NOTE, first it has to be opened from settings)
        """
        time.sleep(3)
        x = self.marionette.find_elements(*DOM.DownloadManager.download_list_elems)
        self.UTILS.reporting.debug("*** Download list: {}   Length: {}".format(x, len(x)))

        if not x or len(x) == 0:
            self.UTILS.reporting.logResult("info", "Downloads list is empty, it's not necessary delete any file")
        else:
            self.UTILS.reporting.logResult("info", "Downloads list is not empty, it's necessary delete some files")
            self.delete_all_downloads()

    def delete_all_downloads(self):
        """
            Selects all downloads and wipes them
        """
        self._enter_edit_mode()

        # Verify "Select All button" is enabled and "Deselect All" is disabled
        select_all = self._check_button_status(
            DOM.DownloadManager.download_select_all, "Select All", "disabled", "false", return_button=True)
        self._check_button_status(DOM.DownloadManager.download_deselect_all, "Deselect All", "disabled", "true")

        # Select all downloads
        select_all.tap()
        time.sleep(1)

        # Verify that now "Deselect All" button is enabled and "Select All"
        # button is disabled
        self._check_button_status(DOM.DownloadManager.download_select_all, "Select All", "disabled", "true")
        self._check_button_status(DOM.DownloadManager.download_deselect_all, "Deselect All", "disabled", "false")

        delete_btn = self.UTILS.element.getElement(DOM.DownloadManager.download_delete_button, "Getting Delete button")
        delete_btn.tap()

        confirm_btn = self.UTILS.element.getElement(DOM.DownloadManager.download_confirm_yes, "Getting Confirm button")
        confirm_btn.tap()
        # self.UTILS.element.simulateClick(x)

        # Verify no downloads are present
        no_downloads = self.UTILS.element.getElement(
            DOM.DownloadManager.download_empty_list_content, "Getting empty list content")
        self.UTILS.test.TEST(no_downloads.text == _(
            "No downloads"), "Verifying '{}' message is displayed".format(_("No downloads")))

    def delete_download(self, data_url):
        """
        Deletes a single download from the downloads list
        """

        self._enter_edit_mode()

        entry_locator = (DOM.DownloadManager.download_element[0],
                         DOM.DownloadManager.download_element[1].format(data_url))
        entry = self.UTILS.element.getElementByXpath(entry_locator[1])
        self.UTILS.element.simulateClick(entry)

        delete_btn = self.UTILS.element.getElement(DOM.DownloadManager.download_delete_button, "Getting Delete button")
        self.UTILS.element.simulateClick(delete_btn)

        confirm_btn = self.UTILS.element.getElement(DOM.DownloadManager.download_confirm_yes, "Getting Confirm button")
        self.UTILS.element.simulateClick(confirm_btn)

        # TODO - CONFIRMATION!!!! - We will add a new parameter, called 'confirm'
        # and wait for a confirmation popup.... like in stop_download and restart_download

        # Wait for download to be deleted
        self.UTILS.element.waitForNotElements(entry_locator, "Download item from downloads list", timeout=5)

    def download_file(self, file_name):
        #
        # Start the file download
        # TODO - This works for our test page. Try to generalize a lil' bit
        #

        link = self.UTILS.element.getElement(('css selector', 'a[href="{}"]'.format(file_name)),
                                             'The file [{}] to download'.format(file_name), True, 10)
        link.tap()

    def is_file_downloading(self, data_url):
        """
        Checks whether the file is downloading in the downloads list
        """

        #
        # Sometimes it takes too long to load the list
        #
        self.parent.wait_for_element_displayed(DOM.DownloadManager.download_list[0],
                                               DOM.DownloadManager.download_list[1], 60)
        return self.get_download_state(data_url) == "downloading"

    def open_download(self, data_url):
        download_entry = self.get_download_entry(data_url)
        download_entry.tap()

    def restart_download(self, download_id, confirm):

        #
        # Restarts a download that was previously stopped, if <confirm> = True
        #

        #
        # Tap on a stopped Download by download_id
        #
        elem = (DOM.DownloadManager.download_element_button[0],
                DOM.DownloadManager.download_element_button[1] % download_id)
        x = self.UTILS.element.getElement(elem, "Getting download item refresh button")
        x.tap()

        #
        # Verify if we must press yes or no button
        #
        if confirm:
            #
            # Press Try again button to restart the download
            #
            x = self.UTILS.element.getElement(DOM.DownloadManager.download_confirm_yes,
                                              "Restart the download tapping on Try again button")
            x.tap()

            #
            # Verify text during the download process (graphically)
            #
            elem = (DOM.DownloadManager.download_status_text[0],
                    DOM.DownloadManager.download_status_text[1] % download_id)
            x = self.UTILS.element.getElement(elem,
                                              "Obtain the text displayed to verify the text 'X' MB of 'Y' MB")

            match = re.search(r"(\d)+(.(\d)+)*\s(GB|MB|KB)\sof\s(\d)+(.(\d)+)*\s(GB|MB|KB)",
                              x.text)
            self.UTILS.test.TEST(match is not None, "Verify the the text is: 'X' MB of 'Y' MB")

            #
            # Verify status downloading using data-state="downloading".
            #
            elem = (DOM.DownloadManager.download_status_text[0],
                    DOM.DownloadManager.download_status[1] % download_id)
            x = self.UTILS.element.getElement(elem, "Obtain the download state")
            self.UTILS.test.TEST("downloading" == x.get_attribute("data-state"),
                                 "Verify that the status is downloading")

        else:
            #
            # Press cancel button and the download still stopped
            #
            x = self.UTILS.element.getElement(DOM.DownloadManager.download_confirm_no,
                                              "Press cancel button and the download still stopped")
            x.tap()

            #
            # Verify text Stopped.
            #
            elem = (DOM.DownloadManager.download_status_text[0],
                    DOM.DownloadManager.download_status_text[1] % download_id)
            x = self.UTILS.element.getElement(elem,
                                              "Obtain the text displayed to verify the text stopped")
            self.UTILS.test.TEST("Stopped" in x.text, "Verify the text Stopped")

            #
            # Verify status Stopped using data-state="stopped".
            #
            elem = (DOM.DownloadManager.download_status_text[0], DOM.DownloadManager.download_status[1] % download_id)
            x = self.UTILS.element.getElement(elem, "Obtain the download state")
            self.UTILS.test.TEST("stopped" == x.get_attribute("data-state"),
                                 "Verify that the status is stopped")

    def stop_download_by_position(self, position, confirm):
        # Stops a download in progress if <confirm> = True
        #

        #
        # Tap in Stopping Download by download_id
        #
        elem = (DOM.DownloadManager.download_element_button_position[0],
                DOM.DownloadManager.download_element_button_position[1].format(position))
        x = self.UTILS.element.getElement(elem, "Get element by position")
        x.tap()

        #
        # Verify if we must press yes or no button
        #
        if confirm:
            #
            # Press Yes button and Confirm Stop Download.
            #
            x = self.UTILS.element.getElement(DOM.DownloadManager.download_confirm_yes,
                                              "Confirm Stop Download, Yes button")
            x.tap()

            #
            # Verify text Stopped.
            #
            elem = (DOM.DownloadManager.download_status_text_position[0],
                    DOM.DownloadManager.download_status_text_position[1].format(position))
            x = self.UTILS.element.getElement(elem,
                                              "Obtain the text displayed to verify the text stopped")
            self.UTILS.test.TEST("Stopped" in x.text, "Verify the text Stopped")

            #
            # Verify status Stopped using data-state="stopped".
            #
            elem = (DOM.DownloadManager.download_status_position[
                    0], DOM.DownloadManager.download_status_position[1].format(position))
            x = self.UTILS.element.getElement(elem, "Obtain the download state")
            self.UTILS.test.TEST("stopped" == x.get_attribute("data-state"),
                                 "Verify the status stopped")

        else:
            #
            # Press No button and Cancel Stop Download
            #
            x = self.UTILS.element.getElement(DOM.DownloadManager.download_confirm_no,
                                              "Confirm Stop Download, Yes button")
            x.tap()

            #
            # Verify text during the download process.
            #

            elem = (DOM.DownloadManager.download_status_text_position[0],
                    DOM.DownloadManager.download_status_text_position[1].format(position))
            x = self.UTILS.element.getElement(elem,
                                              "Obtain the text displayed to verify the text 'X' MB of 'Y' MB")

            pattern = r"^(\d)+(.(\d)+)*\s(GB|MB|KB)\sof\s(\d)+(.(\d)+)*\s(GB|MB|KB)$"
            match = re.search(pattern, x.text)
            self.UTILS.test.TEST(match is not None, "Verify the text is : 'X' MB of 'Y' MB")

            #
            # Verify status downloading using data-state="downloading".
            #
            elem = (DOM.DownloadManager.download_status_position[
                    0], DOM.DownloadManager.download_status_position[1].format(position))
            x = self.UTILS.element.getElement(elem, "Obtain the download state")
            self.UTILS.test.TEST("downloading" == x.get_attribute("data-state"),
                                 "Verify that the status is downloading")

    def stop_download(self, download_id, confirm):

        #
        # Stops a download in progress if <confirm> = True
        #

        #
        # Tap in Stopping Download by download_id
        #
        elem = (DOM.DownloadManager.download_element_button[0],
                DOM.DownloadManager.download_element_button[1] % download_id)
        x = self.UTILS.element.getElement(elem, "Get element by id")
        x.tap()

        #
        # Verify if we must press yes or no button
        #
        if confirm:
            #
            # Press Yes button and Confirm Stop Download.
            #
            x = self.UTILS.element.getElement(DOM.DownloadManager.download_confirm_yes,
                                              "Confirm Stop Download, Yes button")
            x.tap()

            #
            # Verify text Stopped.
            #
            elem = (DOM.DownloadManager.download_status_text[0],
                    DOM.DownloadManager.download_status_text[1] % download_id)
            x = self.UTILS.element.getElement(elem,
                                              "Obtain the text displayed to verify the text stopped")
            self.UTILS.test.TEST("Stopped" in x.text, "Verify the text Stopped")

            #
            # Verify status Stopped using data-state="stopped".
            #
            elem = (DOM.DownloadManager.download_status_text[0], DOM.DownloadManager.download_status[1] % download_id)
            x = self.UTILS.element.getElement(elem, "Obtain the download state")
            self.UTILS.test.TEST("stopped" == x.get_attribute("data-state"),
                                 "Verify the status stopped")

        else:
            #
            # Press No button and Cancel Stop Download
            #
            x = self.UTILS.element.getElement(DOM.DownloadManager.download_confirm_no,
                                              "Confirm Stop Download, Yes button")
            x.tap()

            #
            # Verify text during the download process.
            #
            elem = (DOM.DownloadManager.download_status_text[0],
                    DOM.DownloadManager.download_status_text[1] % download_id)
            x = self.UTILS.element.getElement(elem,
                                              "Obtain the text displayed to verify the text 'X' MB of 'Y' MB")

            pattern = r"^(\d)+(.(\d)+)*\s(GB|MB|KB)\sof\s(\d)+(.(\d)+)*\s(GB|MB|KB)$"
            match = re.search(pattern, x.text)
            self.UTILS.test.TEST(match is not None, "Verify the text is : 'X' MB of 'Y' MB")

            #
            # Verify status downloading using data-state="downloading".
            #
            elem = (DOM.DownloadManager.download_status_text[0], DOM.DownloadManager.download_status[1] % download_id)
            x = self.UTILS.element.getElement(elem, "Obtain the download state")
            self.UTILS.test.TEST("downloading" == x.get_attribute("data-state"),
                                 "Verify that the status is downloading")
