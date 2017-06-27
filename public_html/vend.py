#! /usr/bin/python
# Show variables passed via CGI

import cgi, cgitb
cgitb.enable()

def Main():
    form=cgi.FieldStorage()
    the_keys=form.keys()
    the_keys.sort()
    html=''
    for akey in the_keys:
        avalue=form.getvalue(akey,'')
        html+=akey+'='+str(avalue)+'<br>\n'
    print 'Content-type: text/html\n'
    print '<html><body><b>Variables and values sent:</b><p>\n'
    print html
    print '</body></html>'
    
        
Main()

