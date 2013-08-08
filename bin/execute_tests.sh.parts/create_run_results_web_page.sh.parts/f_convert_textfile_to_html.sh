#
# Create html version of the flat text file that is passed in.
#
f_convert_textfile_to_html(){
	
	fnam=$1
	
    #
    # Add some header info and make this a 'pre' (maintains any leading spaces and
    # lets us use our css styling for font etc...).
    #
    echo "<html>
    <head>
        <base target=\"_blank\">
        <link rel="stylesheet" type="text/css" href="run_html.css">
    </head>
    <body><pre>" > $fnam.html
    
    #
    # Put any possible 'real files' listed in here in a hyperlink.
    #
    sed -e "s,\("$RESULT_DIR"\/\)\([^<]*\),<a href=\"\2\">"$HTML_WEBDIR/"\2<\/a>,g" $fnam >> $fnam.html
        
    #
    # Finish the file off.
    #
    echo "
    </pre></body>
</html>" >> $fnam.html
    
}
