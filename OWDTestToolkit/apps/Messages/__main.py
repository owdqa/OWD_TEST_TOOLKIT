from OWDTestToolkit.global_imports import *

import  addContactToThisSMS                ,\
        addNumberInToField                 ,\
        checkAirplaneModeWarning           ,\
        checkIsInToField                   ,\
        checkNumberIsInToField             ,\
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
        removeFromToField                  ,\
        selectAddContactButton             ,\
        sendSMS                            ,\
        startNewSMS                        ,\
        threadCarrier                      ,\
        threadEditModeOFF                  ,\
        threadEditModeON                   ,\
        threadType                         ,\
        timeOfLastMessageInThread          ,\
        timeOfThread                       ,\
        waitForReceivedMsgInThisThread     ,\
        waitForSMSNotifier                 

class Messages (
            addContactToThisSMS.main,
            addNumberInToField.main,
            checkAirplaneModeWarning.main,
            checkIsInToField.main,
            checkNumberIsInToField.main,
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
            removeFromToField.main,
            selectAddContactButton.main,
            sendSMS.main,
            startNewSMS.main,
            threadCarrier.main,
            threadEditModeOFF.main,
            threadEditModeON.main,
            threadType.main,
            timeOfLastMessageInThread.main,
            timeOfThread.main,
            waitForReceivedMsgInThisThread.main,
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

