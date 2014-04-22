import time
import datetime
import codecs


class reporting(object):

    def __init__(self, parent, result, comment):
        self.parent = parent
        self._resultArray = result
        self._commentArray = comment
        self.passed = parent.passed
        self.failed = parent.failed
        self.det_fnam = parent.det_fnam
        self.sum_fnam = parent.sum_fnam
        self.testNum = parent.testNum

    def logComment(self, p_str):
        #
        # Add a comment to the comment array.
        #
        self._commentArray.append(p_str)

    _subnote = "|__ "
    _no_time = "         "

    def logResult(self, p_result, p_msg, p_fnam=False):
        #
        # Add a test result to the result array.
        # Everything after the first "|" is a 'note' line for this message
        # (will be put on a separate line with _subnote prefixed).
        #

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

        if str(p_result).lower() != "info" and str(p_result).lower() != "debug":
            if p_result:
                self.passed = self.passed + 1
                return
            else:
                self.failed = self.failed + 1

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

        #DET_FILE = open(self.det_fnam, "w")
        DET_FILE = codecs.open(self.det_fnam, "w", encoding='utf-8')
        SUM_FILE = open(self.sum_fnam, "w")

        DET_FILE.write("<span style=\"font-size:14px\">")
        DET_FILE.write("<b>Test case</b>      : <b>{}</b>\n".format(self.testNum))
        DET_FILE.write("<b>Test desc</b>      : XXDESCXX\n")

        DET_FILE.write("<b>Time taken</b>     : {} (not including restarting device etc...)\n".format(test_time))

        boolStart = False
        for i in self._commentArray:
            if not boolStart:
                boolStart = True
                DET_FILE.write("<b>Comments</b>       : {}\n".format(i))
            else:
                DET_FILE.write("               : {}\n".format(i))

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
        SUM_FILE.write("{}\t{}\t{}".format(self.passed, self.failed, total_tests))

        #
        # Update details file.
        #
        DET_FILE.write("<b>Asserts passed</b> : {}\n".format(self.passed))
        DET_FILE.write("<b>Asserts failed</b> : {}\n".format(self.failed))
        DET_FILE.write("<b>Asserts result</b> : <b>{}{}</span></b>\n".format(res_span, res_str))
        DET_FILE.write("</span>")
        DET_FILE.write("\n")

        x = len(self._resultArray)
        if x > 0:
            for i in self._resultArray:
                try:
                    if i[1]:
                        DET_FILE.write(" " * (len(fail_str) + 2))
                    else:
                        DET_FILE.write("<span style=\"font-weight:bold;color:#ff0000\">*" + fail_str + "*</span>")
                    DET_FILE.write(" ")
                except:
                    # Sometimes a pass means that item [1] is an object!
                    DET_FILE.write(pass_str)

                DET_FILE.write(i[0])  # (Timestamp)
                #DET_FILE.write(" " + i[2].encode('ascii', 'ignore') + "\n")
                DET_FILE.write(" " + i[2] + "\n")

        DET_FILE.close()
        SUM_FILE.close()
