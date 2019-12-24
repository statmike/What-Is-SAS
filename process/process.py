import itertools
from common.commons import myreader, mywriter

def node_name(inputlist,header,prefix,keepcoln,labelcoln):
    # create node_name for each unique occurence of the PROC across products
    # 1 - unique list of Product | Procedure | Procedure_Short
    node_list = []
    for row in inputlist:
        node_list.append(tuple(row[:keepcoln]))
    node_set=set(node_list)
    node_list = []
    for row in node_set:
        node_list.append(list(row))
    # 2 - group by the Procedure_Short
    groups = []
    uniquekey = []
    node_list = sorted(node_list, key=lambda coll: coll[labelcoln])
    for k, g in itertools.groupby(node_list, lambda coll: coll[labelcoln]):
        groups.append(list(g))
        uniquekey.append(k)
    # 3 - node_name variable is Procedure_short + iterator within group
    node_list =[]
    for group in groups:
        for i, row in enumerate(group):
            row.append(prefix+row[labelcoln]+str(i))
            node_list.append(row)
    # 4 - merge node_list back into collect to add column Node_name
    for row in inputlist:
        for node in node_list:
            if row[:keepcoln] == node[:keepcoln]:
                row.append(node[-1])
    header.append('Node_Name')
    return inputlist






# process procs_linked - data clean, create node_name for unique occurences of PROC
procs_linked = myreader('crawlers/procs_by_product/','procs_linked')
header = procs_linked.pop(0)

# The rows for TEMPLATE: type of template are causing the create of the dot.svg to break as : is interpreted for port
for row in procs_linked:
    if 'TEMPLATE:' in row[1]:
        row[1]=row[1].replace(':',' -')

# add node_name column for the short proc name in [2], feed the first thre columns [:3] Product, Proc, Proc_Short
procs_linked = node_name(procs_linked,header,'PROC_',3,2)
print(header)
mywriter('process/processed_data/',header,procs_linked,'procs_linked')






# process viya actionsets - remove actionsets with no actions, add node_name to actions and action_sets
actions = myreader('crawlers/actions_by_product/','actions')
action_sets = myreader('crawlers/actions_by_product/','action_sets')

a_header = actions.pop(0)
as_header = action_sets.pop(0)

used_actionsets = []
for actionset in actions:
    if actionset[1] not in used_actionsets: used_actionsets.append(actionset[1])

for i, action_set in enumerate(action_sets):
    if action_set[1] not in used_actionsets: del action_sets[i]

actions = node_name(actions,a_header,'A_',3,2)
action_sets = node_name(action_sets,as_header,'AS_',2,1)

mywriter('process/processed_data/',a_header,actions,'actions')
mywriter('process/processed_data/',as_header,action_sets,'action_sets')







# process product clusters: add SAS 9 Products without Viya versions, add HAS_PROC=Y/N, HAS_ACTION=Y/N
pcm = myreader('process/manual_inputs/','product_clusters_manual')

# Make list of Products with Procs and actions
proc_products = []
for row in procs_linked:
    if row[0] not in proc_products:
        proc_products.append(row[0])
action_products = []
for row in action_sets:
    if row[0] not in action_products:
        action_products.append(row[0])

# add SAS 9 Products
header = pcm.pop(0)
unique_products = []
for row in pcm:
    unique_products.append(row[1])
for row in procs_linked:
    if row[0] not in unique_products:
        unique_products.append(row[0])
        pcm.append(['SAS 9',row[0]])
# add HAS_PROC, HAS_ACTION
for i, row in enumerate(pcm):
    if row[1] in proc_products: pcm[i].append('Y')
    else: pcm[i].append('N')
    if row[1] in action_products: pcm[i].append('Y')
    else: pcm[i].append('N')
header.append('HAS_PROC')
header.append('HAS_ACTION')

mywriter('process/processed_data/',header,pcm,'product_clusters')






# process viya_procs and remove SAS 9 products from the second columns (visual statistics references SAS/STAT)
viya_procs = myreader('crawlers/viya_procs/','viya_procs')

header = viya_procs.pop(0)
for i, row in enumerate(viya_procs):
    if row[1] in unique_products: del viya_procs[i]

mywriter('process/processed_data/',header,viya_procs,'viya_procs')
