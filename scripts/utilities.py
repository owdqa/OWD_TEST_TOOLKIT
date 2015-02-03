import json
import pygal
import os
import shutil
from csv_writer import CsvWriter
from pygal.style import Style
import subprocess32


class Utilities():

    @staticmethod
    def parse_file(file_name):
        """ Generic JSON parser.

        It takes a JSON file as an input and returns a dictionary containing all
        its properties.
        """
        the_file = open(file_name)
        data = json.load(the_file)
        the_file.close()
        return data

    @staticmethod
    def connect_device():
        """Force connection to device and forward ports, just in case.
        """
        with open(os.devnull, 'w') as DEVNULL:
            subprocess32.call('adb kill-server', shell=True, stderr=DEVNULL, stdout=DEVNULL)
            subprocess32.call('adb devices', shell=True, stderr=DEVNULL, stdout=DEVNULL)
            subprocess32.call('adb forward tcp:2828 tcp:2828', shell=True, stderr=DEVNULL, stdout=DEVNULL)

    @staticmethod
    def generate_csv_reports(test_runner, is_cert=False):
        """Generate CSV reports with the results of the test.

        Generate an entry in the weekly CSV report and another one in the daily CSV report
        if required. If is_cert is True, it will use different values for device, branch
        and buildname than the ones detected automatically.
        """
        is_ci_server = os.getenv("ON_CI_SERVER")
        # Provide a default value so that call to find works even if the variable does not exist
        is_by_test_suite = os.getenv("RUN_ID", "").find("testing_by_TEST_SUITE")
        if (not is_ci_server or is_by_test_suite != -1) and not is_cert:
            return
        fieldnames = ['START_TIME', 'DATE', 'TEST_SUITE', 'TEST_CASES_PASSED', 'FAILURES', 'AUTOMATION_FAILURES',
                      'UNEX_PASSES', 'KNOWN_BUGS', 'EX_PASSES', 'IGNORED', 'UNWRITTEN', 'PERCENT_FAILED', 'DEVICE',
                      'VERSION', 'BUILD', 'TEST_DETAILS']
        passes = test_runner.passed + test_runner.unexpected_passed
        failures = test_runner.unexpected_failures + test_runner.automation_failures
        totals = passes + failures
        error_rate = float(failures * 100) / totals
        device = os.getenv("DEVICE") if not is_cert else test_runner.runner.testvars["device_cert"]
        branch = os.getenv("BRANCH") if not is_cert else test_runner.runner.testvars["branch_cert"]
        run_id = os.getenv("RUN_ID")
        buildname_var = os.getenv("DEVICE_BUILDNAME") if not is_cert else test_runner.runner.testvars["buildname_cert"]
        print "Device: {}   Branch: {}  Run id: {}  Device buildname: {}".format(device, branch, run_id, buildname_var)
        index = buildname_var.find(".Gecko")
        buildname = buildname_var[:index]
        index = -1
        filedir = ""
        html_webdir = test_runner.runner.testvars['output']['webdir'] + "/{}/{}/{}".format(device, branch, run_id)
        on_ci_server = os.getenv("ON_CI_SERVER")
        if on_ci_server:
            index = html_webdir.find("owd_tests")
            filedir = html_webdir[index + 9:]
        else:
            filedir = test_runner.runner.testvars['output']['html_output']
        values = [test_runner.start_time.strftime("%d/%m/%Y %H:%M"), test_runner.end_time.strftime("%d/%m/%Y %H:%M"),
                  run_id, "{} / {}".format(passes, totals),
                  str(test_runner.unexpected_failures),
                  str(test_runner.automation_failures), str(test_runner.unexpected_passed),
                  str(test_runner.expected_failures), str(test_runner.passed), str(test_runner.skipped), "0",
                  "{:.2f}".format(error_rate), device, branch, buildname, filedir]
        weekly_file = '/var/www/html/owd_tests/total_csv_file.csv'
        daily_file = '/var/www/html/owd_tests/{}/{}/partial_csv_file_NEW.csv'.format(device, branch)
        csv_writer = CsvWriter(device, branch)
        csv_writer.create_report(fieldnames, dict(zip(fieldnames, values)), weekly_file, False)
        csv_writer.create_report(fieldnames, dict(zip(fieldnames, values)), daily_file)
        if on_ci_server:
            Utilities.persist_result_files(test_runner.runner.testvars, device, branch, run_id)

    @staticmethod
    def persist_result_files(testvars, device, branch, suite):
        """Move the result files to their persistent location.

        Result and error files are stored in a temporary location while the suite
        is running. In order to preserve them from being deleted or overwritten between
        executions, they must be moved to a permanent location, given by the device, branch
        and suite names.
        """
        dstdir = '{}/{}/{}/{}'.format(testvars['output']['persistent_dir'], device, branch, suite)

        # Move the details directory to dstdir
        shutil.move(testvars['output']['result_dir'], dstdir + '/details')

        # Move the results file, changing also its name to index
        result_file = testvars['output']['html_output']
        shutil.move(result_file, dstdir + '/index.html')

        # Move the errors file to the same location
        shutil.move(testvars['output']['error_output'], dstdir)


class Graphics(object):

    def __init__(self, **kwargs):
        self.custom_style = Style(
            background='#073642',
            plot_background='#002b36',
            foreground='#839496',
            foreground_light='#fdf6e3',
            foreground_dark='#657b83',
            opacity='.66',
            opacity_hover='.9',
            transition='500ms ease-in',
            colors=('#20C72E', '#EB0C35', '#F06B0C', '#0404B4', '#CFF73E', '#6E6E6E'))

        self._POSSIBLE_RESULTS = ['Passed', 'Failed', 'Automation Failed', 'Blocked', 'Unblock', 'Skipped']
        self.results_by_suite = kwargs.pop('results_by_suite')
        self.total_results_count = kwargs.pop('total_results_count')
        self.output_dir = kwargs.pop('output_dir')
        self.suites = sorted(self.results_by_suite.keys())

        self.total_results_percentages = self._get_test_run_percentages()
        self.results_occurrences_by_suite = self._calculate_result_occurrences_by_suite()

    def _calculate_result_occurrences_by_suite(self):
        """
        Returns an array of arrays contains the ocurrences of each possible test result for each suite
        Thus, it always has 6 elements, corresponding to the possible values (see above)
        Each element, is an array containing the occurrences of that values for each suite, so it'll
        have as many elements as suites being run

        Example: running 2 suites, A and B

                   Passed       Failed       AF        blocked     Unblock     Skipped
        Results: [ [2, 1],     [0, 1],     [1, 0],     [0, 0],     [0, 0],     [0, 0] ]
                    |  |        |  |        |  |        |  |        |  |        |  |
                    |  B        |  B        |  B        |  B        |  B        |  B
                    A           A           A           A           A           A
        """
        return [[self.results_by_suite[suite].count(pv) for suite in self.suites] for pv in self._POSSIBLE_RESULTS]

    def _get_test_run_percentages(self):
        def _get_percentage(result_type):
            return float(result_type) / total * 100
        total = sum(self.total_results_count)
        return map(_get_percentage, self.total_results_count)

    def generate_all_graphics(self):
        self.suite_graphic(self.results_occurrences_by_suite, self._POSSIBLE_RESULTS, self.suites, self.output_dir)
        self.total_results_graphic(self.total_results_percentages, self._POSSIBLE_RESULTS, self.output_dir)

    def suite_graphic(self, results, legend, labels, output):
        bar_chart = pygal.StackedBar(
            x_label_rotation=45, style=self.custom_style, title_font_size=24, label_font_size=16, tooltip_font_size=16)
        bar_chart.x_labels = map(str.capitalize, labels)
        bar_chart.title = 'TESTRUN RESULTS by SUITE'
        for index, result in enumerate(results):
            bar_chart.add(legend[index], result)
        bar_chart.render_to_png("{}/{}".format(output, "results_suites.png"))
        bar_chart.render_to_file("{}/{}".format(output, "results_suites.svg"))

    def total_results_graphic(self, results, legend, output):
        pie_chart = pygal.Pie(
            x_label_rotation=30, style=self.custom_style, title_font_size=24, label_font_size=16, tooltip_font_size=16)
        pie_chart.title = 'TESTRUN RESULTS'
        for index, result in enumerate(results):
            pie_chart.add(legend[index], result)
        pie_chart.render_to_png("{}/{}".format(output, "results_total.png"))
        pie_chart.render_to_file("{}/{}".format(output, "results_total.svg"))
