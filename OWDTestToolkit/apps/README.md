# Notes about using app classes

To implement these, put this in the import section of your code:

<pre>
from OWDTestToolkit import *
</pre>

Then in the 'setUp() method of your code, put:

<pre>
self.browser   = Browser(self)
</pre>

(... or whatever app you want to use.)

Then you can use these methods in your code like this:

<pre>
self.browser.check_page_loaded("http://www.this_api_works_for_me.com")
</pre>

<!--api-->
