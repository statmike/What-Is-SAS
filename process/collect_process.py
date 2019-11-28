import csv
import itertools

# read in csv
with open('Projects/PROC overview/collect.csv','r') as f:
    reader = csv.reader(f)
    collect = list(reader)
f.close()

#remove header row from list
#del collect[0]

# easy function for viewing list
def printlist(list):
    length=len(list)
    for i in range(length):
        print(list[i])
#printlist(collect)

# The rows for TEMPLATE: type of template are causing the create of the dot.svg to break as : is interpreted for port
for row in collect:
    if 'TEMPLATE:' in row[1]:
        row[1]=row[1].replace(':',' -')

# create node_name for each unique occurence of the PROC across products
# 1 - unique list of Product | Procedure | Procedure_Short
header = collect.pop(0)
node_list = []
for row in collect:
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
for row in collect:
    for node in node_list:
        if row[:3] == node[:3]:
            row.append(node[-1])
header.append('Node_Name')
collect.insert(0,header)

# Products added to product_clusters.csv
with open('Projects/PROC overview/product_clusters_manual.csv','r') as f:
    reader = csv.reader(f)
    pcm = list(reader)
f.close()

unique_products = []
for row in pcm:
    unique_products.append(row[1])
for row in collect:
    if row[0] not in unique_products:
        unique_products.append(row[0])
        pcm.append(['SAS 9',row[0],'Y','N'])

with open("Projects/PROC overview/product_clusters.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(pcm)
f.close












with open("Projects/PROC overview/collect_processed.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(collect)
f.close
