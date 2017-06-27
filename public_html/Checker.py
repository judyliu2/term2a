#! /usr/bin/python

import cgi, cgitb
cgitb.enable()

HTML_HEADER = 'Content-type: text/html\n\n'
TopHTML='''
<html>
<head>
<link rel="stylesheet" type="text/css"
          href="https://fonts.googleapis.com/css?family=Roboto">
<title>Restaurant Results </title>
<style>

h1{
font-family:"Roboto";
font-size:40px;
color:#000000;
background-color:#ff8080;}

body{
font-family:"Roboto";
background-color:#d5f4e6;
background-image:url("15544912-Vintage-Restaurant-Background-With-Icons-Illustration-Stock-Vector.jpg");
}

a:hover{
color:#b0aac0;
}

table{
font-family:"Roboto";
border-radius:12px;
font-size:18px;
background-color:#f9ccac;
border: 19px ridge #c83349;
padding: 5px;
width:650px;}

table th{
padding: 9px;
4px solid #3333cc;
letter-spacing: 0.05em;
height:200px;
width: 100px}

ul {font-family:"Roboto";
    font-size:25px;
    list-style-type: none;
    margin: 0;
    padding: 0;
    width: 20%;
    background-color: #f9ccac;
    position: fixed;
    height: 100%;
    overflow: auto;
}

li a {
    display: block;
    color: #000;
    padding: 8px 0 8px 16px;
    text-decoration: none;
}

li a.active {
    background-color: #ff8080;;
    color: white;
}

li a:hover:not(.active) {
    background-color: #ff8080;;
    color: white;
}

</style>
</head>
<body>

<ul>
  <li><a class="active" href="http://marge.stuy.edu/~judy.liu1/page1.html">Home</a></li>
  <li><a href="http://marge.stuy.edu/~judy.liu1/checker.html">Restaurant Checker</a></li>
  <li><a href="http://marge.stuy.edu/~judy.liu1/finder.html">Restaurant Finder</a></li>
  <li><a href="http://marge.stuy.edu/~judy.liu1/near.html">Restaurants Near Stuy</a></li>
</ul>

<div style="margin-left:20%;padding:1px 16px;height:1000px;">


<h1><center> Restaurant Results </center></h1>
<center>
'''
BotHTML='''
</body>
</html>
'''

def ConvertLine(line):
    fields=line.split(',')
    if len(fields)!=9:
        part=fields[7:-1]
        part2=','.join(part)
        if '"' in part2[0]:
            part2=part2[1:-1]
            fields=fields[:7]+list(part2)+[fields[-1]]
        if fields[-1]=='':
            fields[-1]='No grade'
        fields=fields[:7]+[part2]+[fields[-1]]
    else:
        if '"' in fields[7]:
            fields[7]=fields[7][1:-1]
        if fields[-1]=='':
            fields[-1]='No grade'
    return fields
    
def small(line):
    val=ConvertLine(line)
    d={}
    key=['CAMIS', 'DBA', 'BORO', 'BUILDING', 'STREET', 'ZIPCODE','CUISINE DESCRIPTION','VIOLATION DESCRIPTION','GRADE']
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
    masters=master('checker.csv')
    mkey=masters.keys()
    rating=[]
    if infos.has_key('restaurantname'):
        for key in mkey:
            if str(infos['restaurantname'].value).upper() in  masters[key]['DBA']:
                print '<table>'
                subkey= masters[key].keys()
                for skeys in subkey:
                    print '<tr><td><strong> %s:</strong> </td> <td> %s </td></tr>' %(skeys,masters[key][skeys])
                print '</table><br>'
    print 'If there are no results, there is no input for "restaurant name" or input value is not found.'
    print BotHTML
findme()

