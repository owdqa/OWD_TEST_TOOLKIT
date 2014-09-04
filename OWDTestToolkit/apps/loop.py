import time
from OWDTestToolkit import DOM
from marionette import Actions


class Loop(object):

    """Object representing the Loop application.
    """

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS
        self.actions = Actions(self.marionette)

    def launch(self):
        """
        Launch the app.
        """
        self.app = self.apps.launch("Firefox Hello")
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay,
                                              self.__class__.__name__ + " app - loading overlay")
        return self.app

    def dummy(self):
        self.marionette.execute_script(""" console.log(arguments[0]); """, script_args=["Hello"])

    def wizard_or_login(self, ffox_login=None):
        # try:
        self.parent.wait_for_element_displayed(*DOM.Loop.wizard)
        self.skip_wizard(ffox_login)
        # except:
            # try:
            # self.parent.wait_for_element_displayed(*DOM.Loop.wizard_login)
                # TODO: maybe I need to do something more here, once I'm logged, but I dont think so
                # if ffox_login is not None:
                #     self.firefox_login() if ffox_login else self.phone_login()
            # except:
                # self.UTILS.test.TEST(False, "Something is not right when starting Loop", stop_on_error=True)

    def get_wizard_steps(self):
        return len(self.marionette.find_elements(*DOM.Loop.wizard_slideshow_step))

    def skip_wizard(self, ffox_login=None):
        wizard_steps = self.get_wizard_steps()

        current_frame = self.apps.displayed_app.frame
        x_start = current_frame.size['width']
        x_end = x_start // 3
        y_start = current_frame.size['height'] // 2

        for i in range(wizard_steps):
            self.actions.flick(
                current_frame, x_start, y_start, x_end, y_start, duration=500).perform()
            time.sleep(1)

        self.marionette.switch_to_frame(self.apps.displayed_app.frame_id)
        self.parent.wait_for_element_displayed(DOM.Loop.wizard_login[0], DOM.Loop.wizard_login[1], timeout=10)

        if ffox_login is not None:
            self.firefox_login() if ffox_login else self.phone_login()


    def firefox_login(self):
        self.UTILS.reporting.logResult('info', 'Starting ffox login...')

        ffox_btn = self.marionette.find_element(*DOM.Loop.wizard_login_ffox_account)
        #TODOOOOOO: delete this try-except :(
        try:
            self.UTILS.element.simulateClick(ffox_btn)
        except:
            pass

        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult('info', "Screenshot of Loop", screenshot)

        self.marionette.switch_to_frame()
        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult('info', "Screenshot of top_frame", screenshot)

    def phone_login(self):
        self.UTILS.reporting.logResult('info', 'Starting phone login...')