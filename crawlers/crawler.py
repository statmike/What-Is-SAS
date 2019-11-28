# imports
import crawlers.actions_by_product.actions_by_product as actions
import crawlers.viya_procs.viya_procs as viya_procs

# easy function for viewing list
def printlist(list):
    length=len(list)
    for i in range(length):
        print(list[i])

actions_by_product_url='https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.5&docsetId=allprodsactions&docsetTarget=actionSetsByProduct.htm&locale=en'
products = actions.products(actions_by_product_url,'Yes')
action_sets = actions.action_sets(products,'Yes')
actions = actions.actions(action_sets,'Yes')

procs_by_product_url='https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.5&docsetId=allprodsproc&docsetTarget=p1vzipzy6l8so0n1gbbh3ae63czb.htm&locale=en'

viya_procs_url='https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.5&docsetId=allprodsproc&docsetTarget=p1o1v16by0iotvn10m0jzzv9i3y8.htm&locale=en#'
viya_procs = viya_procs.procs(viya_procs_url,'Yes')


#printlist(products)
#printlist(action_sets)
#printlist(actions)
#printlist(viya_procs)
