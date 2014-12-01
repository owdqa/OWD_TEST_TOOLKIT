#-*- coding: utf-8 -*-
import time
from gaiatest import GaiaTestCase
from marionette import By
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.utils.html5player import HTML5Player


class test_main(GaiaTestCase):

    test_msg = "Welcome to the September Checkpoint. See this: https://www.youtube.com/watch?v=jAHlQ77lm10"
    video_container_locator = (By.CSS_SELECTOR, 'div[style^="background-image"]')
    video_element_locator = (By.TAG_NAME, 'video')

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)
        self.browser = Browser(self)

        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.target_mms_number = self.UTILS.general.get_os_variable("TARGET_MMS_NUM")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.data_layer.connect_to_cell_data()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Load files into the device.
        #
        self.UTILS.general.addFileToDevice('./tests/_resources/300x300.png', destination='DCIM/100MZLLA')

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create a new SMS
        #
        self.messages.startNewSMS()

        #
        # Insert the phone number in the To field
        #
        self.messages.addNumbersInToField([self.phone_number])

        #
        # Create MMS.
        #
        self.messages.enterSMSMsg(self.test_msg)

        self.messages.createMMSImage()
        self.gallery.clickThumbMMS(0)

        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()

        self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msg, timeout=120)
        self.UTILS.statusbar.click_on_notification_detail(self.test_msg, DOM.Messages.frame_locator)

        text = self.UTILS.element.getElement(DOM.Messages.last_message_mms_text, "Message text").text
        last_msg = self.messages.lastMessageInThisThread()
        self.UTILS.element.scroll_into_view(last_msg)
        self.UTILS.test.TEST(text == self.test_msg, u"[{}] received. Expected [{}]".format(text, self.test_msg), True)

        url = self.marionette.find_element("css selector", "a[data-url*=youtube]", id=last_msg.id)
        url.tap()

        #
        # Tap the video container
        #
        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)
        self.browser.switch_to_content()
        self.wait_for_element_present(*self.video_container_locator, timeout=30)
        self.marionette.find_element(*self.video_container_locator).tap()

        #
        # Wait HTML5 player appear
        #
        self.wait_for_element_present(*self.video_element_locator, timeout=30)
        video = self.marionette.find_element(*self.video_element_locator)

        #
        # Check that video is playing
        #
        time.sleep(5)
        player = HTML5Player(self.marionette, video)
        player.wait_for_video_loaded()
        self.assertTrue(player.is_video_playing())
