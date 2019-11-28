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

# read in csv
with open('Projects/PROC overview/driver.csv','r') as f:
    reader = csv.reader(f)
    collect = list(reader)
f.close()
#printlist(collect)

# read in csv
with open('Projects/PROC overview/prodlink.csv','r') as f:
    reader = csv.reader(f)
    prodlink = list(reader)
f.close()
#printlist(prodlink)

# read in csv
with open('Projects/PROC overview/vdriver.csv','r') as f:
    reader = csv.reader(f)
    vcollect = list(reader)
f.close()
#printlist(vcollect)















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
#collect = collect[141:143] #subset for testing
for row in collect:
    driver.get(row[3])
    time.sleep(10)
    proc_soup = BeautifulSoup(driver.page_source,"lxml")
    for proc_link in proc_soup.find_all('a'):
        if ("Overview" in proc_link.text) and proc_link.get('href'):
            if not proc_link.get('href').startswith('#') and len(row) == 4:
                row.append(check_addstump(proc_link.get('href'),comp_stump))
    if len(row) != 5:
            row.append('')
    for proc_link in proc_soup.find_all('a'):
        comps=["Contrasted","Compared"]
        if any(comp in proc_link.text for comp in comps) and proc_link.get('href'):
            if not proc_link.get('href').startswith('#') and len(row) == 5:
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
