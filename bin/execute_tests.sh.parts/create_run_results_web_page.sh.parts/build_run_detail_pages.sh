#
# Create html versions of all the test case execution detail files.
#
ls $RESULT_DIR/*_detail 2>/dev/null | while read fnam
do
    #
    # Add some header info.
    #
    echo "<html>
    <head>
        <base target=\"_blank\">
        <link rel="stylesheet" type="text/css" href="run_html.css">
    </head>
    <body class=\"details\">" > $fnam.html
    
    #
    # Put the file contents in the html (change newlines to html code etc...).
    #
    sed -e "s/$/<br>/" $fnam              | \
    sed -e "s/ /\&nbsp/g"                 | \
    sed -e "s,\("$RESULT_DIR"\/\)\([^<]*\),<a href=\"\2\">"$HTML_WEBDIR"\2<\/a>,g"  >> $fnam.html
        
    #
    # Finish the file off.
    #
    echo "
    </body>
</html>" >> $fnam.html
    
done
