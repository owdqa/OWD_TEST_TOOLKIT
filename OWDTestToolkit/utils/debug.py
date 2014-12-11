import base64


class debug(object):

    def __init__(self, parent):
        self.parent = parent
        self.errNum = parent.errNum
        self.test_num = parent.test_num
        self.marionette = parent.marionette

    def save_page_html(self, p_outfile):
        #
        # Save the HTML of the current page to the specified file.
        #
        f = open(p_outfile, 'w')
        f.write(self.marionette.page_source.encode('ascii', 'ignore'))

    def screenShot(self, p_fileSuffix):
        #
        # Take a screenshot.
        #
        outFile = self.parent.general.get_config_variable('result_dir', 'output') + "/" + p_fileSuffix + ".png"

        try:
            screenshot = self.marionette.screenshot()
            with open(outFile, 'w') as f:
                f.write(base64.decodestring(screenshot))

            # We have to return the relative path, so that the report does not depend on the RESULTS_DIR
            return p_fileSuffix + ".png"
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
        fnam = self.test_num + "_" + str(self.errNum)

        #
        # Record the screenshot.
        #
        screenDump = self.screenShot(fnam)

        #
        # Dump the current page's html source too.
        #
        htmlDump = self.parent.general.get_config_variable('result_dir', 'output') + "/" + fnam + ".html"

        try:
            self.save_page_html(htmlDump)
        except:
            htmlDump = "(Unable to dump html for this page: possible Marionette issue.)"

        result_dir = self.parent.general.get_config_variable('result_dir', 'output')
        return [fnam + ".html", screenDump]
