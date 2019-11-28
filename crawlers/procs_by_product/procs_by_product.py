#retrieve the html from the list of all sas procs by product
def procs(url,reload='No'):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time
    pathhead = 'crawlers/procs_by_product/'
    if reload == 'No':
        driver = webdriver.Safari()
        driver.get(url)
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source,"lxml")
        driver.close()
        #print(soup)

        # Build the collect list: Product | Procedure | Procedure_Short | Procedure_Link
        bowl = soup.findAll(['h2','p'],attrs={'class':['xisDoc-title','xisDoc-paragraph']})
        procs = []
        product = []
        for spoon in bowl:
            #print('line - ', spoon)
            if spoon.name=='h2' and "SAS Products" not in spoon.text:
                product.append(spoon.text.strip())
            if spoon.name=='p' and product:
                block = spoon.find('a')
                if block:
                    link = block.get('href')
                    proc = ' '.join(block.text.split())
                    proc_short = proc.replace(': ',' ') # template shows up as template: because it has multiple links
                    proc_short = proc_short.split(' ',1)[0]
                    procs.append([product[-1], proc, proc_short, link.strip()])
        #remove the few cases where a product starts by listing another product (not a proc): as in "includes contents of product..."
        for idx, item in enumerate(procs):
            if item[1] in product:
                del procs[idx]
        #keep the list of links for products and procedures in procs.csv
        header=["Product","Procedure","Procedure_Short","Procedure_Link"]
        mywriter(pathhead,header,procs,'procs')
        return procs
    else:
        procs = myreader(pathhead,'procs')
        return procs

# cycle through procedure links, check for overview and contrasted links
def procs_plus(procs,reload='No'):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time
    pathhead = 'crawlers/procs_by_product/'
    if reload == 'No':

        #keep the list of links for products and procedures in procs_plus.csv
        header=["Product","Procedure","Procedure_Short","Procedure_Link","Overview_Link","Compared_Link"]
        mywriter(pathhead,header,procs_plus,'procs_plus')
        return procs_plus
    else:
        procs_plus = myreader(pathhead,'procs_plus')
        return procs_plus

# get list of procs mentioned on overview/compared to pages when they exist
def procs_linked(procs_plus,reload='No'):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time
    import csv
    import re
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
        procs_linked = myreader(pathhead,'procs_linked')
        return procs_linked

# read csv files into lists
def myreader(pathhead,filename):
    import csv
    with open(pathhead+filename+'.csv','r') as f:
        reader = csv.reader(f)
        input_list = list(reader)
    f.close()
    del input_list[0]
    return input_list

# write csv files into lists
def mywriter(pathhead,header,listname,filename):
    import csv
    with open(pathhead+filename+'.csv','w',newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(listname)
    f.close()
