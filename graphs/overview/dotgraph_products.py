import collect_process.py

from graphviz import Digraph
import csv
import itertools



# read in csv
#with open('Projects/PROC overview/product_clusters_manual.csv','r') as f:
with open('Projects/PROC overview/product_clusters.csv','r') as f:
    reader = csv.reader(f)
    prodclus = list(reader)
f.close()
#remove header row from list
print(prodclus[0])
del prodclus[0]

# read in csv
with open('Projects/PROC overview/collect_processed.csv','r') as f:
    reader = csv.reader(f)
    collect = list(reader)
f.close()
#remove header row from list
print(collect[0])
del collect[0]

# read in csv
#manual is only product on Viya and able to be added for 9 to viya, remove manual and all SAS 9 products are presented
with open('Projects/PROC overview/product_edges_manual.csv','r') as f:
    reader = csv.reader(f)
    prodedge = list(reader)
f.close()
#remove header row from list
print(prodedge[0])
del prodedge[0]



# easy function for viewing list
def printlist(list):
    length=len(list)
    for i in range(length):
        print(list[i])
#printlist(collect)
#print(collect)

# function for cluster (subgraph) naming with iteration
def subs(name,label,color):
    name = Digraph(name,comment=label)
    name.attr(label=label,style="filled",fillcolor=color,tooltip="This Tooltip (Cluster)")
    return name

# function for escaping & in URL so SVG works in browser
def url_escape(url):
    url_esc ={"&": "&amp;"}
    return "".join(url_esc.get(c,c) for c in url)



#create dot graph with graphviz
dot = Digraph(comment = 'SAS',strict=True)
# ,splines='ortho'
dot.attr(rankdir='LR',splines='polyline')#,compound='True',nodesep='0.1',ranksep='.02')#,ratio='compress')

Node_Name_List = []
clusters = {}
# subclusters for platforms - iterate by groups - Platform Clusters
platforms = []
platformkey = []
prodclus = sorted(prodclus, key=lambda coll: coll[0])
for k, g in itertools.groupby(prodclus, lambda coll: coll[0]):
    platforms.append(list(g))
    platformkey.append(k)
i1 = 0
for platform in platforms:
    i1 += 1
    clusters[platform[0][0]] = "cluster_"+str(i1)
    platform_sub = subs(clusters[platform[0][0]],platform[0][0],'lightgrey')
    # sub-subclusters for products - iterate by groups - Products on Platform
    products =[]
    productkey =[]
    tplatform = sorted(platform, key=lambda coll: coll[1])
    for k, g in itertools.groupby(tplatform, lambda coll: coll[1]):
        products.append(list(g))
        productkey.append(k)
    i2 = 0
    #dot.attr(randdir='TD')
    for product in products:
        i2 +=1
        clusters[product[0][1]] = "cluster_"+str(i1)+"_"+str(i2)
        product_sub = subs(clusters[product[0][1]],product[0][1],'white')
        if product[0][2] == 'Y': # has procedures
            clusters[product[0][1]+'_P'] = "cluster_"+str(i1)+"_"+str(i2)+"_procs"
            procs = subs(clusters[product[0][1]+'_P'],'Procedures','white')
            # special nodes for these products that dont have procs
            if product[0][1] == 'SAS Visual Analytics':
                procs.node('SVA',label='SVA',shape='plaintext',style='invis')
            elif product[0][1] == 'SAS IML':
                procs.node('SIML',label='SIML',shape='plaintext',style='invis')
            else:
                clusters[product[0][1]+'_S'] = 'p_'+str(i1)+'_'+str(i2)
                # lookup procedures for the product and create nodes for each
                s = 0 # overall count for procedures in product
                c = 0 # column count for sturcture
                x = 5 # number of columns for structures
                sstruct = '' # holder for the structure label
                for row in collect:
                    if row[0] == product[0][1]:
                        if row[7] not in Node_Name_List:
                            #build a struct row for each x procs: "<r11> name |<r12> name |<r13> name |<r14> name|<r15> name"
                            c += 1
                            s += 1
                            if c == 1:
                                struct = '<'+row[7]+'> '+row[1]
                            elif c == x:
                                struct = struct+'|<'+row[7]+'> '+row[1]
                                c = 0
                            else:
                                struct = struct+'|<'+row[7]+'> '+row[1]
                            if s % x == 0:
                                if not sstruct: sstruct = '{'+struct+'}'
                                else: sstruct = sstruct+'|{'+struct+'}'
                            Node_Name_List.append(row[7])
                # check for incomplete stucture, add empty columns, make node
                if s < x:
                    procs.node('p_'+str(i1)+'_'+str(i2),label=struct,shape='record')
                elif s % x:
                    for r in range(1,x-(s % x)+1):
                        struct = struct+'| '
                    sstruct = sstruct+'|{'+struct+'}'
                    procs.node('p_'+str(i1)+'_'+str(i2),label=sstruct,shape='record')
                else:
                    procs.node('p_'+str(i1)+'_'+str(i2),label=sstruct,shape='record')
            product_sub.subgraph(procs)
        if product[0][3] == 'Y': # has actions (CAS)
            clusters[product[0][1]+'_A'] = "cluster_"+str(i1)+"_"+str(i2)+"_actions"
            actions = subs(clusters[product[0][1]+'_A'],'Actions','white')
            # lookup actionsets for product and create nodes for each shape=ellipse
            # placeholder until i have the data crawled
            actions.node('a'+str(i2),label='actions',shape='plaintext',style='invis')
            product_sub.subgraph(actions)
        platform_sub.subgraph(product_sub)

    dot.subgraph(platform_sub)
# put edges between products from the product_edges_manual.csv stored in prodedge list: From,To,Edge_Label
for edge in prodedge:
    # get the first prod from each product to do connection with
    if edge[0] == 'SAS Visual Analytics': from_prod = 'SVA'
    elif edge[0] == 'SAS IML': from_prod = 'SIML'
    else: from_prod = clusters[edge[0]+'_S']
    #else: from_prod = next((item[7] for item in collect if item[0] == edge[0]),'Nothing')
    if edge[1] == 'SAS Visual Analytics': to_prod = 'SVA'
    elif edge[1] == 'SAS IML': to_prod = 'SIML'
    else: to_prod = clusters[edge[1]+'_S']
    #else: to_prod = next((item[7] for item in collect if item[0] == edge[1]),'Nothing')
    #print(from_prod,to_prod)
    dot.edge(from_prod,to_prod,label=edge[2],ltail=clusters[edge[0]],lhead=clusters[edge[1]])


# platform clusters: SAS 9 Available on Viya, SAS 9
# color code procs: CAS, 9 Workspace, gradient for both
# add actionsets
# add hyperlinks to procs and actionsets
# add hovertext


# create the dot graph code file - good for interactive testing in atom IDE
#sample = open('Projects/Proc overview/dotgraph.dot', 'w')
#print(dot.source,file=sample)
#sample.close()



dot.format = 'SVG'
dot.render('Projects/Proc overview/dotgraph_products')
# unflatten -l 3 dotgraph_products | dot -Tsvg -o dotgraph_products.svg
