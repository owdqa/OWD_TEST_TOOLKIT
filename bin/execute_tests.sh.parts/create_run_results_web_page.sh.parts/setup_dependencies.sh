#
# The directory that the physical files will be located for the web page.
#
HTML_FILEDIR=/var/www/html/owd_tests/$RUN_ID
if [ ! -d "$HTML_FILEDIR" ]
then
    sudo mkdir -p $HTML_FILEDIR
fi
sudo chmod 777 $HTML_FILEDIR

# 'sudo rm' so be paranoid!
if [ "$HTML_FILEDIR" ]
then
    cd $HTML_FILEDIR
    sudo rm -f * 2>/dev/null
    cd - >/dev/null
fi


#
# The url for this results web page.
#
HTML_WEBDIR="http://owd-qa-server/owd_tests/$RUN_ID"

#
# Functions for this script.
#
. $0.parts/f_sub_variables_into_webpage.sh
. $0.parts/f_convert_textfile_to_html.sh

#
# Some final variables before we start.
#
[ "$OWD_NO_BLOCKED" ] && blocked="No" || blocked="Yes"
[ "$OWD_USE_2ND_CHANCE" ] && chance2="Yes" || chance2="No"
