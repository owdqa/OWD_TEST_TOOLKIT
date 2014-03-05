from OWDTestToolkit.global_imports import *
from OWDTestToolkit.apps.Video import *
from OWDTestToolkit.apps.Music import *


class main(GaiaTestCase):
    #
    # attached_type must being image, video or audio.
    #

    #
    #audio and video have the same code, but are separated in thinking if future changes
    #

    def verifyMMSReceived(self, attached_type):


        if attached_type=="image":
            #
            # This step is necessary because our sim cards receive mms with +XXX
            #
            x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
            x.tap()

            self.openThread("+" + self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM"))

            #
            # Wait for the last message in this thread to be a 'recieved' one.
            #
            returnedSMS = self.waitForReceivedMsgInThisThread()
            self.UTILS.TEST(returnedSMS, "A receieved message appeared in the thread.", True)


            #
            # Obtaining file attached type
            #
            x = self.UTILS.getElement(DOM.Messages.attach_preview_img_type, "preview type")
            type=x.get_attribute("data-attachment-type")

            if type != "img":
                self.UTILS.quitTest("Incorrect file type. The file must be img ")

        elif attached_type=="video":
            #
            # This step is necessary because our sim cards receive mms with +XXX
            #
            x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
            x.tap()

            self.openThread("+" + self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM"))

            #
            # Wait for the last message in this thread to be a 'recieved' one.
            #
            returnedSMS = self.waitForReceivedMsgInThisThread()
            self.UTILS.TEST(returnedSMS, "A receieved message appeared in the thread.", True)


            #
            # Obtaining file attached type
            #
            x = self.UTILS.getElement(DOM.Messages.attach_preview_video_audio_type, "preview type")
            type=x.get_attribute("data-attachment-type")

            if type != "video":
                self.UTILS.quitTest("Incorrect file type. The file must be video")




        elif attached_type=="audio":
           #
            # This step is necessary because our sim cards receive mms with +XXX
            #
            x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
            x.tap()

            self.openThread("+" + self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM"))

            #
            # Wait for the last message in this thread to be a 'recieved' one.
            #
            returnedSMS = self.waitForReceivedMsgInThisThread()
            self.UTILS.TEST(returnedSMS, "A receieved message appeared in the thread.", True)


            #
            # Obtaining file attached type
            #
            x = self.UTILS.getElement(DOM.Messages.attach_preview_video_audio_type, "preview type")
            type=x.get_attribute("data-attachment-type")

            if type != "audio":
                self.UTILS.quitTest("Incorrect file type. The file must be audio ")

        else:
            #self.UTILS.logResult("info", "incorrect value received")
            self.UTILS.quitTest("FAILED: Incorrect parameter received in verifyMMSReceived() . attached_type must being image, video or audio.")






