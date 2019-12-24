#retrieve the html from the list of all sas procs by product
def procs(url,reload='No'):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time
    from common.commons import myreader, mywriter
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
        procs = myreader(pathhead,'procs',header='drop')
        return procs

# cycle through procedure links, check for overview and contrasted links
def procs_plus(procs,reload='No'):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time
    from common.commons import myreader, mywriter
    pathhead = 'crawlers/procs_by_product/'
    if reload == 'No':
        # start with procs and add columns:
        procs_plus = procs
        #function to see check if link is for desired purpose and if it needs stump url
        def check_addstump(link,stump):
                link=link.strip()
                if link.startswith('http'):
                    return link
                else:
                    return stump + link
        # cycle through procedure links, check for overview and contrasted links: Collect = Product | Procedure | Procedure_Short | Procedure_Link | Overview_Link | Compared_Link
        comp_stump='https://documentation.sas.com'
        #procs_plus = procs_plus[393:397] #subset for testing
        #procs_plus = procs_plus[290:296] #subset for testing
        driver = webdriver.Safari()
        for row in procs_plus:
            driver.get(row[3])
            time.sleep(10)
            proc_soup = BeautifulSoup(driver.page_source,"lxml")
            for proc_link in proc_soup.find_all('a'):
                if ("Overview" in proc_link.text) and proc_link.get('href'):
                    if "overview" in proc_link.get('href'):
                        row.append(check_addstump(proc_link.get('href'),comp_stump))
            if len(row) != 5:
                    row.append('')
            for proc_link in proc_soup.find_all('a'):
                comps=["Contrasted","Compared"]
                if any(comp in proc_link.text for comp in comps) and proc_link.get('href'):
                    row.append(check_addstump(proc_link.get('href'),comp_stump))
            if len(row) !=6:
                row.append('')
        driver.quit()
        #keep the list of links for products and procedures in procs_plus.csv
        header=["Product","Procedure","Procedure_Short","Procedure_Link","Overview_Link","Compared_Link"]
        mywriter(pathhead,header,procs_plus,'procs_plus')
        return procs_plus
    else:
        procs_plus = myreader(pathhead,'procs_plus',header='drop')
        return procs_plus

# get list of procs mentioned on overview/compared to pages when they exist
def procs_linked(procs_plus,reload='No'):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time
    import csv
    import re
    from common.commons import myreader, mywriter
    pathhead = 'crawlers/procs_by_product/'
    if reload == 'No':
        # start with procs_plus and add columns:
        procs_linked = procs_plus
        #build a list of procedures
        procedures = []
        for row in procs_linked:
            if row[2] not in procedures:
                procedures.append(row[2])
        #keep the list of links for products and procedures in procs_linked.csv
        header=["Product","Procedure","Procedure_Short","Procedure_Link","Overview_Link","Compared_Link",'Compared_PROCS']
        with open(pathhead+"procs_linked.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
        f.close
        driver = webdriver.Safari()
        for row in procs_linked:
            row.append('')
            regex = r"\b[A-Z][A-Z]+\b"
            compared_procs = []
            if row[5]: # get compared PROCs
                driver.get(row[5])
                time.sleep(10)
                comp_soup = BeautifulSoup(driver.page_source,"lxml")
                for comp_link in comp_soup.find_all('p'):
                    for match in re.finditer(regex, comp_link.text):
                        if (match.group() not in compared_procs) and (match.group() in procedures) and (match.group() != row[2]): #not already found, is in full list, not the current proc
                            compared_procs.append(match.group())
                            row[6]=match.group()
                            with open(pathhead+"procs_linked.csv","a") as f:
                                writer = csv.writer(f)
                                writer.writerow(row)
            if row[4]: # get overview PROCs - only keep ones not already covered in compared
                driver.get(row[4])
                time.sleep(10)
                comp_soup = BeautifulSoup(driver.page_source,"lxml")
                for comp_link in comp_soup.find_all('p'):
                    for match in re.finditer(regex, comp_link.text):
                        if (match.group() not in compared_procs) and (match.group() in procedures) and (match.group() != row[2]): #not already found, is in full list, not the current proc
                            compared_procs.append(match.group())
                            row[6]=match.group()
                            with open(pathhead+"procs_linked.csv","a") as f:
                                writer = csv.writer(f)
                                writer.writerow(row)
            if not compared_procs:
                row[6]=''
                with open(pathhead+"procs_linked.csv","a") as f:
                    writer = csv.writer(f)
                    writer.writerow(row)
        driver.quit()
        return procs_linked
    else:
        procs_linked = myreader(pathhead,'procs_linked',header='drop')
        return procs_linked
