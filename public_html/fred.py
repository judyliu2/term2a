#! /usr/bin/python
import cgi, cgitb
cgitb.enable()

def main():
    form=cgi.FieldStorage()
    if 'something' in form:
        his_name=form['something'].value
    else:
        his_name='Mud'
    print 'Content-type: text/html\n'
    print '<html><body>'
    print 'Bless me:'+his_name
    print '</body></html>'

main()
