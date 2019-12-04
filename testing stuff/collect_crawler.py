# imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import re
import csv

# easy function for viewing list
def printlist(list):
    length=len(list)
    for i in range(length):
        print(list[i])









#url for page with links to all sas Viya procs by Viya product
base_url='https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.5&docsetId=allprodsproc&docsetTarget=p1o1v16by0iotvn10m0jzzv9i3y8.htm&locale=en#'

#retrieve the html from the list of all sas procs by product
driver = webdriver.Safari()
driver.get(base_url)
time.sleep(10)
soup = BeautifulSoup(driver.page_source,"lxml")
driver.close()
#print(soup)

# Build the collect list: Product | Procedure | Procedure_Short | Procedure_Link
bowl = soup.findAll(['h2','p'],attrs={'class':['xisDoc-title','xisDoc-paragraph']})

vcollect = []
vproduct = []
for spoon in bowl:
    if spoon.name=='h2' and "SAS Products" not in spoon.text:
        vproduct.append(spoon.text.strip())
    if spoon.name=='p' and vproduct:
        block = spoon.find('a')
        if block:
            link = block.get('href')
            proc = ' '.join(block.text.split())
            proc_short = proc.replace(': ',' ') # template shows up as template: because it has multiple links
            proc_short = proc_short.split(' ',1)[0]
            vcollect.append([vproduct[-1], proc, proc_short, link.strip()])

#keep the list of links for products and procedures in vdriver.csv
header=["Product","Procedure","Procedure_Short","Procedure_Link"]
with open("Projects/PROC overview/vdriver.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(vcollect)
f.close

#remove the few cases where a product starts by listing another product (not a proc): as in "includes contents of product..."
#store these separately for linking Viya and 9.4 Product clusters
prodlink = []
for idx, item in enumerate(vcollect):
    if item[1] in product:
        prodlink.append(vcollect[idx])
        del vcollect[idx]

#keep the list of links between 9.4 and viya products in prodlink.csv
header=["Product","Procedure","Procedure_Short","Procedure_Link"]
with open("Projects/PROC overview/prodlink.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(prodlink)
f.close








# url with viya products with action sets
base_url='https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.5&docsetId=allprodsactions&docsetTarget=actionSetsByProduct.htm&locale=en'

#retrieve the html from the list of all sas procs by product
driver = webdriver.Safari()
driver.get(base_url)
time.sleep(10)
soup = BeautifulSoup(driver.page_source,"lxml")
driver.close()
#print(soup)

# Build the collect list: Product | Procedure | Procedure_Short | Procedure_Link
bowl = soup.findAll('div',attrs='xisDoc-toc_1 ng-scope')
#printlist(bowl)
adriver = []
for spoon in bowl:
    adriver.append([spoon.text,spoon.find('a').get('href')])
#printlist(adriver)
#keep the list of links for actions in adriver.csv
header=["Product","Product_Link"]
with open("Projects/PROC overview/adriver.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(adriver)
f.close

# cycle through each product with actions and get list of actions by product - save to acollect.csv
driver = webdriver.Safari()
acollect = [] # Product | ActionSet | ActionSet_Describe | ActionSet_Link | ActionSet_LinkText
for row in adriver:
    driver.get(row[1])
    time.sleep(10)
    action_soup = BeautifulSoup(driver.page_source,"lxml")
    bowl = action_soup.findAll('tr')
    for spoon in bowl:
        sip = spoon.findAll('td')
        if len(sip) == 3:
            acollect.append([row[0],sip[1].text.strip(),' '.join(sip[2].text.split()),sip[0].find('a').get('href').strip(),' '.join(sip[0].text.split())])
            #print(' '.join(sip[0].text.split()),sip[0].find('a').get('href').strip(),sip[1].text.strip(),' '.join(sip[2].text.split()))
driver.close()
#keep the list of links for actions in acollect.csv
header=["Product","ActionSet","ActionSet_Describe","ActionSet_Link","ActionSet_LinkText"]
with open("Projects/PROC overview/acollect.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(acollect)
f.close









#url for page with links to all sas procs by product
#base_url='https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=allprodsproc&docsetTarget=p1vzipzy6l8so0n1gbbh3ae63czb.htm&locale=en'
base_url='https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.5&docsetId=allprodsproc&docsetTarget=p1vzipzy6l8so0n1gbbh3ae63czb.htm&locale=en'

#retrieve the html from the list of all sas procs by product
driver = webdriver.Safari()
driver.get(base_url)
time.sleep(10)
soup = BeautifulSoup(driver.page_source,"lxml")
driver.close()
#print(soup)

# Build the collect list: Product | Procedure | Procedure_Short | Procedure_Link
bowl = soup.findAll(['h2','p'],attrs={'class':['xisDoc-title','xisDoc-paragraph']})
collect = []
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
            collect.append([product[-1], proc, proc_short, link.strip()])
#remove the few cases where a product starts by listing another product (not a proc): as in "includes contents of product..."
for idx, item in enumerate(collect):
    if item[1] in product:
        del collect[idx]
#print(collect)

#keep the list of links for products and procedures in driver.csv
header=["Product","Procedure","Procedure_Short","Procedure_Link"]
with open("Projects/PROC overview/driver.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(collect)
f.close


# cycle through products, visit pages, look for links to overview and comparisons

#build a list of procedures
procedures = []
for row in collect:
    if row[2] not in procedures:
        procedures.append(row[2])
#printlist(procedures)

#function to see check if link is for desired purpose and if it needs stump url
def check_addstump(link,stump):
        link=link.strip()
        if link.startswith('http'):
            return link
        else:
            return stump + link

# cycle through procedure links, check for overview and contrasted links: Collect = Product | Procedure | Procedure_Short | Procedure_Link | Overview_Link | Compared_Link
comp_stump='https://documentation.sas.com'
driver = webdriver.Safari()
#collect = collect[393:397] #subset for testing
#collect = collect[290:296] #subset for testing
for row in collect:
    driver.get(row[3])
    time.sleep(10)
    proc_soup = BeautifulSoup(driver.page_source,"lxml")
    for proc_link in proc_soup.find_all('a'):
        if ("Overview" in proc_link.text) and proc_link.get('href'):
            row.append(check_addstump(proc_link.get('href'),comp_stump))
    if len(row) != 5:
            row.append('')
    for proc_link in proc_soup.find_all('a'):
        comps=["Contrasted","Compared"]
        if any(comp in proc_link.text for comp in comps) and proc_link.get('href'):
            row.append(check_addstump(proc_link.get('href'),comp_stump))
    if len(row) !=6:
        row.append('')
#printlist(collect)

#keep the incompete collect list to run again from here:
header=["Product","Procedure","Procedure_Short","Procedure_Link","Overview_Link","Compared_Link"]
with open("Projects/PROC overview/precollect.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(collect)
f.close



# get list of procs mentioned on overview/compared to pages when they exist: Collect = Product | Procedure | Procecure_Short | Procedure_Link | Overview_Link | Compared_Link | Compared_PROCS (list)
header=["Product","Procedure","Procedure_Short","Procedure_Link","Overview_Link","Compared_Link",'Compared_PROCS']
with open("Projects/PROC overview/collect.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
f.close
for row in collect:
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
                    with open("Projects/PROC overview/collect.csv","a") as f:
                        writer = csv.writer(f)
                        writer.writerow(row)
    if row[4]: # get overview PROCs - only keep ones not already covered in compared
        driver.get(row[4])
        time.sleep(15)
        comp_soup = BeautifulSoup(driver.page_source,"lxml")
        for comp_link in comp_soup.find_all('p'):
            for match in re.finditer(regex, comp_link.text):
                if (match.group() not in compared_procs) and (match.group() in procedures) and (match.group() != row[2]): #not already found, is in full list, not the current proc
                    compared_procs.append(match.group())
                    row[6]=match.group()
                    with open("Projects/PROC overview/collect.csv","a") as f:
                        writer = csv.writer(f)
                        writer.writerow(row)
    if not compared_procs:
        with open("Projects/PROC overview/collect.csv","a") as f:
            writer = csv.writer(f)
            writer.writerow(row)
driver.quit()
#printlist(collect)
