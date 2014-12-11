import sys
import shutil
sys.path.insert(1, "../")
import os
import re
import random

from marionette import HTMLReportingTestRunnerMixin
from marionette import BaseMarionetteTestRunner
from gaiatest.runtests import GaiaTextTestRunner
from marionette.runner import BaseMarionetteOptions
from marionette import expected
from gaiatest import GaiaTestCase, GaiaTestRunnerMixin
from bs4 import BeautifulSoup
from datetime import datetime
from gaiatest.version import __version__
from mozlog import structured

from OWDTestToolkit.utils.assertions import AssertionManager
from utilities import Utilities


class OWDMarionetteTestRunner(BaseMarionetteTestRunner):

    assertion_manager = AssertionManager()

    def _show_test_info(self, filepath):
        """
        This method is responsible of running a single test.
        We've overrun it in order to perform some tasks belonging to OWD initiative.
        """
        # Extract the test identifier
        idx = filepath.rindex('test_')
        # + 5: to skip the "test_" part
        # - 3: to remove the .py extension"""
        test_num = filepath[idx + 5:-3]

        desc_len = int(self.testvars['general']['description_length'])
        if test_num in self.descriptions:
            description = self.descriptions[test_num][:desc_len] + "..."
        else:
            description = "Description not available..."

        if test_num in self.blocked_tests:
            description = "[BLOCKED] " + self.blocked_tests[test_num][:desc_len] + "..."
            expected = "fail"

        sys.stdout.write(u"{}: {:103s} ".format(test_num, description))
        sys.stdout.flush()
    
    def run_test_set(self, tests):
        if self.shuffle:
            random.seed(self.shuffle_seed)
            random.shuffle(tests)
        
        for test in tests:
            attempt = 0
            total_time = 0
            self._show_test_info(test['filepath'])
            while attempt < self.testvars['general']['test_retries']:
                self.run_test(test['filepath'], test['expected'], test['oop'])
                result = self.results[-1]
                total_time += result.time_taken
                # Be careful, now self.results is a list of GaiaTestResult
                attempt += 1
                if len(result.errors) + len(result.failures) > 0:
                    # If we have to reattempt, just substract the number of assertions to keep the results
                    # accurate
                    if attempt < self.testvars['general']["test_retries"]:
                        print "Restarting device!!!!"
                        self.assertion_manager.set_accum_passed(self.assertion_manager.get_accum_passed() -
                                                                self.assertion_manager.get_passed())
                        self.assertion_manager.set_accum_failed(self.assertion_manager.get_accum_failed() -
                                                                self.assertion_manager.get_failed())
                        # Remove this result from results list, because now we call run_test() twice and we'll
                        # get as many results as retries we've configured, and we're only interested in the last one
                        self.results.pop(-1)
                        
                        # Tell the suite that we have to restart the device for next test (the retry)
                        self.test_kwargs['restart'] = True
                else:
                    break
                
                if self.marionette.check_for_crash():
                    break
                
                # Store the total time in the results, for the report
                result.time_taken = total_time
                # Store the total number of attempts done for this test, for the report
                result.attempts = attempt
            
            # Reset restart (if needed) for the upcoming test
            try:
                self.test_kwargs.pop('restart')
            except KeyError:
                pass
            self.show_results(result)
            result.stream.flush()
    
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


class OWDTestRunner(OWDMarionetteTestRunner, GaiaTestRunnerMixin,HTMLReportingTestRunnerMixin):
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
        self.testvars['toolkit_cfg']['toolkit_location'] = kwargs['toolkit_location']
        Utilities.detect_device(self.testvars)

        GaiaTestRunnerMixin.__init__(self, **kwargs)
        HTMLReportingTestRunnerMixin.__init__(self, name='gaiatest-v2.0', version=__version__,
                                              html_output=self.testvars['output']['html_output'], **kwargs)
        self.test_handlers = [GaiaTestCase]

    def parse_descriptions_file(self):
        self.descriptions = Utilities.parse_file(self.testvars['general']['test_descriptions'])

    def parse_blocked_tests_file(self):
        self.blocked_tests = Utilities.parse_file(self.testvars['general']['blocked_tests'])

    def prepare_results(self):
        """ This methods ensures that the destination results directory is created before launching the
        test/s execution. It also creates (or cleans) the html results report file and the error_output file
        """
        if not os.path.exists(self.testvars['output']['result_dir']):
            os.makedirs(self.testvars['output']['result_dir'])

        def _initialize_file(file_path):
            with open(file_path, 'w') as f:
                f.close()

        files = [self.testvars['output']['html_output'], self.testvars['output']['error_output']]
        map(_initialize_file, files)
    
    def start_httpd(self, need_external_ip):
        super(OWDTestRunner, self).start_httpd(need_external_ip)
        self.httpd.urlhandlers.append({
            'method': 'GET',
            'path': '.*\.webapp',
            'function': self.webapp_handler})

    def webapp_handler(self, request):
        with open(os.path.join(self.server_root, request.path[1:]), 'r') as f:
            data = f.read()
        return (200, {
            'Content-type': 'application/x-web-app-manifest+json',
            'Content-Length': len(data)}, data)


class TestRunner():

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
        self.start_time = datetime.now()
        runner = runner_class(**vars(options))
        runner.prepare_results()
        runner.run_tests(tests)
        self.end_time = datetime.now()
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
        try:
            columns = int(os.popen('stty size', 'r').read().split()[-1])
        except Exception:
            columns = 120
        return "#" * columns

    def display_results(self):
        print
        print self._console_separator
        print "Click here for details\t\t\t\t\t: file://{}".format(self.runner.testvars['output']['html_output'])
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
        """
        Edits general result html file adding for each test run, a link to its detail file
        """
        results_file = open(self.runner.testvars['output']['html_output'])
        soup = BeautifulSoup(results_file)
        results_file.close()

        test_nums = [re.search('test_(\w*).*$', testname.string.strip()).group(1)
                     for testname in soup.find_all("td", class_="col-class")]
        col_links = soup.find_all("td", class_="col-links")
        i = 0
        for link in col_links:
            detail_tag = soup.new_tag("a", href="details/{}_detail.html".format(test_nums[i]),
                                      class_="details", target="_blank")
            detail_tag.string = "Details"
            link.append(detail_tag)
            i += 1

        results_file = open(self.runner.testvars['output']['html_output'], 'w')
        results_file.write(soup.prettify("utf-8"))
        results_file.close()

    def edit_test_details(self):
        """
        This method edits each of the detail files created during the test/suite execution
        and adds some information (result, time taken...) which could only be know a posteriori.
        """
        
        for result in self.runner.results:
            # TODO: look if there's another way of getting the test_number
            test_number = re.search('test_(\w*).*$', result.tests.next().test_name).group(1)
            detail_file_path = "{}/{}_detail.html".format(self.runner.testvars['output']['result_dir'], test_number)

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
            test_result = re.search("^\((.*)\).*$", self.runner.get_result_msg(result).strip()).group(1)
            new_tag = soup.new_tag("span", id="result", **{'class': test_result})
            new_tag.string = test_result
            result_tag.append(new_tag)

            detail_file = open(detail_file_path, "w")
            detail_file.write(soup.prettify())
            detail_file.close()

            # Copy the css file
            css_path = "{}/{}".format(self.runner.testvars['toolkit_cfg']['toolkit_location'],
                                      self.runner.testvars['toolkit_cfg']['css_file'])
            shutil.copy(css_path, self.runner.testvars['output']['result_dir'])

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
        structured.commandline.add_logging_group(parser)
        options, tests = parser.parse_args(self.args[1:])
        parser.verify_usage(options, tests)
        
        logger = structured.commandline.setup_logging(options.logger_name, options) #{"mach": open("/tmp/tests/tests.log", "a")})
        options.logger = logger
        
        # Remove default stdout logger from mozilla logger
        to_delete = filter(lambda h: h.stream.name == '<stdout>', logger.handlers)
        for d in to_delete:
            logger.remove_handler(d)

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
    TestRunner(sys.argv).run()