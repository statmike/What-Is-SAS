#retrieve the html from the list of all sas procs by product
def procs(url,reload='No'):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time
    pathhead = 'crawlers/viya_procs/'
    if reload == 'No':
        driver = webdriver.Safari()
        driver.get(url)
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source,"lxml")
        driver.close()
        #print(soup)

        # Build the collect list: Product | Procedure | Procedure_Short | Procedure_Link
        bowl = soup.findAll(['h2','p'],attrs={'class':['xisDoc-title','xisDoc-paragraph']})
        products = []
        procs = []
        for spoon in bowl:
            if spoon.name == 'h2' and "SAS Products" not in spoon.text:
                products.append(spoon.text.strip())
            if spoon.name == 'p' and products:
                block = spoon.find('a')
                if block:
                    link = block.get('href')
                    proc = ' '.join(block.text.split())
                    proc_short = proc.replace(': ',' ') # template shows up as template: because it has multiple links
                    proc_short = proc_short.split(' ',1)[0]
                    procs.append([products[-1], proc, proc_short, link.strip()])
        #keep the list of links for products and procedures in procs.csv
        header=["Product","Procedure","Procedure_Short","Procedure_Link"]
        mywriter(pathhead,header,procs,'procs')
        return procs
    else:
        procs = myreader(pathhead,'procs',header='drop')
        return procs

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
