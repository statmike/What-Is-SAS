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

import itertools

# process procs_linked - data clean, create node_name for unique occurences of PROC
procs_linked = myreader('crawlers/procs_by_product/','procs_linked')
header = procs_linked.pop(0)

# The rows for TEMPLATE: type of template are causing the create of the dot.svg to break as : is interpreted for port
for row in procs_linked:
    if 'TEMPLATE:' in row[1]:
        row[1]=row[1].replace(':',' -')

# create node_name for each unique occurence of the PROC across products
# 1 - unique list of Product | Procedure | Procedure_Short
node_list = []
for row in procs_linked:
    node_list.append(tuple(row[:3]))
node_set=set(node_list)
node_list = []
for row in node_set:
    node_list.append(list(row))
# 2 - group by the Procedure_Short
groups = []
uniquekey = []
node_list = sorted(node_list, key=lambda coll: coll[2])
for k, g in itertools.groupby(node_list, lambda coll: coll[2]):
    groups.append(list(g))
    uniquekey.append(k)
# 3 - node_name variable is Procedure_short + iterator within group
node_list =[]
for group in groups:
    for i, row in enumerate(group):
        row.append(row[2]+str(i))
        node_list.append(row)
# 4 - merge node_list back into collect to add column Node_name
for row in procs_linked:
    for node in node_list:
        if row[:3] == node[:3]:
            row.append(node[-1])
header.append('Node_Name')

mywriter('process/processed_data/',header,procs_linked,'procs_linked_processed')






# process product clusters and add SAS 9 Products without Viya versions
pcm = myreader('process/manual_inputs/','product_clusters_manual')

header = pcm.pop(0)
unique_products = []
for row in pcm:
    unique_products.append(row[1])
for row in procs_linked:
    if row[0] not in unique_products:
        unique_products.append(row[0])
        pcm.append(['SAS 9',row[0],'Y','N'])

mywriter('process/processed_data/',header,pcm,'product_clusters')
