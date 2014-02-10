from OWDTestToolkit.global_imports import *
from OWDTestToolkit.apps.Video import *
from OWDTestToolkit.apps.Gallery import *
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
        elif attached_type=="video":
            #
            # Load an video file into the device.
            #
            self.UTILS.addFileToDevice('./tests/_resources/mpeg4.mp4', destination='/SD/mus')

            self.createMMSVideo()
            self.video.clickOnVideoMMS(0)

        elif attached_type=="audio":
            #
            # Load an video file into the device.
            #
            self.UTILS.addFileToDevice('./tests/_resources/AMR.amr', destination='/SD/mus')

            self.createMMSMusic()
            self.music.clickOnSongMMS()

        else:
            #self.UTILS.logResult("info", "incorrect value received")
            self.UTILS.quitTest("FAILED: Incorrect parameter received in createAndSendMMS() . attached_type must being image, video or audio.")



        #
        # Click send and wait for the message to be received
        #
        self.sendSMS()


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
