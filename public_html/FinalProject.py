#! /usr/bin/python

import cgi, cgitb
cgitb.enable()

HTML_HEADER = 'Content-type: text/html\n\n'
TopHTML='''
<html>
<head>
<title> Results </title>
</head>
<body>
<center>
<table border="1">
'''
BotHTML='''
</table>
</body>
</html>
'''

def ConvertLine(line):
    fields=line.split(',')
    if len(fields)!=8:
        part=fields[7:]
        part2=','.join(part)
        if '"' in part2:
            part2=part2[1:-1]
        fields=fields[0:7]+[part2]
    else:
        if '"' in fields[7]:
            fields[7]=fields[7][1:-1]
    return fields

    
def small(line):
    val=ConvertLine(line)
    d={}
    key=['CAMIS', 'DBA', 'BUILDING', 'STREET', 'ZIPCODE', 'PHONE', 'INSPECTION DATE', 'VIOLATION DESCRIPTION']
    for i in range(len(key)):
        d[key[i]]=val[i]
    return d

def master(filename):
    f=open(filename,'rU')
    lines=f.read().split('\n')
    lines=lines[1:]
    if len(lines[-1])==0:
        lines=lines[:-1]
    md={}
    for line in lines:
        d=small(line)
        md[d['CAMIS']]=d
    return md

def findme():
    print HTML_HEADER
    print TopHTML
    infos=cgi.FieldStorage()
    keys=infos.keys
    masters=master('mini.txt')
    mkey=masters.keys()
    rating=[]
    if infos.has_key('restaurantname'):
        for key in mkey:
            if str(infos['restaurantname'].value).upper() in  masters[key]['DBA']:
                subkey= masters[key].keys()
                for skeys in subkey:
                    print '<tr><td> %s </td> <td> %s </td></tr>' %(skeys,masters[key][skeys])
    else:
        print 'Restaurant cannot be found'
    print BotHTML
findme()
