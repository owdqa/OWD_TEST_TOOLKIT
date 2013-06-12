# Notes about using 'utils' classes

To implement these, put this in the import section of your code:

<pre>
from OWDTestToolkit import *
</pre>

Then in the 'setUp() method of your code, put:

<pre>
self.UTILS   = UTILS(self)
</pre>

Then you can use these methods in your code like this:

<pre>
self.UTILS.TEST(True, "I am using the utils classes!")
</pre>


<!--api-->
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>
