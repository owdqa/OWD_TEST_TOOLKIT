from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def getStackTrace(self):
        #
        # Adds the stack trace to the test report.
        #
        import traceback
        from inspect import stack
        
        _style      = "<span style='color:#7a7a7a'>"
            
        _logstr     = "CODE TRACE:"     
        _stack      = traceback.extract_stack()
        _counter    = 0
        
        for i in _stack:
            if  ("OWDTestToolkit" in i[0] or "/test_" in i[0])  and \
                "quitTest.py" not in i[0]                       and \
                i[2] != stack()[0][3]                           and \
                i[2] != "TEST":
                    _counter = _counter + 1
                    _logstr  = _logstr + "|%s. %s: <i>%s</i>" % \
                                (_counter,
                                 ("<b>" + os.path.basename(i[0]) + "</b>(%s)" % i[1]).ljust(40),
                                 i[3])
        
        self.logResult("info", "%s%s</span>" % (_style, _logstr))

