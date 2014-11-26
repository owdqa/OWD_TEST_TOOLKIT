import sys
import shutil
sys.path.insert(1, "../")
import os
import unittest
import logging.config
import re

from marionette import HTMLReportingTestRunnerMixin
from marionette import BaseMarionetteTestRunner
from gaiatest.runtests import GaiaTextTestRunner
from marionette.runner import BaseMarionetteOptions
from gaiatest import GaiaTestCase, GaiaTestRunnerMixin
from bs4 import BeautifulSoup
from datetime import datetime
from gaiatest.version import __version__

from OWDTestToolkit.utils.assertions import AssertionManager
from utilities import Utilities


class OWDMarionetteTestRunner(BaseMarionetteTestRunner):

    assertion_manager = AssertionManager()

    def run_test(self, filepath, expected, oop):
        """
        This method is responsible of running a single test.
        We've overrun it in order to perform some tasks belonging to OWD initiative.
        """
        #
        # Previous operations
        #
        idx = filepath.rindex('test_')
        # + 5: to skip the "test_" part
        # - 3: to remove the .py extension"""
        test_num = filepath[idx + 5:-3]

        desc_len = int(self.testvars['description_length'])
        if test_num in self.descriptions:
            description = self.descriptions[test_num][:desc_len] + "..."
        else:
            description = "Description not available..."

        if test_num in self.blocked_tests:
            description = "[BLOCKED] " + self.blocked_tests[test_num][:desc_len] + "..."
            expected = "fail"

        sys.stdout.write(u"{}: {:100s} ".format(test_num, description))
        sys.stdout.flush()

        # TODO - erase them when deleting reportResults
        self.testvars['TEST_NUM'] = test_num

        # Parent method -> start
        self.logger.info('TEST-START %s' % os.path.basename(filepath))

        testloader = unittest.TestLoader()
        suite = unittest.TestSuite()
        self.test_kwargs['expected'] = expected
        self.test_kwargs['oop'] = oop
        mod_name = os.path.splitext(os.path.split(filepath)[-1])[0]
        for handler in self.test_handlers:
            if handler.match(os.path.basename(filepath)):
                handler.add_tests_to_suite(mod_name, filepath, suite, testloader, self.marionette, self.testvars,
                                           **self.test_kwargs)
                break

        attempt = 0
        if suite.countTestCases():
            # Run the test. For that purpose, we have to instantiate the runnerclass, which, in this
            # this case, is MarionetteTextTestRunner
            runner = self.textrunnerclass(verbosity=int(self.testvars["verbosity"]),
                                          marionette=self.marionette,
                                          capabilities=self.capabilities)

            # This will redirect the messages that will go by default to the error output to another file
            runner.stream = unittest.runner._WritelnDecorator(open(self.testvars['error_output'], 'a'))

            # Temporary variable to store the total time used by all test retries, not only the last one.
            total_time = 0
            while attempt < self.testvars["test_retries"]:
                results = runner.run(suite)
                total_time += results.time_taken
                attempt += 1
                if len(results.errors) + len(results.failures) > 0:
                    suite._tests[0].restart = True
                    # If we have to reattempt, just substract the number of assertions to keep the results
                    # accurate
                    if attempt < self.testvars["test_retries"]:
                        self.assertion_manager.set_accum_passed(self.assertion_manager.get_accum_passed() -
                                                                self.assertion_manager.get_passed())
                        self.assertion_manager.set_accum_failed(self.assertion_manager.get_accum_failed() -
                                                                self.assertion_manager.get_failed())
                else:
                    break

            # Store the total time in the results, for the report
            results.time_taken = total_time
            # Store the total number of attempts done for this test, for the report
            results.attempts = attempt
            self.results.append(results)

            self.failed += len(results.failures) + len(results.errors)
            if hasattr(results, 'skipped'):
                self.skipped += len(results.skipped)
                self.todo += len(results.skipped)
            self.passed += results.passed
            for failure in results.failures + results.errors:
                self.failures.append((results.getInfo(failure), failure.output, 'TEST-UNEXPECTED-FAIL'))
            if hasattr(results, 'unexpectedSuccesses'):
                self.failed += len(results.unexpectedSuccesses)
                self.unexpected_successes += len(results.unexpectedSuccesses)
                for failure in results.unexpectedSuccesses:
                    self.failures.append((results.getInfo(failure), 'TEST-UNEXPECTED-PASS'))
            if hasattr(results, 'expectedFailures'):
                self.todo += len(results.expectedFailures)

        self.show_results(results)
        results.stream.flush()

    def get_result_msg(self, results):
        result_msg = None
        if len(results.errors) > 0:
            result_msg = "(automation fail) *"
        elif len(results.failures) > 0:
            result_msg = "(failed)  *"
        elif len(results.skipped) > 0:
            result_msg = "(skipped)"
        elif len(results.unexpectedSuccesses) > 0:
            result_msg = "(unblock?)"
        elif len(results.expectedFailures) > 0:
            result_msg = "(blocked)"
        else:
            result_msg = "(passed)"
        return result_msg

    def show_results(self, results):
        # Console messages - for each test, we will show the time taken to run it and the result
        hours = int(results.time_taken / 3600)
        hours_str = "{:02d}:".format(hours)
        mins = int((results.time_taken - hours * 3600) / 60)
        mins_str = "{:02d}:".format(mins)
        seconds = int(results.time_taken - (hours * 3600) - (mins * 60))
        seconds_str = "{:02d}".format(seconds)
        hundreds = int((results.time_taken - int(results.time_taken)) * 100)
        hundreds_str = ".{:02d}s".format(hundreds)
        time_string = "{:3s}{:3s}{}{}".format(hours_str if hours else "", \
                                      mins_str if mins else "", seconds_str, hundreds_str)
        sys.stdout.write("{} {:4s} {:20s} (assertions: {}/{})\n".\
                         format(time_string, "(x{})".format(results.attempts) if results.attempts > 1 else "",
                                self.get_result_msg(results),
                                OWDMarionetteTestRunner.assertion_manager.get_passed(),
                                OWDMarionetteTestRunner.assertion_manager.get_total()))


class OWDTestRunner(OWDMarionetteTestRunner, GaiaTestRunnerMixin, HTMLReportingTestRunnerMixin):
    """
    OWD runner class
    This class performs a bunch of tasks which are needed before and after running the test/s
    """
    textrunnerclass = GaiaTextTestRunner

    def __init__(self, **kwargs):

        BaseMarionetteTestRunner.__init__(self, **kwargs)

        # Some initial steps going through!
        self.parse_blocked_tests_file()
        self.parse_descriptions_file()
        # Store the toolkit location to infer the location of some files relative to it, such as
        # the devices config or the css template
        self.testvars['toolkit_location'] = kwargs['toolkit_location']
        Utilities.detect_device(self.testvars)

        GaiaTestRunnerMixin.__init__(self, **kwargs)
        HTMLReportingTestRunnerMixin.__init__(self, name='gaiatest-v2.0', version=__version__,
                                              html_output=self.testvars['html_output'], **kwargs)
        self.test_handlers = [GaiaTestCase]

    def parse_descriptions_file(self):
        self.descriptions = Utilities.parse_file(self.testvars['test_descriptions'])

    def parse_blocked_tests_file(self):
        self.blocked_tests = Utilities.parse_file(self.testvars['blocked_tests'])

    def prepare_results(self):
        """ This methods ensures that the destination results directory is created before launching the
        test/s execution. It also creates (or cleans) the html results report file and the error_output file
        """
        if not os.path.exists(self.testvars['RESULT_DIR']):
            os.makedirs(self.testvars['RESULT_DIR'])

        def _initialize_file(file_path):
            with open(file_path, 'w') as f:
                f.close()

        # We will redirect BaseMarionetteTestRunner default logger to our own logger.
        # Loggers are not directly instantiated, but created by calling loggin.getLogger.
        # Multiple calls to getLogger with the same name will point to the same logger
        # reference
        config_file = self.testvars['OWD_LOG_CFG']
        logging.config.fileConfig(config_file)
        self.logger = logging.getLogger('OWDTestToolkit')

        files = [self.testvars['html_output'], self.testvars['error_output'], self.testvars["log_path"]]
        map(_initialize_file, files)


class Main():

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
        self.assertion_manager = AssertionManager()
        self.assertion_manager.reset()

    def start_test_runner(self, runner_class, options, tests):
        """
        This method instantiates the class responsible of running the tests and run them.
        Returns the runner instances itself so that we can access to the results
        """
        self.start_time = datetime.utcnow()
        runner = runner_class(**vars(options))
        runner.prepare_results()
        runner.run_tests(tests)
        self.end_time = datetime.utcnow()
        return runner

    def update_attr(self, attr_name, attr_value):
        """
        Updates the "attr_name" attribute with the desired "attr_value"
        """
        setattr(self, attr_name, getattr(self, attr_name) + attr_value)

    def process_runner_results(self):
        """
        This method takes the results contained in the instance of runner (it assumes the runner has been run, ofc)
        and update the class attributes accordingly, so that they can be displayed afterwards.
        NOTE: since self.test_handlers is GaiaTestCase, the results will be instances of GaiaTestResult which, in the
        end, inherit from MarionetteTestResult
        """
        own_attrs = ['passed', 'skipped', 'unexpected_passed', 'automation_failures', 'unexpected_failures',
                     'expected_failures']
        result_attrs = ['tests_passed', 'skipped', 'unexpectedSuccesses', 'errors', 'failures', 'expectedFailures']

        for result in self.runner.results:
            # We have to use len(), since result is an array of arrays containing the error reason
            result_values = [len(getattr(result, name)) for name in result_attrs]
            map(self.update_attr, own_attrs, result_values)

        self.total = len(self.runner.results)

    @property
    def _console_separator(self):
        columns = int(os.popen('stty size', 'r').read().split()[-1])
        return "#" * columns

    def display_results(self):
        print
        print self._console_separator
        print "Click here for details\t\t\t\t\t: file://{}".format(self.runner.testvars['html_output'])
        print
        print "Start time\t\t\t\t\t\t: {}".format(self.start_time.strftime("%d/%m/%Y %H:%M"))
        print "End time\t\t\t\t\t\t: {}".format(self.end_time.strftime("%d/%m/%Y %H:%M"))
        print "Automation failures\t\t\t\t\t: {}".format(self.automation_failures)
        print "Test cases passed\t\t\t\t\t: {} / {}".format(self.passed, self.total)
        print "Unexpected failures\t\t\t\t\t: {}".format(self.unexpected_failures)
        print "Unexpected passes\t\t\t\t\t: {}".format(self.unexpected_passed)
        print "Skipped tests\t\t\t\t\t\t: {}".format(self.skipped)
        print "Expected failures\t\t\t\t\t: {}".format(self.expected_failures)
        print "Passes/Total assertions\t\t\t\t\t: {} / {}".format(self.assertion_manager.accum_passed,
                                                                  self.assertion_manager.accum_total)
        print self._console_separator
        print

    def edit_html_results(self):
        results_file = open(self.runner.testvars['html_output'])
        soup = BeautifulSoup(results_file)
        results_file.close()

        test_nums = [re.search('^test_(.*).*$', testname.string.strip()).group(1)
                     for testname in soup.find_all("td", class_="col-class")]
        col_links = soup.find_all("td", class_="col-links")
        i = 0
        for link in col_links:
            detail_tag = soup.new_tag("a", href="details/{}_detail.html".format(test_nums[i]),
                                      class_="details", target="_blank")
            detail_tag.string = "Details"
            link.append(detail_tag)
            i += 1

        results_file = open(self.runner.testvars['html_output'], 'w')
        results_file.write(soup.prettify("utf-8"))
        results_file.close()

    def edit_test_details(self):
        for result in self.runner.results:
            # TODO: look if there's another way of getting the test_number
            test_number = re.search('test_(.*).*$', result.tests.next().test_name).group(1)
            detail_file_path = "{}/{}_detail.html".format(self.runner.testvars['RESULT_DIR'], test_number)

            try:
                detail_file = open(detail_file_path)
            except IOError:
                return

            soup = BeautifulSoup(detail_file)
            detail_file.close()

            description_tag = soup.find("span", id='test-description')
            description_tag.string = self.runner.descriptions[test_number]
            duration_tag = soup.find("span", id='duration')
            duration_tag.string = "{:.2f} seconds".format(result.time_taken)
            result_tag = soup.find("div", id="result-container")
            test_result = self.runner.get_result_msg(result).strip()
            new_tag = soup.new_tag("span", id="result", **{'class': test_result.replace(" ", "-")})
            new_tag.string = test_result
            result_tag.append(new_tag)

            detail_file = open(detail_file_path, "w")
            detail_file.write(soup.prettify())
            detail_file.close()

            # Copy the css file
            css_path = "{}/{}".format(self.runner.testvars['toolkit_location'],
                                      self.runner.testvars['toolkit_cfg']['css_file'])
            shutil.copy(css_path, self.runner.testvars['RESULT_DIR'])

    def run(self):
        """
        Custom runner for OWD initiative
        It takes as arguments the parameters that gaiatest command would need
        For example:
            python ffox_test_runner_py --testvars=<testvars path> --address=localhost:2828 <tests path |\
            test suite path>
        """

        # Preprocess
        parser = BaseMarionetteOptions(usage='%prog [options] test_file_or_dir <test_file_or_dir> ...')
        options, tests = parser.parse_args(self.args[1:])
        parser.verify_usage(options, tests)

        location = self.parse_toolkit_location(self.args)
        options.toolkit_location = location

        # Hit the runner
        self.runner = self.start_test_runner(self.runner_class, options, tests)

        # Show the results via console and prepare the details
        self.process_runner_results()
        self.edit_html_results()
        self.edit_test_details()
        self.display_results()

    def parse_toolkit_location(self, args):
        path = args[0]
        index = path.find('/scripts/ffox_test_runner.py')
        return path[:index]

if __name__ == "__main__":
    Main(sys.argv).run()
