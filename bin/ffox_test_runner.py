from marionette.runtests import startTestRunner
from marionette import HTMLReportingTestRunnerMixin
from marionette import BaseMarionetteTestRunner
from gaiatest.runtests import GaiaTestRunner
from gaiatest.runtests import GaiaTextTestRunner
from marionette.runner import BaseMarionetteOptions
from gaiatest import GaiaTestCase, GaiaTestRunnerMixin
import sys
from gaiatest.version import __version__


class OWDMarionetteTestRunner(BaseMarionetteTestRunner):

    def run_test(self, filepath, expected, oop):
        idx = filepath.rindex('test_')
        # + 5: to skip the "test_" part
        # - 3: to remove the .py extension
        test_num = filepath[idx + 5:-3]
        self.logger.info("Test num: {}".format(test_num))
        self.testvars['TEST_NUM'] = test_num
        self.testvars['DET_FILE'] = test_num + "_detail"
        self.testvars['SUM_FILE'] = test_num + "_summary"
        super(OWDMarionetteTestRunner, self).run_test(filepath, expected, oop)


class OWDTestRunner(OWDMarionetteTestRunner, GaiaTestRunnerMixin, HTMLReportingTestRunnerMixin):

    textrunnerclass = GaiaTextTestRunner

    def __init__(self, **kwargs):
        BaseMarionetteTestRunner.__init__(self, **kwargs)
        GaiaTestRunnerMixin.__init__(self, **kwargs)
        HTMLReportingTestRunnerMixin.__init__(self, name='gaiatest-v2.0', version=__version__, **kwargs)
        self.test_handlers = [GaiaTestCase]


# runner_class=MarionetteTestRunner, parser_class=BaseMarionetteOptions
def ffox_test_runner(args):
    parser = BaseMarionetteOptions(usage='%prog [options] test_file_or_dir <test_file_or_dir> ...')
    options, tests = parser.parse_args(args)
    print "Options: {}".format(options)
    print "Tests: {}".format(tests)
    parser.verify_usage(options, tests)

    print "Version: {}".format(__version__)
    runner = startTestRunner(OWDTestRunner, options, tests)
    if runner.failed > 0:
        sys.exit(10)

if __name__ == "__main__":
    ffox_test_runner(sys.argv[1:])
