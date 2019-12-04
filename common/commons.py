# read csv files into lists
def myreader(pathhead,filename,header='keep'):
    import csv
    with open(pathhead+filename+'.csv','r') as f:
        reader = csv.reader(f)
        input_list = list(reader)
    f.close()
    if header != 'keep': del input_list[0]
    return input_list

# write csv files into lists
def mywriter(pathhead,header,listname,filename):
    import csv
    with open(pathhead+filename+'.csv','w',newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(listname)
    f.close()
