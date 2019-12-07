from graphviz import Digraph
import csv
import itertools
from common.commons import myreader



# read in csv
prodclus = myreader('process/processed_data/','product_clusters',header='drop')
collect = myreader('process/processed_data/','procs_linked',header='drop')
prodedge = myreader('process/manual_inputs/','product_edges_manual',header='drop')
action_sets = myreader('process/processed_data/','action_sets',header='drop')
actions_data = myreader('crawlers/actions_by_product/','actions',header='drop')

# function for cluster (subgraph) naming with iteration
def subs(name,label,color):
    name = Digraph(name,comment=label)
    name.attr(label=label,style="filled",fillcolor=color,tooltip="This Tooltip (Cluster)")
    return name

# function for escaping & in URL so SVG works in browser
def url_escape(url):
    #url_esc ={"&": "&amp;"}
    url_esc ={"&": "&#38;"}
    return "".join(url_esc.get(c,c) for c in url)

# build an html table for each actionset where the actionset spans the first row, actions on second row on
def actiontab(actionSet):
    #actionSet is a row from the action_set data: 0=product, 1=actionset,2=description, 3=link, 4=link text
    Node_Name_List.append(actionSet[1])
    colspan=5
    innertab = '<table border="0">'
    # build the rows for actions
    a=0
    for rows in actions_data:
        if rows[1] == actionSet[1]: a += 1
    if a <= colspan: colspan = a
    innertab += '<tr><td colspan="'+str(colspan)+'" port="'+actionSet[1]+'" href="'+url_escape(actionSet[3])+'" tooltip="'+actionSet[2]+'">'+actionSet[1]+'</td></tr>'
    s = 0 # overall count for actions in actionset
    c = 0 # column count for table
    sstruct = '' # holder for row of actions
    for rows in actions_data:
        if rows[1] == actionSet[1]:
            c += 1
            s += 1
            if c == 1 and colspan == 1: # first and last column on row
                struct = '<tr><td port="action_'+rows[2]+'" border="1" href="'+url_escape(rows[4])+'" tooltip="'+rows[3]+'">'+rows[2]+'</td></tr>'
            elif c == 1: # first column on row
                struct = '<tr><td port="action_'+rows[2]+'" border="1" href="'+url_escape(rows[4])+'" tooltip="'+rows[3]+'">'+rows[2]+'</td>'
            elif c == colspan: # last column on row
                struct = struct+'<td port="action_'+rows[2]+'" border="1" href="'+url_escape(rows[4])+'" tooltip="'+rows[3]+'">'+rows[2]+'</td></tr>'
                c = 0
            else: # not first or last column on row
                struct = struct+'<td port="action_'+rows[2]+'" border="1" href="'+url_escape(rows[4])+'" tooltip="'+rows[3]+'">'+rows[2]+'</td>'
            if s % colspan == 0: # end of a complete row
                if not sstruct: sstruct = struct  # first row
                else: sstruct = sstruct+struct  # new row, not first row
    innertab += sstruct+'</table>'
    #return actionSet
    return innertab

#temp = actiontab('cdm')
#print(temp)

#create dot graph with graphviz
dot = Digraph(comment = 'SAS',strict=True, format='SVG')
# ,splines='ortho'
dot.attr(rankdir='LR',splines='polyline')#,compound='True',nodesep='0.1',ranksep='.02')#,ratio='compress')

Node_Name_List = []
clusters = {} # will hold a dictionary to lookup cluster names from product, platform names, also for procedures (_P)

# subclusters for platforms - iterate with by groups - Platform Clusters
platforms = [] # will hold a list of sublist for each value of coll[0] in prodclus - platform (SAS 9, Viya)
platformkey = [] # a list of unique values for coll[0] in prodclus - platform (SAS 9, Viya)
prodclus = sorted(prodclus, key=lambda coll: coll[0])
for k, g in itertools.groupby(prodclus, lambda coll: coll[0]):
    platforms.append(list(g))
    platformkey.append(k)

i1 = 0
for platform in platforms: # gets a list for a platform in platforms
    i1 += 1
    clusters[platform[0][0]] = "cluster_"+str(i1) # a unique value of platform
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
    for product in products: # individual product within a platform
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
                clusters[product[0][1]+'_NP'] = 'p_'+str(i1)+'_'+str(i2)
                # lookup procedures for the product and create a node containing a table (html)
                s = 0 # overall count for procedures in product
                c = 0 # column count for sturcture
                x = 5 # number of columns for structures
                sstruct = '' # holder for the structure label
                for row in collect:
                    if row[0] == product[0][1]:
                        if row[7] not in Node_Name_List:
                            #build a struct row for each x procs as an html table
                            c += 1
                            s += 1
                            if c == 1: # first column on row
                                struct = '<tr><td port="'+row[7]+'" border="1">'+row[1]+'</td>'
                            elif c == x: # last column on row
                                struct = struct+'<td port="'+row[7]+'" border="1">'+row[1]+'</td></tr>'
                                c = 0
                            else: # not first or last column on row
                                struct = struct+'<td port="'+row[7]+'" border="1">'+row[1]+'</td>'
                            if s % x == 0: # end of a complete row
                                if not sstruct: sstruct = struct  # first row
                                else: sstruct = sstruct+struct  # new row, not first row
                            Node_Name_List.append(row[7])
                # check for incomplete stucture, add empty columns, make node
                if s < x: # not a full single row
                    sstruct = '<<table border="0" cellspacing="0">'+struct+'</tr></table>>'
                elif s % x: # more than one row, last row not full (x) so end row with </tr>
                    sstruct = '<<table border="0" cellspacing="0">'+sstruct+struct+'</tr></table>>'
                else: # one or more rows, full
                    sstruct = '<<table border="0" cellspacing="0">'+sstruct+'</table>>'
                procs.node('p_'+str(i1)+'_'+str(i2),label=sstruct,shape='none')
            product_sub.subgraph(procs)
        if product[0][3] == 'Y': # has actions (CAS)
            clusters[product[0][1]+'_A'] = "cluster_"+str(i1)+"_"+str(i2)+"_actions"
            actions = subs(clusters[product[0][1]+'_A'],'Action Sets','white')
            # lookup actionsets for product and create a node containing a table (html)
            # placeholder
            #actions.node('a'+str(i2),label='actions',shape='plaintext',style='invis')

            clusters[product[0][1]+'_NA'] = 'a_'+str(i1)+'_'+str(i2)
            # lookup procedures for the product and create a node containing a table (html)
            s = 0 # overall count for procedures in product
            c = 0 # column count for sturcture
            x = 1 # number of columns for structures
            sstruct = '' # holder for the structure label
            for row in action_sets:
                if row[0] == product[0][1]:
                    if row[1] not in Node_Name_List: # are proc, actionset, action names all unique with no overlap?
                        #build a struct row for each x procs as an html table
                        c += 1
                        s += 1
                        if c==1 and c==x: # first and last column on row
                            struct = '<tr><td port="'+row[1]+'" border="1">'+actiontab(row)+'</td></tr>'
                            c=0
                        elif c == 1: # first column on row
                            struct = '<tr><td port="'+row[1]+'" border="1">'+actiontab(row)+'</td>'
                        elif c == x: # last column on row
                            struct = struct+'<td port="'+row[1]+'" border="1">'+actiontab(row)+'</td></tr>'
                            c = 0
                        else: # not first or last column on row
                            struct = struct+'<td port="'+row[1]+'" border="1">'+actiontab(row)+'</td>'
                        if s % x == 0: # end of a complete row
                            if not sstruct: sstruct = struct  # first row
                            else: sstruct = sstruct+struct  # new row, not first row

            # check for incomplete stucture, add empty columns, make node
            if s < x: # not a full single row
                sstruct = '<<table border="0" cellspacing="0">'+struct+'</tr></table>>'
            elif s % x: # more than one row, last row not full (x) so end row with </tr>
                sstruct = '<<table border="0" cellspacing="0">'+sstruct+struct+'</tr></table>>'
            else: # one or more rows, full
                sstruct = '<<table border="0" cellspacing="0">'+sstruct+'</table>>'
            actions.node('a_'+str(i1)+'_'+str(i2),label=sstruct,shape='none')

            product_sub.subgraph(actions)
        platform_sub.subgraph(product_sub)
    dot.subgraph(platform_sub)



# put edges between products from the product_edges_manual.csv stored in prodedge list: From,To,Edge_Label
for edge in prodedge:
    # get the first prod from each product to do connection with
    if edge[0] == 'SAS Visual Analytics': from_prod = 'SVA'
    elif edge[0] == 'SAS IML': from_prod = 'SIML'
    else: from_prod = clusters[edge[0]+'_NP']
    #else: from_prod = next((item[7] for item in collect if item[0] == edge[0]),'Nothing')
    if edge[1] == 'SAS Visual Analytics': to_prod = 'SVA'
    elif edge[1] == 'SAS IML': to_prod = 'SIML'
    else: to_prod = clusters[edge[1]+'_NP']
    #else: to_prod = next((item[7] for item in collect if item[0] == edge[1]),'Nothing')
    #print(from_prod,to_prod)
    dot.edge(from_prod,to_prod,label=edge[2],ltail=clusters[edge[0]],lhead=clusters[edge[1]])











# create the dot graph code file - good for interactive testing in atom IDE
#sample = open('Projects/Proc overview/dotgraph.dot', 'w')
#print(dot.source,file=sample)
#sample.close()

#print(dot.source)

dot.format = 'SVG'
dot.render('graphs/overview/dotgraph_products_html')
# unflatten -l 3 dotgraph_products | dot -Tsvg -o dotgraph_products.svg
# dot -Tsvg dotgraph_products_html -o dotgraph_products_html.svg



#use regex to fix all href in the svg: escape & as &amp;
import re
regex = re.compile(r"&(?!amp;|lt;|gt;)")
with open('graphs/overview/dotgraph_products_html.svg', 'r') as file:
    lines = file.readlines()

for i, line in enumerate(lines):
    lines[i] = regex.sub("&amp;", line)

with open('graphs/overview/dotgraph_products_html.svg', 'w') as file:
    file.writelines(lines)
