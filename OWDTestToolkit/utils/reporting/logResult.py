from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    _subnote  = "|__ ";
    _no_time  = "         " #(10 spaces)
    
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
            p_msg     = '<span style="color:c5c5c5;font-style:italic"><b>DEBUG NOTE:</b> ' + p_msg
        else:
            #
            # Set up timestamp and mark this as pass or fail.
            #
            time_now   = time.time() - self.last_timestamp
            time_now   = round(time_now, 0)
            time_now   = "[" + str(datetime.timedelta(seconds=time_now)) + "]"
    
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
            
        self._resultArray.append((self._no_time, "info", " "))     # (blank newline)
        self._resultArray.append((timestamp, p_result, msgMain)) # (the main message)
        
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
        for i in range(1, len(msgArr)):                 # (any 'notes' for this message)
            self._resultArray.append((self._no_time,"info", self._subnote + msgArr[i]))
        