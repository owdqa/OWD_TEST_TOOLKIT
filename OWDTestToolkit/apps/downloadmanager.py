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
        self.UTILS.test.test(button.get_attribute(attribute) == desired_value,
                             'Checking "{}" button is "{}={}"'.format(button_type, attribute, desired_value))
        if return_button:
            return button

    def _enter_edit_mode(self):
        """
        Enter into Edit Mode
        """
        edit_mode = self.UTILS.element.getElement(DOM.DownloadManager.download_edit_button,
                                                  "Download edit button", True, 10)
        edit_mode.tap()
        self.UTILS.element.waitForElements(DOM.DownloadManager.downloads_edit_header_title,
                                           "Edit downloads header")

    def _unable_open_option(self):
        """
        Select open option when tap on a non-recognized file
        """
        self.tap_on_open_option()

        unable_msg = self.UTILS.element.getElement(DOM.DownloadManager.download_confirm_h1, "Unable to open msg")
        self.UTILS.test.test(unable_msg.text == _("Unable to open"), "Unable to open msg")

    def _tap_on_confirm_button(self, yes=True, msg="Confirm dialog button"):
        """
        Taps on confirmation buttons
        """
        btn = self.UTILS.element.getElement(DOM.DownloadManager.download_confirm_yes if
                                            yes else DOM.DownloadManager.download_confirm_no, msg)
        btn.tap()

    def get_download_entry(self, data_url):
        elem = (DOM.DownloadManager.download_element[0],
                DOM.DownloadManager.download_element[1].format(data_url))
        return self.UTILS.element.getElement(elem, "Download entry for file: {}".format(data_url.split("/")[-1]))

    def get_download_status(self, data_url):
        download_entry = self.get_download_entry(data_url)
        return download_entry.get_attribute("data-state")

    def verify_download_status(self, data_url, status):
        self.UTILS.test.test(self.get_download_status(data_url) == status,
                             "The download entry {} has the state: {}".format(data_url, status))

    def get_download_info(self, data_url):
        """
        Gets the info <p> of the a certain download entry_locator
        """
        elem = (DOM.DownloadManager.download_entry_info[0],
                DOM.DownloadManager.download_entry_info[1].format(data_url))
        return self.UTILS.element.getElement(elem, "Obtain the info for: {}".format(data_url))

    def get_download_progress(self, data_url):
        elem = (DOM.DownloadManager.download_element_progress[0],
                DOM.DownloadManager.download_element_progress[1].format(data_url))

        progress = self.UTILS.element.getElement(elem, "Getting downloaded file [{}]'s progress".format(data_url))
        if progress:
            value = progress.get_attribute("value")
            return int(value)

    def verify_download_graphical_status(self, data_url, status):
        """
        Verify text during the download process (graphically)
        """

        download_info = self.get_download_info(data_url)
        self.UTILS.reporting.logResult('info', 'The status [element_text] is: {}'.format(download_info.text))
        self.UTILS.reporting.logResult('info', 'The status [parameter] is: {}'.format(status))

        if status == "downloading":
            match = re.search(r"(\d)+(.(\d)+)*\s(GB|MB|KB)\sof\s(\d)+(.(\d)+)*\s(GB|MB|KB)",
                              download_info.text)
            self.UTILS.test.test(match is not None, "Verify the the text is of the type: 'X' MB of 'Y' MB")
        else:
            self.UTILS.test.test(status in download_info.text.lower(), "Verify the the status is: {}".format(status))

    def tap_on_open_option(self):
        open_btn = self.UTILS.element.getElement(DOM.DownloadManager.download_file_option_open, "Open option button")
        open_btn.tap()

    def get_aside_element(self, data_url):
        elem = (DOM.DownloadManager.download_element_aside[0],
                DOM.DownloadManager.download_element_aside[1].format(data_url))
        return self.UTILS.element.getElement(elem, "Download entry aside button")

    def tap_on_aside_element(self, data_url):
        self.get_aside_element(data_url).tap()

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

        self._tap_on_confirm_button(yes=True, msg="Confirm button")

        # TODO: When bug 1061096 fixed, put the following code at the end of clean_downloads_list, so
        # that it also checks for the message when the download list was already empty
        # Verify no downloads are present
        no_downloads = self.UTILS.element.getElement(
            DOM.DownloadManager.download_empty_list_content, "Getting empty list content")
        self.UTILS.test.test(no_downloads.text == _(
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
        return self.get_download_status(data_url) == "downloading"

    def open_download(self, data_url):
        download_entry = self.get_download_entry(data_url)
        self.UTILS.element.simulateClick(download_entry)

    def open_download_delete_file(self):
        """
        Deletes the file when it was unable to open it
        """
        self._unable_open_option()
        self._tap_on_confirm_button(yes=True, msg="Delete button")
        self._tap_on_confirm_button(yes=True, msg="Confirm Delete button")

    def open_download_keep_file(self):
        """
        Keeps the file when it was unable to open it
        """
        self._unable_open_option()
        self._tap_on_confirm_button(yes=False, msg="Keep file button")

    def stop_download(self, data_url, confirm):
        """
        This method taps on "X" button in order to stop a download in progress
        If @confirm is set to True, it confirms the order. Otherwise, it taps
        in "No" and the download keeps running
        """

        self.tap_on_aside_element(data_url)

        if confirm:
            self._tap_on_confirm_button(yes=True, msg="Confirm button")
            # Verify that the status is stopped
            self.verify_download_status(data_url, "stopped")
            self.verify_download_graphical_status(data_url, "stopped")
        else:
            self._tap_on_confirm_button(yes=False, msg="Cancel button")
            self.verify_download_status(data_url, "downloading")
            self.verify_download_graphical_status(data_url, "downloading")

    def restart_download(self, data_url, confirm, previous_state="stopped"):
        """
        This method taps on the "refresh" button in order to restart a download
        which was either stopped or failed.
        If @confirm is set to True, it confirms the order. Otherwise, it taps
        in "No" and the download remains as it was before
        """
        self.tap_on_aside_element(data_url)

        self._tap_on_confirm_button(yes=confirm, msg="Confirm button" if confirm else "Cancel button")
        self.verify_download_status(data_url, "downloading" if confirm else previous_state)
        self.verify_download_graphical_status(data_url, "downloading" if confirm else previous_state)
