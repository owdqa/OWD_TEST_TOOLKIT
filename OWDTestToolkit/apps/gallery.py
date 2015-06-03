from OWDTestToolkit import DOM
import time
import datetime
from marionette_driver.marionette import Actions


class Gallery(object):

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS
        self.actions = Actions(self.marionette)

    def launch(self):
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(
            DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        self.UTILS.element.waitForNotElements(DOM.Gallery.loading_bar, "Loading bar", True, 10)
        return self.app

    def convert_str_to_seconds(self, the_string):
        """
        Converts a str of the form "aa:bb" into seconds
        """
        processed = time.strptime(the_string, '%M:%S')
        return (int(datetime.timedelta(minutes=processed.tm_min, seconds=processed.tm_sec).total_seconds()))

    def check_video_length(self, expected_duration, margin=2):
        """
        This method asserts that the video has the desired duration
        @param  int expected_duration   specifies the video duration in seconds
        """

        # Play the video and get total duration
        self.play_current_video()
        video_length = self.UTILS.element.getElement(DOM.Gallery.preview_current_video_duration, "Video length")
        real_duration = self.convert_str_to_seconds(video_length.text)

        # Note: we give 1 second margin in case the things went a little bit slower when recording the video
        interval = range(expected_duration - margin, expected_duration + margin + 1, 1)
        self.UTILS.test.test(real_duration in interval, "Duration matches")

    def click_on_thumbnail_at_position(self, position, preview=True):
        """
        Clicks on a thumbnail at a certain position from the gallery.
        @param  boolean     preview     specifies whether we have to check for the preview screen or not
        """
        self.parent.wait_for_element_displayed(*DOM.Gallery.thumbnail_items)
        thumb_list = self.marionette.find_elements(*DOM.Gallery.thumbnail_items)
        time.sleep(1)
        thumb = thumb_list[position]
        thumb.tap()

        self.UTILS.element.waitForNotElements(DOM.Gallery.thumbnail_items, "Thumbnail list", True, 10)
        if preview:
            self.UTILS.element.waitForElements(DOM.Gallery.preview, "Thumbnail preview", True, 10)

    def _click_on_thumb_external(self, position, frame_to_change):
        """
        Private method which handles image selection and image cropping
        @param  int     position            thumbnail to click
        @param  tuple   frame_to_change     frame to switch once the image has been cropped
        """
        time.sleep(1)
        self.click_on_thumbnail_at_position(position, preview=False)

        time.sleep(2)

        crop = self.UTILS.element.getElement(DOM.Gallery.crop_done, "Crop Done")
        crop.tap()

        self.UTILS.iframe.switchToFrame(*frame_to_change)

    def click_on_thumbnail_at_position_mms(self, position):
        """
        Clicks a thumbnail from the gallery in order to attach it to a MMS
        """
        self._click_on_thumb_external(position, DOM.Messages.frame_locator)

    def click_on_thumbnail_at_position_email(self, position):
        """
        Clicks a thumbnail from the gallery in order to attach it to an email
        """
        self._click_on_thumb_external(position, DOM.Email.frame_locator)

    def delete_thumbnails(self, num_array):
        """
        Deletes the thumbnails listed in num_array
        (following an index starting at number 0)
        The list must be numeric, i.e "delete_thumbnails([0,1,2])".
        """

        # Get the amount of thumbnails we currently have.
        before_thumbcount = self.get_number_of_thumbnails()
        delete_thumbcount = len(num_array)
        target_thumbcount = before_thumbcount - delete_thumbcount

        select_mode_btn = self.UTILS.element.getElement(DOM.Gallery.thumbnail_select_mode, "Select button")
        select_mode_btn.tap()

        # Select the target ones
        thumbs = self.UTILS.element.getElements(DOM.Gallery.thumbnail_items, "Thumbnails")
        for position in num_array:
            thumbs[position].tap()

        selected = self.UTILS.element.getElement(DOM.Gallery.thumbnail_number_selected, "Number selected header")
        self.UTILS.test.test(str(delete_thumbcount) in selected.text, "Right number of thumbs selected")

        trash_btn = self.UTILS.element.getElement(DOM.Gallery.thumbnail_trash_icon, "Trash icon")
        trash_btn.tap()

        confirm = self.UTILS.element.getElement(DOM.GLOBAL.modal_confirm_ok, "Delete")
        confirm.tap()

        if target_thumbcount < 1:
            self.UTILS.element.waitForElements(DOM.Gallery.no_thumbnails_message,
                                       "Message saying there are no thumbnails", False, 5)
        else:
            # Come out of 'select' mode.
            exit_select_mode_header = self.UTILS.element.getElement(
                DOM.Gallery.exit_select_mode_header, "Exit select mode button")
            exit_select_mode_header.tap(25, 25)

            current_thumbs = self.get_number_of_thumbnails()
            self.UTILS.test.test(current_thumbs == target_thumbcount,
                                 "After deleting [{}] pics, we have the expected number: {}".\
                                 format(delete_thumbcount, target_thumbcount))

    def get_gallery_items(self):
        """
        Returns a list of gallery item objects, with RAW info (date, metadata, size...)
        """
        self.UTILS.element.waitForElements(DOM.Gallery.thumbnail_items, "Thumbnails", True, 20, False)
        return self.marionette.execute_script("return window.wrappedJSObject.files;")

    def play_current_video(self):
        """
        Plays the video that has previously been loaded (by pressing its thumbnail first), then press a play button.
        """
        play_btn = self.UTILS.element.getElement(DOM.Gallery.preview_current_video_play, "Video play button")
        time.sleep(1)
        play_btn.tap()

        self.UTILS.element.waitForElements(DOM.Gallery.preview_current_video_pause, "Pause button", True, 20, False)

    def get_number_of_thumbnails(self):
        """
        Returns the number of thumbnails.
        """
        try:
            self.parent.wait_for_element_displayed(*DOM.Gallery.thumbnail_items)
            return len(self.marionette.find_elements(*DOM.Gallery.thumbnail_items))
        except:
            return 0

    def wait_for_thumbnails_number(self, number, timeout=10):
        """
        Waits untils @number thumbnails are present in the thumbnails screen
        """
        msg = "Waiting until we have the expected number of thumbnails"
        self.parent.wait_for_condition(
            lambda m: len(m.find_elements(*DOM.Gallery.thumbnail_items)) == number, timeout=timeout, message=msg)

    def swipe_between_gallery_items(self, steps):
        """
        Swipes over the gallery items (the preview screen must be displayed) a certain number of steps
        Important: there is no way of checking that the image is being shown each time we swipe,
        """
        current_frame = self.apps.displayed_app.frame
        x_start = current_frame.size['width']
        x_end = x_start // 4
        y_start = current_frame.size['height'] // 2

        for i in range(steps):
            self.actions.flick(
                current_frame, x_start, y_start, x_end, y_start, duration=600).perform()
            time.sleep(1)
