def restaurants():
    try:
        f=open('Restaurants1.csv','rU')
        s=f.read()
        f.close()
        lines=s.split('/n')
        lines=lines[1:-1]
        fields_list=[]
        for line in lines: 
