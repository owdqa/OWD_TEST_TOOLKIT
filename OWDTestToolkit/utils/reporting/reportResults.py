from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def reportResults(self):
        #
        # Clear out 'things' left by previous tests, then
        # Create the final result file from the result and comment arrays
        # (run only once, at the end of each test case).
        #
        self.clearAllStatusBarNotifs(p_silent=True)

        #
        # Create output files (summary, which is displayed and
        # details, which is not displayed).
        #
        pass_str      = "         "
        fail_str      = "*FAILED* "
        blocked_str   = "(blocked)"
        unblocked_str = "*unblock*"
        test_time     = time.time() - self.start_time
        test_time     = round(test_time, 0)
        test_time     = str(datetime.timedelta(seconds=test_time))

        DET_FILE    = open(self.det_fnam, "w")
        SUM_FILE    = open(self.sum_fnam, "w")

        DET_FILE.write("Test case  : %s\n" % self.testNum)
        DET_FILE.write("Description: %s\n" % self.testDesc)
        DET_FILE.write("Time taken : %s\n" % str(test_time))

        boolStart = False
        for i in self._commentArray:
            if not boolStart:
                boolStart = True
                DET_FILE.write("Comments   : %s\n" % i)
            else:
                DET_FILE.write("           : %s\n" % i)
        
        res_str = pass_str if self.failed == 0 else fail_str
        res_str = blocked_str   if (res_str == fail_str and "BLOCKED BY" in self.testDesc) else res_str
        res_str = unblocked_str if (res_str == pass_str and "BLOCKED BY" in self.testDesc) else res_str

        #
        # Get total number of tests performed.
        #
        x = self.passed + self.failed
        y = x - self.failed
        
        totals = "%s/%s" % (str(y).rjust(3), str(x).ljust(3))
        if len(self.testDesc) > 80:
            self.testDesc = self.testDesc[:76] + " ..."

        SUM_FILE.write("#%s %s (%s - %s): %s.\n" % (
                                                  self.testNum.ljust(5),
                                                  res_str.ljust(9),
                                                  str(test_time),
                                                  totals.center(7),
                                                  self.testDesc.ljust(80)
                                                  )
                       )
        
        DET_FILE.write("Passed     : %s\n" % str(self.passed))
        DET_FILE.write("Failed     : %s\n" % str(self.failed))
        DET_FILE.write("RESULT     : %s\n" % res_str)
        DET_FILE.write("\n")

        x = len(self._resultArray)
        boolFail = False
        if x > 0:
            for i in self._resultArray:
                try:
                    if i[1]:
                        DET_FILE.write(pass_str)
                    else:
                        DET_FILE.write(fail_str)                        
                except:
                    # Sometimes a pass means that item [1] is an object!
                    DET_FILE.write(pass_str)
                    
                DET_FILE.write(i[0]) # (Timestamp)

                DET_FILE.write(" " + i[2] + "\n")
        
        DET_FILE.close()
        SUM_FILE.close()
