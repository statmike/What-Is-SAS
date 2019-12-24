#retrieve the html from the list of all sas procs by product
def viya_procs(url,reload='No'):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time
    from common.commons import myreader, mywriter
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
        viya_procs = []
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
                    viya_procs.append([products[-1], proc, proc_short, link.strip()])
        #keep the list of links for products and procedures in procs.csv
        header=["Product","Procedure","Procedure_Short","Procedure_Link"]
        mywriter(pathhead,header,viya_procs,'viya_procs')
        return viya_procs
    else:
        viya_procs = myreader(pathhead,'viya_procs',header='drop')
        return viya_procs
