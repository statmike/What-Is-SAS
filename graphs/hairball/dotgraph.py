from graphviz import Digraph
import csv
import itertools
from common.commons import myreader

# read in csv
collect = myreader('process/processed_data/','procs_linked',header='drop')

# iterate by groups
groups = []
uniquekey = []
collect = sorted(collect, key=lambda coll: coll[0])
for k, g in itertools.groupby(collect, lambda coll: coll[0]):
    groups.append(list(g))
    uniquekey.append(k)
#print(uniquekey)
#prit(groups[0])

#create dot graph with graphviz
dot = Digraph(comment = 'SAS Procedures',strict=True)
dot.attr(rankdir='LR')

# function for cluster (subgraph) naming with iteration
def subs(name,label):
    name = Digraph(name,comment=label)
    name.attr(label=label,style="filled",fillcolor="lightgrey",tooltip="This Tooltip (Cluster)")
    return name

# function for escaping & in URL so SVG works in browser
def url_escape(url):
    url_esc ={"&": "&amp;"}
    return "".join(url_esc.get(c,c) for c in url)

i=0
for group in groups:
    i += 1
    group_sub = subs("cluster"+str(i),group[0][0])
    unique_nodes = []
    for row in group:
        if row[1] not in unique_nodes:
            group_sub.node(row[7],URL=url_escape(row[3]),label=row[1],style="filled",fillcolor="white",tooltip="This Tooltip")
            unique_nodes.append(row[1])
        if row[6]:
            if row[5]:
                dot.edge(row[7],row[6]+'0',URL=url_escape(row[5]))
            else:
                dot.edge(row[7],row[6]+'0',URL=url_escape(row[4]))
    dot.subgraph(group_sub)
#print(dot.source)
print(unique_nodes)

# create the dot graph code file - good for interactive testing in atom IDE
#sample = open('Projects/Proc overview/dotgraph.dot', 'w')
#print(dot.source,file=sample)
#sample.close()


dot.format = 'SVG'
dot.render('graphs/hairball/dotgraph')
