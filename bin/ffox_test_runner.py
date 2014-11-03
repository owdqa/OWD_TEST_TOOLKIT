from marionette import HTMLReportingTestRunnerMixin
from marionette import BaseMarionetteTestRunner
from gaiatest.runtests import GaiaTextTestRunner
from marionette.runner import BaseMarionetteOptions
from gaiatest import GaiaTestCase, GaiaTestRunnerMixin
from datetime import datetime
import sys
import os
from gaiatest.version import __version__
import logging.config

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
        # Establish our own logger
        BaseMarionetteTestRunner.__init__(self, **kwargs)
        config_file = self.testvars['OWD_LOG_CFG']
        logging.config.fileConfig(config_file)
        self.logger = logging.getLogger('OWDTestToolkit')
        
        GaiaTestRunnerMixin.__init__(self, **kwargs)
        self.prepare_results()
        HTMLReportingTestRunnerMixin.__init__(self, name='gaiatest-v2.0', version=__version__, html_output=self.testvars['html_output'], **kwargs)
        self.test_handlers = [GaiaTestCase]
    
    def prepare_results(self):
        """ This methods ensures that the destination results directory is created before launching the 
        test/s execution. It also creates the html results report file.
        """
        if not os.path.exists(self.testvars['RESULT_DIR']): 
            os.makedirs(self.testvars['RESULT_DIR'])
            
        with open(self.testvars['html_output'], 'w') as f:
            f.write('')
            f.close()

class FfoxTestRunner():
    
# runner_class=MarionetteTestRunner, parser_class=BaseMarionetteOptions
    def __init__(self, args):
        self.args = args
        self.runner_class = OWDTestRunner
        self.runner = None
        self.total = 0
        self.skipped = 0
        self.unexpected_passed = 0
        self.passed = 0 
        self.automation_failures = 0 
        self.unexpected_failures = 0
        self.expected_failures = 0
        
    def start_test_runner(self, runner_class, options, tests):
        self.start_time = datetime.utcnow()
        runner = runner_class(**vars(options))
        runner.run_tests(tests)
        self.end_time = datetime.utcnow() 
        return runner
    
    def update_attr(self, attr_name, attr_value):
        setattr(self, attr_name, getattr(self, attr_name) + attr_value)
        
    def process_runner_results(self):
        # NOTE: since self.test_handlers is GaiaTestCase, the results will be instances of GaiaTestResult which, in the end
        # inherit from MarionetteTestResult
        own_attrs = ['passed', 'skipped', 'unexpected_passed', 'automation_failures', 'unexpected_failures', 'expected_failures']
        result_attrs = ['tests_passed', 'skipped', 'unexpectedSuccesses', 'errors', 'failures', 'expectedFailures']
        
        for result in self.runner.results:
            print "Result: {}".format(result)
            # We have to use len(), since result is an array of arrays containing the error reason
            result_values = [len(getattr(result, name)) for name in result_attrs] 
            map(self.update_attr, own_attrs, result_values)
            
        self.total = sum([getattr(self, own_attr) for own_attr in own_attrs])
    
    @property
    def _console_separator(self):
        columns = int(os.popen('stty size', 'r').read().split()[-1])
        return "#" * columns
        
    def display_results(self):
        print self._console_separator
        print "Click here for details\t\t\t\t\t: file://{}".format(self.runner.testvars['html_output'])
        print
        print "Start time\t\t\t\t\t\t: {}".format(self.start_time.strftime("%d/%m/%Y %H:%M"))
        print "End time\t\t\t\t\t\t: {}".format(self.end_time.strftime("%d/%m/%Y %H:%M"))
        print "Automation failures\t\t\t\t\t: {}".format(self.automation_failures)
        print "Test cases passed\t\t\t\t\t: {} / {}".format(self.passed, self.total)
        print "Unexpected failures\t\t\t\t\t: {}".format(self.unexpected_failures)
        print "Skipped tests\t\t\t\t\t\t: {}".format(self.skipped)
        print "Expected failures\t\t\t\t\t: {}".format(self.expected_failures)
        print self._console_separator
        
    def run(self):
        """
        Custom runner for OWD initiative
        It takes as arguments the parameters that gaiatest command would need
        For example:
            python ffox_test_runner_py --testvars=<testvars path> --address=localhost:2828 <tests path | test suite path>
        """
            
        parser = BaseMarionetteOptions(usage='%prog [options] test_file_or_dir <test_file_or_dir> ...')
        options, tests = parser.parse_args(self.args)
        parser.verify_usage(options, tests)
    
        self.runner = self.start_test_runner(self.runner_class, options, tests)
        self.process_runner_results()
        self.display_results()

if __name__ == "__main__":
    FfoxTestRunner(sys.argv[1:]).run()
