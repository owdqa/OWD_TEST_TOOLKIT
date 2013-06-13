import base64, sys
from marionette import Marionette

#
# The first variable is the log directory.
#
LOGDIR  = sys.argv[1] + "/"

ucount  = 0
m       = Marionette(host='localhost', port=2828)  
m.start_session()
m.set_search_timeout(1000)

#
# Now loop through all the iframes, gathering details about each one.
#
m.switch_to_frame()
frames = m.find_elements("tag name", "iframe")
for fnum in range (0, len(frames)):
  
    #
    # App name is usually in the "src" attribute, so it's worth a shot..
    #
    frame_src = frames[fnum].get_attribute("src")
      
    if frame_src != "":
        startpos = frame_src.index('/') + 2
        stoppos  = frame_src.index('.')
        appname  = frame_src[startpos:stoppos]
        filename = appname
    else:
        ucount = ucount + 1
        appname  = "(unknown)"
        filename = "unknown_" + str(ucount)
          
    filename_details    = LOGDIR + filename + "_iframe_details.txt"
    filename_screenshot = LOGDIR + filename + ".png"
    filename_htmldump   = LOGDIR + filename + ".html"
    
    print ""
    print "Iframe for app \"" + appname + "\" ..."
    print "    |_ iframe details saved to : " + filename_details
    print "    |_ screenshot saved to     : " + filename_screenshot
    print "    |_ html dump saved to      : " + filename_htmldump
     
    #
    # Record the iframe details (pretty verbose, but 'execute_script' 
    # wasn't letting me use 'for' loops in js for some reason).
    #
    f = open(filename_details, 'w')
    f.write("Attributes for this iframe ...\n")
    num_attribs = m.execute_script("return document.getElementsByTagName('iframe')[" + str(fnum) + "].attributes.length;")
    for i in range(0,num_attribs):
        attrib_name  = m.execute_script("return document.getElementsByTagName('iframe')[" + str(fnum) + "].attributes[" + str(i) + "].nodeName;")
        attrib_value = m.execute_script("return document.getElementsByTagName('iframe')[" + str(fnum) + "].attributes[" + str(i) + "].nodeValue;")

        f.write("    |_ " + attrib_name.ljust(20) + ": \"" + attrib_value + "\"\n")   
    f.close()
 
    #
    # Switch to this frame.
    #
    m.switch_to_frame(fnum)
      
    #
    # Take the screenshot and save it to the file.
    #
    screenshot = m.screenshot()[22:]
    with open(filename_screenshot, 'w') as f:
        f.write(base64.decodestring(screenshot))
    f.close()
          
    #
    # Take the html dump and save it to the file.
    #
    f = open(filename_htmldump, 'w')
    f.write(m.page_source.encode('ascii', 'ignore') )
    f.close()
     
    m.switch_to_frame()
