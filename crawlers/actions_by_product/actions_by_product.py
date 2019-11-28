#retrieve the html from the list of action sets by product main page - has product list - save to products.csv
def products(url,reload='No'):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time
    import csv
    pathhead = 'crawlers/actions_by_product/'
    if reload == 'No':
        driver = webdriver.Safari()
        driver.get(url)
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source,"lxml")
        driver.close()
        #print(soup)

        # Build the product list
        bowl = soup.findAll('div',attrs='xisDoc-toc_1 ng-scope')
        #printlist(bowl)
        products = []
        for spoon in bowl:
            products.append([spoon.text,spoon.find('a').get('href')])
        #printlist(products)
        #keep the list of links for actions in products.csv
        header=["Product","Product_Link"]
        with open(pathhead+"products.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(products)
        f.close
        return products
    else:
        products = reader(pathhead,'products')
        return products

# cycle through each product with actions and get list of action sets - save to action_sets.csv
def action_sets(products,reload='No'):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time
    import csv
    pathhead = 'crawlers/actions_by_product/'
    if reload == 'No':
        driver = webdriver.Safari()
        action_sets = []
        for row in products:
            driver.get(row[1])
            time.sleep(10)
            action_soup = BeautifulSoup(driver.page_source,"lxml")
            bowl = action_soup.findAll('tr')
            for spoon in bowl:
                sip = spoon.findAll('td')
                if len(sip) == 3:
                    action_sets.append([row[0],sip[1].text.strip(),' '.join(sip[2].text.split()),sip[0].find('a').get('href').strip(),' '.join(sip[0].text.split())])
        driver.close()
        #keep the list of links for actions in action_sets.csv
        header=["Product","ActionSet","ActionSet_Describe","ActionSet_Link","ActionSet_LinkText"]
        with open(pathhead+"action_sets.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(action_sets)
        f.close
        return action_sets
    else:
        action_sets = reader(pathhead,'action_sets')
        return action_sets


# cycle through each action set and get list of actions by product - save to actions.csv
def actions(action_sets,reload='No'):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time
    import csv
    pathhead = 'crawlers/actions_by_product/'
    if reload == 'No':
        driver = webdriver.Safari()
        actions = []
        for row in action_sets:
            driver.get(row[3])
            time.sleep(8)
            actions_soup = BeautifulSoup(driver.page_source,"lxml")
            bowl = actions_soup.findAll('table',attrs='xisCas-actionstoc')
            for spoon in bowl:
                sip = spoon.findAll('tr')
                for swallow in sip:
                    if swallow.find('a'):
                        temp = swallow.find('td').find_next_sibling('td').text.strip()
                        actions.append([row[0],row[1],swallow.find('td').text.strip(),' '.join(temp.split()),swallow.find('a').get('href').strip()])
        driver.close()
        #keep the list of links for actions in actions.csv
        header=["Product","ActionSet","Action","Action_Describe","Action_Link"]
        with open(pathhead+"actions.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(actions)
        f.close
        return actions
    else:
        actions = reader(pathhead,'actions')
        return actions

# read csv files into lists
def reader(pathhead,listname):
    import csv
    with open(pathhead+listname+'.csv','r') as f:
        reader = csv.reader(f)
        input_list = list(reader)
    f.close()
    del input_list[0]
    return input_list
