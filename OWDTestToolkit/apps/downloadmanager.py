import re
import time
from OWDTestToolkit import DOM
from marionette import Actions

class DownloadManager(object):

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS

    def clean_downloads_list(self):

        time.sleep(3)
        x = self.marionette.find_elements(*DOM.DownloadManager.download_list_elems)
        self.UTILS.reporting.debug("*** Download list: {}   Length: {}".format(x, len(x)))

        if not x or len(x) == 0:
            self.UTILS.reporting.logResult("info", "Downloads list is empty, it's not necessary delete any file")
        else:
            self.UTILS.reporting.logResult("info", "Downloads list is not empty, it's necessary delete some files")
            self.delete_all_downloads()

    def delete_all_downloads(self):

        #
        # Enter into Edit Mode
        #

        self.UTILS.element.waitForElements(DOM.DownloadManager.download_edit_button,
                                     "Getting download edit button")

        x = self.UTILS.element.getElement(DOM.DownloadManager.download_edit_button,
                                     "Getting download edit button")
        x.tap()

        #
        # Making sure we are in Edit Downloads Mode
        #
        x = self.UTILS.element.getElement(DOM.DownloadManager.downloads_edit_header_title,
                                    "Getting edit downloads header")

        self.UTILS.test.TEST(x.text == "Edit downloads", "Verifying we are in Edit Mode")

        #
        # Verify "Select All button" is enabled and "Deselect All" is disabled
        #

        #
        # Get "Select All" button
        #
        select = self.UTILS.element.getElement(DOM.DownloadManager.download_select_all,
                                "Getting 'Select All' button")

        result = select.get_attribute("disabled")
        self.UTILS.test.TEST(result == "false", 'Checking "Select All" button is enabled')

        #
        # Get "Deselect All" button
        #

        deselect = self.UTILS.element.getElement(DOM.DownloadManager.download_deselect_all,
                                "Getting 'Deselect All' button")

        result = deselect.get_attribute("disabled")

        self.UTILS.test.TEST(result == "true", 'Checking "Deselect All" button is disabled')

        #
        # Selecting all downloads
        #
        select.tap()

        time.sleep(2)

        #
        # Verify that now "Deselect All" button is enabled and "Select All"
        # button is disabled
        #
        select = self.UTILS.element.getElement(DOM.DownloadManager.download_select_all,
                                "Getting 'Select All' button")

        deselect = self.UTILS.element.getElement(DOM.DownloadManager.download_deselect_all,
                                "Getting 'Deselect All' button")

        result = deselect.get_attribute("disabled")
        self.UTILS.test.TEST(result == "false", 'Checking "Deselect All" button is enabled')

        result = select.get_attribute("disabled")
        self.UTILS.test.TEST(result == "true", 'Checking "Select All" button is disabled')

        #
        # Delete all the downloads
        #
        x = self.UTILS.element.getElement(DOM.DownloadManager.download_delete_button,
                        "Getting Delete button")
        x.tap()

        self.UTILS.element.waitForElements(DOM.DownloadManager.download_confirm_yes,
                        "Getting Delete button")
        x = self.UTILS.element.getElement(DOM.DownloadManager.download_confirm_yes,
                        "Getting Delete button")
        x.tap()

        # self.UTILS.element.simulateClick(x)

        #
        # Verify no downloads are present
        #

        x = self.UTILS.element.getElement(DOM.DownloadManager.download_empty_list_content,
                                "Getting empty list content")
        self.UTILS.test.TEST(x.text == "No downloads",
            "Verifying 'No downloads' message is displayed")

    def delete_download_by_position(self, position):
        #
        # Deletes a single download from the downloads list by position
        #

        #
        # Enter into Edit Mode
        #
        x = self.UTILS.element.getElement(DOM.DownloadManager.download_edit_button,
                                     "Getting download edit button")
        x.tap()
        time.sleep(2)

        self.UTILS.element.waitForElements(DOM.DownloadManager.downloads_edit_header_title,
                                    "Getting edit downloads header")
        #
        # Getting the element's checkbox
        #
        elem = (DOM.DownloadManager.download_element_checkbox_position[0],
                 DOM.DownloadManager.download_element_checkbox_position[1].format(position))

        self.UTILS.element.waitForElements(elem, "Getting the checkbox of the file to delete")

        x = self.UTILS.element.getElement(elem, "Getting the checkbox of the file to delete")
        x.tap()

        #
        # Get Delete button
        #
        x = self.UTILS.element.getElement(DOM.DownloadManager.download_delete_button, "Getting Delete button")
        x.tap()

        #
        # Confirmation
        #
        self.UTILS.element.waitForElements(DOM.DownloadManager.download_confirm_yes,
                        "Getting Delete button")
        x = self.UTILS.element.getElement(DOM.DownloadManager.download_confirm_yes,
                        "Getting Delete button")
        x.tap()

    def delete_download(self, filename):
        #
        # Deletes a single download from the downloads list
        #

        #
        # Enter into Edit Mode
        #
        x = self.UTILS.element.getElement(DOM.DownloadManager.download_edit_button,
                                     "Getting download edit button")
        x.tap()

        time.sleep(10)

        #
        # Making sure we are in Edit Downloads Mode
        #
        x = self.UTILS.element.getElement(DOM.DownloadManager.downloads_edit_header_title,
                                    "Getting edit downloads header")

        self.UTILS.test.TEST(x.text == "Edit downloads", "Verifying we are in Edit Mode")
        #
        # Getting the element's checkbox
        #
        elem = (DOM.DownloadManager.download_element_checkbox[0],
                 DOM.DownloadManager.download_element_checkbox[1] % filename)

        x = self.UTILS.element.getElement(elem, "Getting the checkbox of the file to delete")
        x.tap()

        #
        # Get Delete button
        #
        x = self.UTILS.element.getElement(DOM.DownloadManager.download_delete_button, "Getting Delete button")
        x.tap()

        #
        # TODO - CONFIRMATION!!!! - We will add a new parameter, called 'confirm'
        # and wait for a confirmation popup.... like in stop_download and restart_download

        #
        # Wait for download to be deleted
        #
        self.UTILS.element.waitForNotElements(elem, "Download item from downloads list")

    def download_file(self, filename):
        #
        # Start the file download
        # TODO - This works for our test page. Try to generalize a lil' bit
        #

        link = self.UTILS.element.getElement(('css selector', 'a[href="{}"]'.format(filename)), 'The file [{}] to download'.format(filename), 
                                 True, 10)
        link.tap()
    
    def is_file_downloading(self, file_name):
        #
        # Checks whether the file is downloading in the downloads list
        #
        
        #
        # Sometimes it takes too long to load the list
        #
        self.parent.wait_for_element_displayed(DOM.DownloadManager.download_list[0],
            DOM.DownloadManager.download_list[1], 60)

        #
        # Gets the desired file in the list
        #
        elem = (DOM.DownloadManager.download_element[0],
                DOM.DownloadManager.download_element[1].format(file_name))
        # self.parent.wait_for_element_displayed(*elem)
        # file = self.marionette.find_element(*elem)

        file = self.UTILS.element.getElement(elem, "A file")
        return file.get_attribute("data-state") == "downloading"
        
    def open_download(self, file):

        elem = (DOM.DownloadManager.download_element[0],
                DOM.DownloadManager.download_element[1].format(file))

        x = self.UTILS.element.getElement(elem, "Getting desired download")
        x.tap()

    def restart_download_by_position(self, position, confirm):

        #
        # Restarts a download that was previously stopped, if <confirm> = True
        #


        #
        # Tap on a stopped Download by download_id
        #
        elem = (DOM.DownloadManager.download_element_button_position[0],
                DOM.DownloadManager.download_element_button_position[1].format(position))
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
            elem = (DOM.DownloadManager.download_status_text_position[0],
                    DOM.DownloadManager.download_status_text_position[1].format(position))
            x = self.UTILS.element.getElement(elem,
                        "Obtain the text displayed to verify the text 'X' MB of 'Y' MB")

            match = re.search(r"(\d)+(.(\d)+)*\s(GB|MB|KB)\sof\s(\d)+(.(\d)+)*\s(GB|MB|KB)",
                             x.text)
            self.UTILS.test.TEST(match is not None, "Verify the the text is: 'X' MB of 'Y' MB")

            #
            # Verify status downloading using data-state="downloading".
            #
            elem = (DOM.DownloadManager.download_status_text_position[0],
                    DOM.DownloadManager.download_status_position[1].format(position))
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
            elem = (DOM.DownloadManager.download_status_text_position[0],
                     DOM.DownloadManager.download_status_text_position[1].format(position))
            x = self.UTILS.element.getElement(elem,
                         "Obtain the text displayed to verify the text stopped")
            self.UTILS.test.TEST("Stopped" in x.text, "Verify the text Stopped")

            #
            # Verify status Stopped using data-state="stopped".
            #
            elem = (DOM.DownloadManager.download_status_text_position[0], DOM.DownloadManager.download_status_position[1].format(position))
            x = self.UTILS.element.getElement(elem, "Obtain the download state")
            self.UTILS.test.TEST("stopped" == x.get_attribute("data-state"),
                            "Verify that the status is stopped")

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
            elem = (DOM.DownloadManager.download_status_position[0], DOM.DownloadManager.download_status_position[1].format(position))
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
            elem = (DOM.DownloadManager.download_status_position[0], DOM.DownloadManager.download_status_position[1].format(position))
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