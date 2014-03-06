from OWDTestToolkit.global_imports import *
from OWDTestToolkit.apps.Video import *
from OWDTestToolkit.apps.gallery import *
from OWDTestToolkit.apps.Music import *


class main(GaiaTestCase):
    #
    # attached_type must being image, video or audio.
    #

    def createAndSendMMS(self, attached_type, m_text):
        self.gallery    = Gallery(self)
        self.video    = Video(self)
        self.music    = Music(self)

        #
        # Launch messages app.
        #
        self.launch()

        #
        # Create a new SMS
        #
        self.startNewSMS()

        #
        # Insert the phone number in the To field
        #
        self.addNumbersInToField([ self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM") ])

        #
        # Create MMS.
        #
        self.enterSMSMsg(m_text)

        if attached_type=="image":
            #
            # Add an image file
            #
            self.UTILS.addFileToDevice('./tests/_resources/80x60.jpg', destination='DCIM/100MZLLA')

            self.createMMSImage()
            self.gallery.clickThumbMMS(0)

            #
            # Click send and wait for the message to be received
            #
            self.sendSMS()
            time.sleep(5)

            #
            # Obtaining file attached type
            #
            x = self.UTILS.getElement(DOM.Messages.attach_preview_img_type, "preview type")
            type=x.get_attribute("data-attachment-type")


            if type != "img":
                self.UTILS.quitTest("Incorrect file type. The file must be img ")



        elif attached_type=="video":
            #
            # Load an video file into the device.
            #
            self.UTILS.addFileToDevice('./tests/_resources/mpeg4.mp4', destination='/SD/mus')

            self.createMMSVideo()
            self.video.clickOnVideoMMS(0)
            self.sendSMS()


            #
            # Obtaining file attached type
            #
            x = self.UTILS.getElement(DOM.Messages.attach_preview_video_audio_type, "preview type")
            type=x.get_attribute("data-attachment-type")

            if type != "video":
                self.UTILS.quitTest("Incorrect file type. The file must be video")




        elif attached_type=="audio":
            #
            # Load an video file into the device.
            #
            self.UTILS.addFileToDevice('./tests/_resources/AMR.amr', destination='/SD/mus')

            self.createMMSMusic()
            self.music.click_on_song_mms()

            #
            # Click send and wait for the message to be received
            #
            self.sendSMS()
            time.sleep(5)


            #
            # Obtaining file attached type
            #
            x = self.UTILS.getElement(DOM.Messages.attach_preview_video_audio_type, "preview type")
            type=x.get_attribute("data-attachment-type")

            if type != "audio":
                self.UTILS.quitTest("Incorrect file type. The file must be audio ")

        else:
            #self.UTILS.logResult("info", "incorrect value received")
            self.UTILS.quitTest("FAILED: Incorrect parameter received in createAndSendMMS() . attached_type must being image, video or audio.")


