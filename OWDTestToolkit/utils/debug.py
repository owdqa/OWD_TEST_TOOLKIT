import traceback
from inspect import stack
import os
import base64


class debug(object):

    def __init__(self, parent):
        self.parent = parent
        self.errNum = parent.errNum
        self.testNum = parent.testNum
        self.marionette = parent.marionette

    def getStackTrace(self):
        #
        # Adds the stack trace to the test report (called automatically if UTILS.test() fails).
        #

        _logstr = "STACK TRACE (code path to this point):"
        _stack = traceback.extract_stack()
        _counter = 0

        for i in _stack:
            if ("OWDTestToolkit" in i[0] or "/test_" in i[0]) and \
                "quit_test.py" not in i[0] and i[2] != stack()[0][3] and \
                i[2] != "test":
                    _counter = _counter + 1
                    _logstr = _logstr + "|{}. {}: <i>{}</i>".\
                              format(_counter, ("<b>" + os.path.basename(i[0]) + "</b>({})".format(i[1])).ljust(40),
                                     i[3])

        self.parent.reporting.logResult("debug", _logstr)

    def savePageHTML(self, p_outfile):
        #
        # Save the HTML of the current page to the specified file.
        #
        f = open(p_outfile, 'w')
        f.write(self.marionette.page_source.encode('ascii', 'ignore'))

    def screenShot(self, p_fileSuffix):
        #
        # Take a screenshot.
        #
        outFile = self.parent.general.get_os_variable('RESULT_DIR') + "/" + p_fileSuffix + ".png"

        try:
            screenshot = self.marionette.screenshot()
            with open(outFile, 'w') as f:
                f.write(base64.decodestring(screenshot))
            return outFile
        except:
            return "(Unable to capture screenshot: possible Marionette issue.)"

    def screenShotOnErr(self):
        #
        # Take a screenshot on error (increments the file number).
        #

        #
        # Build the error filename.
        #
        self.errNum = self.errNum + 1
        fnam = self.testNum + "_" + str(self.errNum)

        #
        # Record the screenshot.
        #
        screenDump = self.screenShot(fnam)

        #
        # Dump the current page's html source too.
        #
        htmlDump = self.parent.general.get_os_variable('RESULT_DIR') + "/" + fnam + ".html"

        try:
            self.savePageHTML(htmlDump)
        except:
            htmlDump = "(Unable to dump html for this page: possible Marionette issue.)"

        return (htmlDump, screenDump)
