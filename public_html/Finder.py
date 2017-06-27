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
color:#001133;
background-color:#99ccff;}

h2{
background-color:#99ddff;
font-family:"Futura";
font-size:20px;
font-family:"Roboto";
}

body{
color:#004466;
background-color:#b3f0ff;
background-image:url("background2.png");
background-attachment: fixed;
margin:0;
}

a:hover{
color:#b0aac0;
}

table{
font-family:"Roboto";
border-radius:12px;
font-size:18px;
background-color:#deeaee;
border: 19px ridge RoyalBlue;
padding: 5px}

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
    background-color: #deeaee;
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
    background-color: RoyalBlue;
    color: white;
}

li a:hover:not(.active) {
    background-color: RoyalBlue;
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
    return fields

    
def small(line):
    val=ConvertLine(line)
    d={}
    key=['CAMIS', 'DBA', 'BORO', 'BUILDING', 'STREET', 'ZIPCODE', 'PHONE', 'CUISINE DESCRIPTION']
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
    masters=master('finder.csv')
    mkey=masters.keys()
    for key in mkey:
        if infos.has_key('borough'):
            if str(infos['borough'].value).upper()== masters[key]['BORO']:
                if infos.has_key('restaurantname'):
                    if str(infos['restaurantname'].value).upper() in  masters[key]['DBA']:
                        print '<table>'
                        subkey= masters[key].keys()
                        for skeys in subkey:
                            print '<tr><td> %s: </td> <td> %s </td></tr>' %(skeys,masters[key][skeys])
                        print '</table><br>'
    print '<h2>If there are no results, there may be no inputs for "restaurant name" or your restaurant is not found in %s.</h2>' %(str(infos['borough'].value))
    print BotHTML
findme()
