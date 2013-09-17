#!/bin/bash
#
# Comments out certain parts of "gaia_test.py" (for various reasons).
#

. $HOME/.OWD_TEST_TOOLKIT_LOCATION
export GAIATEST=$OWD_TEST_TOOLKIT_DIR/gaia/tests/python/gaia-ui-tests/gaiatest/gaia_test.py
awk '
BEGIN{
	GAIATEST   = ENVIRON["GAIATEST"]
	IN_CLEANUP = 0
	IN_WIFI    = 0
	while ( getline < GAIATEST ){
		#
		# We have problems just now with the cleanUp() method of gaia_test.py sometimes, 
		# in the "wifi" section.
		#
	    if ( $0 ~ /def *cleanUp/ ){
            IN_CLEANUP = 1
        }
        if ( IN_CLEANUP == 1 && $0 ~ /if self.device.has_wifi/ ){
			IN_WIFI = 1
			$0 = "#" $0
		}
	    if ( IN_CLEANUP == 1 && IN_WIFI == 1 && $0 ~ /self.data_layer.enable_wifi/ ){
            $0 = "#" $0
        }
	    if ( IN_CLEANUP == 1 && IN_WIFI == 1 && $0 ~ /self.data_layer.forget_all_networks/ ){
            $0 = "#" $0
        }
		if ( IN_CLEANUP == 1 && IN_WIFI == 1 && $0 ~ /self.data_layer.disable_wifi/ ){
            $0 = "#" $0
            IN_WIFI = 0
            IN_CLEANUP = 0
		}
		
		#
		# We don not need the timezone to be reset to USA.
		#
		if ( IN_CLEANUP == 1 && $0 ~ /self.data_layer.set_setting/ && $0 ~ /timezone/ ){
			$0 = "#" $0
		}
		
		print $0
		
	}
}' > /tmp/gaiatest.tmp

mv /tmp/gaiatest.tmp $GAIATEST