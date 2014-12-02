from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.downloadmanager import DownloadManager
from OWDTestToolkit import DOM


class test_main(GaiaTestCase):

    def setUp(self):

        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)

        self.settings = Settings(self)
        self.download_manager = DownloadManager(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        self.settings.launch()
        self.settings.downloads()

        edit_mode = self.UTILS.element.getElement(DOM.DownloadManager.download_edit_button,
                                                  "Download edit button", True, 10)
        self.UTILS.test.TEST(edit_mode.get_attribute("class") == "disabled", "Edit mode button is disabled")

        edit_mode.tap()
        self.UTILS.element.waitForNotElements(DOM.DownloadManager.downloads_edit_header_title,
                                           "Edit downloads header")
