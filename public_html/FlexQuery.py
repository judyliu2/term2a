Python 2.7.6 (default, Jun 22 2015, 17:58:13) 
[GCC 4.8.2] on linux2
Type "copyright", "credits" or "license()" for more information.
>>> 
#! /usr/bin/python

import cgi, cgitb
cgitb.enable()


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

