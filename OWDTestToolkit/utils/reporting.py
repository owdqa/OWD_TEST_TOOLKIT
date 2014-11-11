import time
import datetime
import codecs
import logging


class reporting(object):

    def __init__(self, parent, result, comment):
        self.parent = parent
        self._resultArray = result
        self._commentArray = comment

        self.det_fnam = parent.det_fnam
        self.sum_fnam = parent.sum_fnam
        self.testNum = parent.testNum
        self.logger = logging.getLogger('OWDTestToolkit')

    def logComment(self, p_str):
        #
        # Add a comment to the comment array.
        #
        self._commentArray.append(p_str)
        self.logger.info("Adding comment: {}".format(p_str))

    _subnote = "|__ "
    _no_time = "         "

    def log_to_file(self, message, level='info'):
        if level in ('critical', 'error', 'warn', 'info', 'debug'):
            f = self.logger.__getattribute__(level)
            f(message)
        else:
            self.logger.info(message)

    def critical(self, message):
        self.logger.critical(message)

    def error(self, message):
        self.logger.error(message)

    def warn(self, message):
        self.logger.warn(message)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def logResult(self, p_result, p_msg, p_fnam=False):
        #
        # Add a test result to the result array.
        # Everything after the first "|" is a 'note' line for this message
        # (will be put on a separate line with _subnote prefixed).
        #
        self.logger.info(u"Logging result: [{}] with message [{}]. p_fnam: {}".format(p_result, p_msg, p_fnam))
        if str(p_result).lower() == "info":
            timestamp = self._no_time
        elif str(p_result).lower() == "debug":
            timestamp = self._no_time
            p_msg = '<span style="color:c5c5c5;font-style:italic"><b>DEBUG NOTE:</b> ' + p_msg
        else:
            #
            # Set up timestamp and mark this as pass or fail.
            #
            time_now = time.time() - self.parent.last_timestamp
            time_now = round(time_now, 0)
            time_now = "[" + str(datetime.timedelta(seconds=time_now)) + "]"

            self.last_timestamp = time.time()

            _color = "#ff0000" if not p_result else "#00aa00"
            span_tag = '<span style="color:' + _color + '">'
            timestamp = span_tag + time_now + "</span>"

        # If we have filename details then add them to the message as note lines.
        if p_fnam:
            if len(p_fnam) == 2:
                p_msg = p_msg + "|current screenshot  = " + p_fnam[1]
                p_msg = p_msg + "|current html source = " + p_fnam[0]
            else:
                p_msg = p_msg + "|" + p_fnam

        p_msg = p_msg + "</span>"

        #
        # The double brackets is intentional (add a 2 part
        # array: true/false/info + message).
        #
        msgArr = p_msg.split("|")

        msgMain = msgArr[0]
        if str(p_result).lower() != "info" and str(p_result).lower() != "debug":
            #
            # This is a 'test' item so make it bold.
            #
            msgMain = span_tag + msgMain + "</span>"

        self._resultArray.append((self._no_time, "info", " "))  # (blank newline)
        self._resultArray.append((timestamp, p_result, msgMain))  # (the main message)

        #
        # Print subnote (only for failed and 'info' messages.
        #
        self._printSubNote(msgArr)

    def _printSubNote(self, msgArr):
        #
        # <i>Private</i> function for reporting. Used by the
        # 'utils' method 'logResult()' - do not call this
        # manually.
        #
        for i in range(1, len(msgArr)):  # (any 'notes' for this message)
            self._resultArray.append((self._no_time, "info", self._subnote + msgArr[i]))

    def reportResults(self):
        return
        #
        # Create output files (summary, which is displayed and
        # details, which is not displayed).
        #
        # NOTE: "XXDESCXX" is a marker that 'run_all_tests.sh' switches
        #       to the correct test description.
        #
        pass_str = "passed"
        fail_str = "FAILED"
        pass_span = "<span style='color:#00aa00'>"
        fail_span = "<span style='color:#ff0000'>"
        test_time = time.time() - self.parent.start_time
        test_time = round(test_time, 0)
        test_time = str(datetime.timedelta(seconds=test_time))

        detail_file = codecs.open(self.det_fnam, "w", encoding='utf-8')
        sum_file = codecs.open(self.sum_fnam, "w", encoding='utf-8')

        detail_file.write("<span style=\"font-size:14px\">")
        detail_file.write("<b>Test case</b>      : <b>{}</b>\n".format(self.testNum))
        detail_file.write("<b>Test desc</b>      : XXDESCXX\n")

        detail_file.write("<b>Time taken</b>     : {} (not including restarting device etc...)\n".format(test_time))

        boolStart = False
        for i in self._commentArray:
            if not boolStart:
                boolStart = True
                detail_file.write("<b>Comments</b>       : {}\n".format(i))
            else:
                detail_file.write("               : {}\n".format(i))

        if self.failed == 0:
            res_str = pass_str
            res_span = pass_span
        else:
            res_str = fail_str
            res_span = fail_span

        #
        # Get total number of tests performed.
        #
        total_tests = self.passed + self.failed

        #
        # Return summary information to stdout.
        #
        sum_file.write("{}\t{}\t{}".format(self.passed, self.failed, total_tests))

        #
        # Update details file.
        #
        detail_file.write("<b>Asserts passed</b> : {}\n".format(self.passed))
        detail_file.write("<b>Asserts failed</b> : {}\n".format(self.failed))
        detail_file.write("<b>Asserts result</b> : <b>{}{}</span></b>\n".format(res_span, res_str))
        detail_file.write("</span>")
        detail_file.write("\n")

        x = len(self._resultArray)
        if x > 0:
            for i in self._resultArray:
                try:
                    if i[1]:
                        detail_file.write(" " * (len(fail_str) + 2))
                    else:
                        detail_file.write("<span style=\"font-weight:bold;color:#ff0000\">*" + fail_str + "*</span>")
                    detail_file.write(" ")
                except:
                    # Sometimes a pass means that item [1] is an object!
                    detail_file.write(pass_str)

                detail_file.write(i[0])  # (Timestamp)
                # detail_file.write(" " + i[2].encode('ascii', 'ignore') + "\n")
                detail_file.write(" " + i[2] + "\n")

        detail_file.close()
        sum_file.close()
