from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def send_new_email(self, p_target, p_subject, p_message):
        #
        # Compose and send a new email.
        #
        x = self.UTILS.getElement(DOM.Email.compose_msg_btn, "Compose message button")
        x.tap()

        #
        # Wait for 'compose message' header.
        #
        x = self.UTILS.getElement(('xpath', DOM.GLOBAL.app_head_specific % "Compose message"),
                                  "Compose message header")
        
        #
        # Put items in the corresponsing fields.
        #
#         msg_to      = self.UTILS.getElement(DOM.Email.compose_to, "'To' field")
#         msg_subject = self.UTILS.getElement(DOM.Email.compose_subject, "'Subject' field")
#         msg_msg     = self.UTILS.getElement(DOM.Email.compose_msg, "Message field")
#         msg_to.send_keys(p_target)
#         time.sleep(1)
#         msg_subject.send_keys(p_subject)
#         time.sleep(1)
#         msg_msg.send_keys(p_message)
#         time.sleep(1)
            
        self.UTILS.typeThis(DOM.Email.compose_to     , "'To' field"     , p_target , True, False)
        self.UTILS.typeThis(DOM.Email.compose_subject, "'Subject' field", p_subject, True, False)
        self.UTILS.typeThis(DOM.Email.compose_msg    , "Message field"  , p_message, True, False, False)

        self.sendTheMessage()

