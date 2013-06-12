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
#Browser
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center>check_page_loaded</td>
        <td align=left>p_url</td>
        <td align=left>Check the page didn't have a problem.</td>
    </tr>


    <tr>
        <td align=center>open_url</td>
        <td align=left>p_url</td>
        <td align=left>Open url.</td>
    </tr>


    <tr>
        <td align=center>waitForPageToFinishLoading</td>
        <td align=left></td>
        <td align=left>Waits for the current url to finish loading.</td>
    </tr>

</table>
#Calculator
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center></td>
        <td align=left></td>
        <td align=left></td>
    </tr>

</table>
#Calendar
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>
