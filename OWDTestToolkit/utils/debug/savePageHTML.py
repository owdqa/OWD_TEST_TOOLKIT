from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def savePageHTML(self, p_outfile):
        #
        # Save the HTML of the current page to the specified file.
        #
        f = open(p_outfile, 'w')
        f.write( self.marionette.page_source.encode('ascii', 'ignore') )


