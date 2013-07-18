from OWDTestToolkit.global_imports import *

import  addNumbersInToField                 ,\
        checkAirplaneModeWarning           ,\
        checkIsInToField                   ,\
        checkNumberIsInToField             ,\
        checkThreadHeader                  ,\
        clickSMSNotifier                   ,\
        closeThread                        ,\
        countMessagesInThisThread          ,\
        createAndSendSMS                   ,\
        deleteAllThreads                   ,\
        deleteMessagesInThisThread         ,\
        deleteSelectedMessages             ,\
        deleteSelectedThreads              ,\
        deleteThreads                      ,\
        editAndSelectMessages              ,\
        editAndSelectThreads               ,\
        enterSMSMsg                        ,\
        lastMessageInThisThread            ,\
        openThread                         ,\
        readLastSMSInThread                ,\
        readNewSMS                         ,\
        removeContactFromToField           ,\
        selectAddContactButton             ,\
        sendSMS                            ,\
        startNewSMS                        ,\
        getThreadText                      ,\
        threadCarrier                      ,\
        threadEditModeOFF                  ,\
        threadEditModeON                   ,\
        threadType                         ,\
        threadExists                       ,\
        timeOfLastMessageInThread          ,\
        timeOfThread                       ,\
        header_sendMessage                 ,\
        header_addToContact                ,\
        header_call                        ,\
        header_createContact               ,\
        waitForReceivedMsgInThisThread     ,\
        waitForNewSMSPopup_by_msg          ,\
        waitForNewSMSPopup_by_number       ,\
        waitForSMSNotifier                 

class Messages (
            addNumbersInToField.main,
            checkAirplaneModeWarning.main,
            checkIsInToField.main,
            checkNumberIsInToField.main,
            checkThreadHeader.main,
            clickSMSNotifier.main,
            closeThread.main,
            countMessagesInThisThread.main,
            createAndSendSMS.main,
            deleteAllThreads.main,
            deleteMessagesInThisThread.main,
            deleteSelectedMessages.main,
            deleteSelectedThreads.main,
            deleteThreads.main,
            editAndSelectMessages.main,
            editAndSelectThreads.main,
            enterSMSMsg.main,
            lastMessageInThisThread.main,
            openThread.main,
            readLastSMSInThread.main,
            readNewSMS.main,
            removeContactFromToField.main,
            selectAddContactButton.main,
            sendSMS.main,
            startNewSMS.main,
            getThreadText.main,
            threadCarrier.main,
            threadEditModeOFF.main,
            threadEditModeON.main,
            threadType.main,
            threadExists.main,
            header_sendMessage.main,
            header_addToContact.main,
            header_call.main,
            header_createContact.main,
            timeOfLastMessageInThread.main,
            timeOfThread.main,
            waitForReceivedMsgInThisThread.main,
            waitForNewSMSPopup_by_msg.main,
            waitForNewSMSPopup_by_number.main,
            waitForSMSNotifier.main):
    
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.parent     = p_parent
        self.marionette = p_parent.marionette
        self.UTILS      = p_parent.UTILS

    def launch(self):
        #
        # Launch the app.
        #
        self.apps.kill_all()
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")

