import json
import os
import shutil
from csv_writer import CsvWriter


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
    def detect_device(testvars):
        """Customize parameters based on the DuT.
        """
        # Ensure device is connected and ports forwarded properly
        Utilities.connect_device()

        current_dut = os.popen("adb shell grep ro.product.name /system/build.prop").read().split("=")[-1].rstrip()
        devices_path = "{}/{}".format(testvars['toolkit_cfg']['toolkit_location'],
                                      testvars['toolkit_cfg']['devices_cfg'])
        devices_map = Utilities.parse_file(devices_path)

        if not current_dut in devices_map:
            print "No specific section for device [{}] was found. Falling down to [generic] device options.".\
                format(current_dut)
            current_dut = "generic"

        device_config = {}
        for item in devices_map[current_dut].keys():
            device_config["OWD_DEVICE_" + item.upper()] = devices_map[current_dut][item]

        for key in device_config.keys():
            testvars[key] = device_config[key]

    @staticmethod
    def connect_device():
        """Force connection to device and forward ports, just in case.
        """
        os.popen("adb kill-server")
        os.popen("adb devices")
        os.popen("adb forward tcp:2828 tcp:2828")

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
        fieldnames = ['START_TIME', 'DATE', 'TEST_SUITE', 'TEST_CASES_PASSED', 'FAILURES', 'AUTOMATION_FAILURES', \
                      'UNEX_PASSES', 'KNOWN_BUGS', 'EX_PASSES', 'IGNORED', 'UNWRITTEN', 'PERCENT_FAILED', 'DEVICE', \
                      'VERSION', 'BUILD', 'TEST_DETAILS']
        passes = test_runner.passed + test_runner.unexpected_passed
        failures = test_runner.expected_failures + test_runner.unexpected_failures + test_runner.automation_failures
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
        values = [test_runner.start_time.strftime("%d/%m/%Y %H:%M"), test_runner.end_time.strftime("%d/%m/%Y %H:%M"), \
                  run_id, "{} / {}".format(passes, totals), \
                  str(test_runner.unexpected_failures), \
                  str(test_runner.automation_failures), str(test_runner.unexpected_passed), \
                  str(test_runner.expected_failures), str(test_runner.passed), str(test_runner.skipped), "0", \
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
