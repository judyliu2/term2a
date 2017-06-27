#! /usr/bin/python

import cgi, cgitb
cgitb.enable()

HTML_HEADER = 'Content-type: text/html\n\n'
TopHTML='''
<html>
<head>
<title> SAT Scores </title>
</head>
<body><center><table border="1">
'''
BotHTML = '</table></center></body></html>'
def ExtremeScores_helper(which_column, how_many, is_top): 
    # read the file and split into lines...
    f=open('SAT-2010.csv','rU')
    s=f.read()
    f.close()
    lines=s.split('\n') 
        
    # now remove first and last lines:
    lines = lines[1:-1]

    # split each line into its fields
    field_lists=[]  # this will be a list of lists
    for line in lines:
        fields=line.split(',')
        # keep the line only if the last field is not "s"
        if fields[-1] != 's':
            if '"' not in line:  # has ordinary school name? add it
                field_lists.append(fields)
            else:  # school name has double-quotes...
                # the last 4 fields are always numbers, so
                school_name_in_parts = fields[1:-4]
                school_name=','.join(school_name_in_parts)
                # remove the double-quotes
                school_name=school_name[1:-1]
                # put the fields back together
                new_fields=fields[0:1]+[school_name]+fields[-4:]
                field_lists.append(new_fields)

    # create a list of just [[score,school_name],[score,school_name],...]
    list_to_sort=[]
    for f_list in field_lists:
        if 3<=which_column<=5:
            list_to_sort.append([int(f_list[which_column]),f_list[1]])
        else:  # we want the total SAT score
            total=int(f_list[3])+int(f_list[4])+int(f_list[5])
            list_to_sort.append([total,f_list[1]])
            
    # now sort it
    if is_top:
        sorted_list=sorted(list_to_sort,reverse=True)
    else:
        sorted_list=sorted(list_to_sort)
    
    return sorted_list[:how_many]

# This is the Step #1 function
# We assume that the arguments are all reasonable...
def ExtremeScores(which_column, how_many, is_top):
    the_list=ExtremeScores_helper(which_column, how_many, is_top)

    # let's get the column headers...
    s=open('SAT-2010.csv','rU').read()
    headers=s.split('\n')[0].split(',')+['Total']
    print headers[which_column]+' , school'
    for i in range(how_many):
        print str(the_list[i][0])+' , '+the_list[i][1]

def scoreme():
    infos=cgi.FieldStorage()
    keys=infos.keys()
    print HTML_HEADER
    print TopHTML
    scoreT=7
    High=False
    scoreS=5
    tabletop='<tr><th> School Name </th> <th> Score </td></tr>'
    print tabletop
    if infos.has_key('scoretype'):
        if str(infos['scoretype'].value)=='Math Mean':
            scoreT=4
        elif str(infos['scoretype'].value)=='Writing Mean':
            scoreT=5
        elif str(infos['scoretype'].value)=='Reading Mean':
            scoreT=3
        else:
            scoreT=6
    if infos.has_key('toporbot'):
        if str(infos['toporbot'].value)=='top':
            High=True
        else:
            High=False
    if infos.has_key('numschools'):
        scoreS=int(infos['numschools'].value)
    ans=ExtremeScores_helper(scoreT,scoreS,High)
    for i in ans:
        print '<tr><td>%s</td> <td>%d</td></tr>' %(i[1],i[0])
    print BotHTML
scoreme()
