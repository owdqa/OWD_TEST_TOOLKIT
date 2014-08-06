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

    def clickDownloadNotifier(self, title):
        #
        # Click new sms in the home page status bar notificaiton.
        #
        self.UTILS.reporting.logResult("info", "Clicking statusbar notification of new Download from {}...".\
                                       format(title))

        #
        # Switch to the 'home' frame to click the notifier.
        #
        self.marionette.switch_to_frame()
        self.UTILS.statusbar.displayStatusBar()

        #
        # Create the strings to wait for.
        #
        x = (DOM.DownloadManager.statusbar_new_notif[0], DOM.DownloadManager.statusbar_new_notif[1].format(title))

        x = self.UTILS.element.getElement(x, "Statusbar notification for " + title, True, 20, True)
        x.tap()

    def restartDownloadsList(self):

        time.sleep(3)
        x = self.marionette.find_elements(*DOM.DownloadManager.download_list_elems)
        self.UTILS.reporting.debug("*** Download list: {}   Length: {}".format(x, len(x)))

        if not x or len(x) == 0:
            self.UTILS.reporting.logResult("info", "Downloads list is empty, it's not necessary delete any file")
        else:
            self.UTILS.reporting.logResult("info", "Downloads list is not empty, it's necessary delete some files")
            self.deleteAllDownloads()

    def deleteAllDownloads(self):

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

    def deleteDownloadByPosition(self, position):
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

    def deleteDownload(self, filename):
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
        # and wait for a confirmation popup.... like in stopDownload and restartDownload

        #
        # Wait for download to be deleted
        #
        self.UTILS.element.waitForNotElements(elem, "Download item from downloads list")

    def downloadFile(self, filename):
        #
        # Start the file download
        #
        self.UTILS.element.waitForElements(('css selector', 'a[href="%s"] ' % filename), "The file " + filename + " is present")

        link = self.UTILS.element.getElement(('css selector', 'a[href="%s"] ' % filename),
                                 "getting the file [%s] to download" % filename,
                                 True, 120)
        
        self.actions = Actions(self.marionette)
        self.actions.long_press(link, 2).perform()
        time.sleep(1)

        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)

        confirm_save = ('xpath', '//section[@data-type="action"]//button[@id="undefined"]')
        confirm_button = self.UTILS.element.getElement(confirm_save, "Confirmation message")
        confirm_button.tap()
    #     try:
    #         self.parent.wait_for_element_displayed(*confirm_save)
    #         confirm_button = self.marionette.find_element(*confirm_save)
    #         confirm_button.tap()
    #     except:
    #         self.UTILS.test.TEST(False, "Something went wrong getting the confirmation button", True)

    def openDownload(self, file):

        elem = (DOM.DownloadManager.download_element[0],
                DOM.DownloadManager.download_element[1] % file)

        x = self.UTILS.element.getElement(elem, "Getting desired download")
        x.tap()

    def restartDownloadByPosition(self, position, confirm):

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

    def restartDownload(self, download_id, confirm):

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

    def stopDownloadByPosition(self, position, confirm):
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


    def stopDownload(self, download_id, confirm):

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


    def waitForDownloadNotifier(self, title, detail, p_timeout=40):
        #
        # Get the element of the new SMS from the status bar notification.
        # returns a boolean (True if found)
        #
        self.UTILS.reporting.logResult("info",
            "Waiting for statusbar notification of download of title [" + title
            + "] and detail [" + detail + "]")

        #
        # Create the strings to wait for.
        #
        x = (DOM.DownloadManager.statusbar_new_notif[0],
            DOM.DownloadManager.statusbar_new_notif[1] % title)

        y = (DOM.DownloadManager.statusbar_new_notif[0],
            DOM.DownloadManager.statusbar_new_notif[1] % detail)

        #
        # Wait for the notification to be present for this event
        # in the popup messages (this way we make sure it's coming from our number,
        # as opposed to just containing our number in the notification).
        #
        time.sleep(5)
        isTitleOK = self.UTILS.statusbar.waitForStatusBarNew(x, p_displayed=False, p_timeOut=p_timeout)
        isDetailOK = self.UTILS.statusbar.waitForStatusBarNew(y, p_displayed=False, p_timeOut=p_timeout)

        return isTitleOK and isDetailOK


    def waitForNewDownloadPopUp(self, file):
        #
        # Waits for a new SMS popup notification which
        # is from this 'p_num' number.
        #
        myIframe = self.UTILS.ifreame.currentIframe()

        self.marionette.switch_to_frame()
        x = (DOM.DownloadManager.new_download_popup_detail[0], DOM.DownloadManager.new_download_popup_detail[1] % file)
        self.UTILS.element.waitForElements(x,
									"Popup message saying we have a new download of " + file,
									True,
									30)

        self.UTILS.iframe.switchToFrame("src", myIframe)
