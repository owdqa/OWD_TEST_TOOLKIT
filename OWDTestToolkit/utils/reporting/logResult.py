from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    _subnote  = " |__ ";
    _no_time  = "          " #(10 spaces)
    
    def logResult(self, p_result, p_msg, p_fnam=False):
        #
        # Add a test result to the result array.
        # Everything after the first "|" is a 'note' line for this message
        # (will be put on a separate line with _subnote prefixed).
        #

        # Get timestamp.        
        time_now   = time.time() - self.last_timestamp
        time_now   = round(time_now, 0)
        time_now   = "[" + str(datetime.timedelta(seconds=time_now)) + "]"

        self.last_timestamp = time.time()
        
        if str(p_result).lower() == "info":
            timestamp = self._no_time 
        else: 
            timestamp = time_now

        
        # If we have filename details then add them to the message as note lines.
        if p_fnam:
            p_msg = p_msg + "|current html source = " + p_fnam[0]
            p_msg = p_msg + "|current screenshot  = " + p_fnam[1]

        #
        # The double brackets is intentional (add a 2 part
        # array: true/false/info + message).
        #
        msgArr = p_msg.split("|")
        self._resultArray.append((self._no_time, "info", " "))          # (blank newline)
        self._resultArray.append((timestamp, p_result, msgArr[0])) # (the main message)
        
        if p_result:
            #
            # Don't add the subnotes if this was just a test that passed.
            #
            if not str(p_result) == "info":
                return
        else:
            #
            # Result = False, mark this up!
            #
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
        for i in range(1, len(msgArr)):                 # (any 'notes' for this message)
            self._resultArray.append((self._no_time,"info", self._subnote + msgArr[i]))
        