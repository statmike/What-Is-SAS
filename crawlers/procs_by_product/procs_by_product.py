#retrieve the html from the list of all sas procs by product
def procs(url,reload='No'):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time
    import csv
    pathhead = 'crawlers/procs_by_product/'
    if reload == 'No':

        #keep the list of links for products and procedures in procs.csv
        header=["Product","Procedure","Procedure_Short","Procedure_Link"]
        with open(pathhead+"procs.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(procs)
        f.close
        return procs
    else:
        procs = reader(pathhead,'procs')
        return procs

# cycle through procedure links, check for overview and contrasted links
def procs_plus(procs,reload='No'):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time
    import csv
    pathhead = 'crawlers/procs_by_product/'
    if reload == 'No':

        #keep the list of links for products and procedures in procs_plus.csv
        header=["Product","Procedure","Procedure_Short","Procedure_Link","Overview_Link","Compared_Link"]
        with open(pathhead+"procs_plus.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(procs_plus)
        f.close
        return procs_plus
    else:
        procs_plus = reader(pathhead,'procs_plus')
        return procs_plus

# get list of procs mentioned on overview/compared to pages when they exist
def procs_linked(procs_plus,reload='No'):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time
    import csv
    impore re
    pathhead = 'crawlers/procs_by_product/'
    if reload == 'No':

        #keep the list of links for products and procedures in procs_linked.csv
        header=["Product","Procedure","Procedure_Short","Procedure_Link","Overview_Link","Compared_Link",'Compared_PROCS']
        with open(pathhead+"procs_linked.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
        f.close

        return procs_linked
    else:
        procs_linked = reader(pathhead,'procs_linked')
        return procs_linked

# read csv files into lists
def reader(pathhead,listname):
    import csv
    with open(pathhead+listname+'.csv','r') as f:
        reader = csv.reader(f)
        input_list = list(reader)
    f.close()
    del input_list[0]
    return input_list
