from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def addSubject(self, p_string):

        #
        # Press options button
        #
        self.UTILS.logResult("info", "Cliking on messages options button")
        x = self.UTILS.getElement(DOM.Messages.messages_options_btn, "Messages option button is displayed")
        x.tap()

        #
        # Press add subject button
        #
        self.UTILS.logResult("info", "Cliking on add subject button")
        x = self.UTILS.getElement(DOM.Messages.addsubject_btn_msg_opt, "add subject option button is displayed")
        x.tap()


        self.UTILS.typeThis(DOM.Messages.target_subject,
	                                "Target Subject  field",
	                                p_string,
	                                p_no_keyboard=True,
	                                p_validate=False,
	                                p_clear=False,
	                                p_enter=False)